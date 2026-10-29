import sqlite3
import datetime
import os

DB = "solicitudes.db"


def e(s):
    return str(s).replace("'", "''")


class Gestor:
    def __init__(self, db=None):
        global DB
        if db:
            DB = db
        self.cnt = 0
        self.ult = None

    def q(self, sql, fetch=False):
        c = sqlite3.connect(DB)
        try:
            cur = c.cursor()
            cur.execute(sql)
            c.commit()
            if fetch:
                return cur.fetchall()
            return cur.lastrowid
        except:
            return None
        finally:
            c.close()

    def init(self):
        if os.path.exists(DB):
            os.remove(DB)
        self.q("CREATE TABLE estudiantes (legajo TEXT PRIMARY KEY, nombre TEXT, email TEXT)")
        self.q("CREATE TABLE responsables (id INTEGER PRIMARY KEY, nombre TEXT, area TEXT)")
        self.q("CREATE TABLE solicitudes (id INTEGER PRIMARY KEY AUTOINCREMENT, legajo TEXT, tipo TEXT, prioridad TEXT, estado TEXT, responsable_id INTEGER, descripcion TEXT, canal TEXT, creado_por TEXT, fecha TEXT)")
        self.q("INSERT INTO estudiantes VALUES ('1001', 'Ana Perez', 'ana.perez@example.com')")
        self.q("INSERT INTO estudiantes VALUES ('1002', 'Bruno Gomez', 'bruno.gomez@example.com')")
        self.q("INSERT INTO estudiantes VALUES ('1003', 'Carla Diaz', 'carla.diaz@example.com')")
        self.q("INSERT INTO estudiantes VALUES ('1004', 'Diego Torres', 'diego.torres@example.com')")
        self.q("INSERT INTO estudiantes VALUES ('1005', 'Elena Ruiz', 'elena.ruiz@example.com')")
        self.q("INSERT INTO responsables VALUES (1, 'Laura Medina', 'Alumnado')")
        self.q("INSERT INTO responsables VALUES (2, 'Martin Sosa', 'Equivalencias')")
        self.q("INSERT INTO responsables VALUES (3, 'Julia Ferrari', 'Bedelia')")
        return "Base inicializada: 5 estudiantes, 3 responsables."

    # def listar_todo(self):
    #     return self.q("SELECT * FROM solicitudes", True)

    def reg(self, legajo, tipo, prioridad, descripcion, canal="CLI", creado_por="sistema", fecha=None):
        tipo = tipo.upper().strip()
        prioridad = prioridad.upper().strip()
        descripcion = descripcion.strip()
        legajo = legajo.strip()
        salida = ""
        if tipo != "CERTIFICADO" and tipo != "EQUIVALENCIA" and tipo != "REINCORPORACION" and tipo != "CONSULTA":
            return "ERROR: Tipo invalido '" + tipo + "'. Valores validos: CERTIFICADO, EQUIVALENCIA, REINCORPORACION, CONSULTA."
        if prioridad != "BAJA" and prioridad != "MEDIA" and prioridad != "ALTA":
            return "ERROR: Prioridad invalida '" + prioridad + "'. Valores validos: BAJA, MEDIA, ALTA."
        if len(descripcion) == 0:
            return "ERROR: La descripcion no puede estar vacia."
        if len(descripcion) > 200:
            return "ERROR: La descripcion supera los 200 caracteres."
        r = self.q("SELECT legajo, nombre FROM estudiantes WHERE legajo = '" + e(legajo) + "'", True)
        if r is None or len(r) == 0:
            return "ERROR: No existe el estudiante con legajo '" + legajo + "'."
        if tipo == "REINCORPORACION":
            if prioridad == "BAJA":
                prioridad = "MEDIA"
                salida = "Aviso: prioridad elevada a MEDIA por tipo REINCORPORACION.\n"
        elif tipo == "CONSULTA":
            if prioridad == "ALTA":
                prioridad = "MEDIA"
                salida = "Aviso: prioridad reducida a MEDIA por tipo CONSULTA.\n"
        elif tipo == "CERTIFICADO":
            pass
        elif tipo == "EQUIVALENCIA":
            pass
        if fecha is None:
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuevo_id = self.q("INSERT INTO solicitudes (legajo, tipo, prioridad, estado, responsable_id, descripcion, canal, creado_por, fecha) VALUES ('" + e(legajo) + "', '" + tipo + "', '" + prioridad + "', 'NUEVA', NULL, '" + e(descripcion) + "', '" + e(canal) + "', '" + e(creado_por) + "', '" + fecha + "')")
        if nuevo_id is None:
            return "ERROR: No se pudo registrar la solicitud."
        return salida + "Solicitud #" + str(nuevo_id) + " registrada (" + tipo + ", prioridad " + prioridad + ", estado NUEVA)."

    def cambiar(self, id_, nuevo):
        nuevo = nuevo.upper().strip()
        if nuevo != "NUEVA" and nuevo != "EN_PROCESO" and nuevo != "RESUELTA" and nuevo != "CERRADA":
            return "ERROR: Estado invalido '" + nuevo + "'. Valores validos: NUEVA, EN_PROCESO, RESUELTA, CERRADA."
        r = self.q("SELECT estado, responsable_id FROM solicitudes WHERE id = " + str(id_), True)
        if r is None or len(r) == 0:
            return "ERROR: No existe la solicitud #" + str(id_) + "."
        actual = r[0][0]
        if actual == "CERRADA":
            return "ERROR: La solicitud #" + str(id_) + " esta CERRADA y no admite cambios de estado."
        if actual == nuevo:
            return "ERROR: La solicitud #" + str(id_) + " ya esta en estado " + nuevo + "."
        if nuevo == "EN_PROCESO" and r[0][1] is None:
            return "ERROR: La solicitud #" + str(id_) + " necesita un responsable antes de pasar a EN_PROCESO."
        if nuevo == "RESUELTA" and r[0][1] is None:
            return "ERROR: La solicitud #" + str(id_) + " necesita un responsable antes de pasar a RESUELTA."
        self.q("UPDATE solicitudes SET estado = '" + nuevo + "' WHERE id = " + str(id_))
        return "Solicitud #" + str(id_) + ": estado " + actual + " -> " + nuevo + "."

    def asig(self, id_, resp_id):
        r = self.q("SELECT estado FROM solicitudes WHERE id = " + str(id_), True)
        if r is None or len(r) == 0:
            return "ERROR: No existe la solicitud #" + str(id_) + "."
        rr = self.q("SELECT nombre, area FROM responsables WHERE id = " + str(resp_id), True)
        if rr is None or len(rr) == 0:
            return "ERROR: No existe el responsable con id " + str(resp_id) + "."
        if r[0][0] == "CERRADA":
            return "ERROR: No se puede asignar responsable a la solicitud #" + str(id_) + " porque esta CERRADA."
        self.q("UPDATE solicitudes SET responsable_id = " + str(resp_id) + " WHERE id = " + str(id_))
        msg = "Solicitud #" + str(id_) + " asignada a " + rr[0][0] + " (" + rr[0][1] + ")."
        if r[0][0] == "NUEVA":
            self.q("UPDATE solicitudes SET estado = 'EN_PROCESO' WHERE id = " + str(id_))
            msg = msg + "\nSolicitud #" + str(id_) + " paso automaticamente a EN_PROCESO."
        return msg

    def buscar(self, estado=None, tipo=None, prioridad=None, legajo=None, texto=None, sin_resp=False, resp=None):
        if estado is not None:
            estado = estado.upper().strip()
            if estado != "NUEVA" and estado != "EN_PROCESO" and estado != "RESUELTA" and estado != "CERRADA":
                return "ERROR: Estado invalido '" + estado + "'. Valores validos: NUEVA, EN_PROCESO, RESUELTA, CERRADA."
        if tipo is not None:
            tipo = tipo.upper().strip()
            if tipo != "CERTIFICADO" and tipo != "EQUIVALENCIA" and tipo != "REINCORPORACION" and tipo != "CONSULTA":
                return "ERROR: Tipo invalido '" + tipo + "'. Valores validos: CERTIFICADO, EQUIVALENCIA, REINCORPORACION, CONSULTA."
        if prioridad is not None:
            prioridad = prioridad.upper().strip()
            if prioridad != "BAJA" and prioridad != "MEDIA" and prioridad != "ALTA":
                return "ERROR: Prioridad invalida '" + prioridad + "'. Valores validos: BAJA, MEDIA, ALTA."
        if legajo is not None:
            legajo = legajo.strip()
        filas = self.q("SELECT s.id, s.tipo, s.prioridad, s.estado, s.legajo, e.nombre, r.nombre, s.descripcion, s.responsable_id FROM solicitudes s LEFT JOIN estudiantes e ON e.legajo = s.legajo LEFT JOIN responsables r ON r.id = s.responsable_id ORDER BY s.id", True)
        out = []
        n = 0
        for f in filas:
            if estado is not None and f[3] != estado:
                continue
            if tipo is not None and f[1] != tipo:
                continue
            if prioridad is not None and f[2] != prioridad:
                continue
            if legajo is not None and f[4] != legajo:
                continue
            if texto is not None and texto.lower() not in f[7].lower():
                continue
            if sin_resp and f[8] is not None:
                continue
            if resp is not None and f[8] != resp:
                continue
            n = n + 1
            if f[6] is None:
                nom = "sin asignar"
            else:
                nom = f[6]
            out.append("#" + str(f[0]) + " | " + f[1] + " | " + f[2] + " | " + f[3] + " | " + f[4] + " " + f[5] + " | " + nom + " | " + f[7])
        if n == 0:
            return "No se encontraron solicitudes."
        return "\n".join(out) + "\nTotal: " + str(n) + " solicitud(es)"

    def rep(self):
        filas = self.q("SELECT s.estado, s.tipo, s.prioridad, s.responsable_id FROM solicitudes s", True)
        total = len(filas)
        sin = 0
        for f in filas:
            if f[3] is None:
                sin = sin + 1
        s = "=== REPORTE DE SOLICITUDES ===\n"
        s = s + "Total de solicitudes: " + str(total) + "\n"
        s = s + "Sin responsable asignado: " + str(sin) + "\n"
        s = s + "\nPor estado:\n"
        for est in ["NUEVA", "EN_PROCESO", "RESUELTA", "CERRADA"]:
            c = 0
            for f in filas:
                if f[0] == est:
                    c = c + 1
            s = s + "  " + est + ": " + str(c) + "\n"
        s = s + "\nPor tipo:\n"
        for t in ["CERTIFICADO", "EQUIVALENCIA", "REINCORPORACION", "CONSULTA"]:
            c = 0
            for f in filas:
                if f[1] == t:
                    c = c + 1
            if t == "CERTIFICADO":
                plazo = 5
            elif t == "EQUIVALENCIA":
                plazo = 15
            elif t == "REINCORPORACION":
                plazo = 10
            else:
                plazo = 3
            s = s + "  " + t + ": " + str(c) + " (plazo estimado: " + str(plazo) + " dias)\n"
        s = s + "\nPor prioridad:\n"
        for p in ["ALTA", "MEDIA", "BAJA"]:
            c = 0
            for f in filas:
                if f[2] == p:
                    c = c + 1
            s = s + "  " + p + ": " + str(c) + "\n"
        s = s + "\nCarga por responsable:\n"
        rs = self.q("SELECT id, nombre, area FROM responsables ORDER BY id", True)
        for r in rs:
            c = 0
            for f in filas:
                if f[3] == r[0]:
                    c = c + 1
            s = s + "  " + r[1] + " (" + r[2] + "): " + str(c) + "\n"
        return s.rstrip("\n")
