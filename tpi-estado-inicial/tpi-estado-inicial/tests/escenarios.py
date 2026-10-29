"""Escenarios de prueba de caracterizacion (comportamiento externo).

Cada escenario es una lista de comandos que se ejecutan en orden contra una
base de datos temporal nueva. La salida completa (stdout + codigo de salida)
se compara contra los archivos de tests/golden/.

Los archivos golden se generaron con la VERSION INICIAL del sistema y la
version refactorizada debe reproducirlos exactamente.
"""

FLUJO_COMPLETO = [
    ["init-demo"],
    ["registrar", "--legajo", "1001", "--tipo", "CERTIFICADO", "--prioridad", "MEDIA",
     "--descripcion", "Necesito certificado de alumno regular"],
    ["registrar", "--legajo", "1002", "--tipo", "REINCORPORACION", "--prioridad", "BAJA",
     "--descripcion", "Solicito reincorporacion a la carrera"],
    ["registrar", "--legajo", "1003", "--tipo", "EQUIVALENCIA", "--prioridad", "ALTA",
     "--descripcion", "Equivalencia de Matematica I"],
    ["registrar", "--legajo", "1004", "--tipo", "consulta", "--prioridad", "alta",
     "--descripcion", "Consulta sobre fechas de examen"],
    ["registrar", "--legajo", "1005", "--tipo", "CERTIFICADO",
     "--descripcion", "No me anda el campus d'alumno"],
    ["registrar", "--legajo", " 1001 ", "--tipo", "EQUIVALENCIA", "--prioridad", "BAJA",
     "--descripcion", "  Equivalencia de Ingles  "],
    ["asignar", "--id", "1", "--responsable", "1"],
    ["asignar", "--id", "3", "--responsable", "2"],
    ["asignar", "--id", "2", "--responsable", "3"],
    ["cambiar-estado", "--id", "1", "--estado", "resuelta"],
    ["cambiar-estado", "--id", "3", "--estado", "RESUELTA"],
    ["cambiar-estado", "--id", "1", "--estado", "CERRADA"],
    ["cambiar-estado", "--id", "2", "--estado", "NUEVA"],
    ["buscar"],
    ["buscar", "--estado", "en_proceso"],
    ["buscar", "--tipo", "certificado"],
    ["buscar", "--prioridad", "ALTA"],
    ["buscar", "--texto", "CAMPUS"],
    ["buscar", "--sin-responsable"],
    ["buscar", "--responsable", "2"],
    ["buscar", "--legajo", "1001"],
    ["buscar", "--tipo", "EQUIVALENCIA", "--estado", "NUEVA"],
    ["reporte"],
]

ERRORES = [
    ["init-demo"],
    ["registrar", "--legajo", "1001", "--tipo", "foo", "--descripcion", "x"],
    ["registrar", "--legajo", "1001", "--tipo", "CERTIFICADO", "--prioridad", "urgente",
     "--descripcion", "x"],
    ["registrar", "--legajo", "1001", "--tipo", "CERTIFICADO", "--descripcion", "   "],
    ["registrar", "--legajo", "1001", "--tipo", "CERTIFICADO", "--descripcion", "a" * 201],
    ["registrar", "--legajo", "9999", "--tipo", "CERTIFICADO", "--descripcion", "Legajo inexistente"],
    ["registrar", "--legajo", "1001' OR '1'='1", "--tipo", "CERTIFICADO",
     "--descripcion", "Intento de inyeccion"],
    ["registrar", "--legajo", "1001", "--tipo", "CERTIFICADO", "--descripcion", "a" * 200],
    ["cambiar-estado", "--id", "1", "--estado", "pendiente"],
    ["cambiar-estado", "--id", "99", "--estado", "EN_PROCESO"],
    ["cambiar-estado", "--id", "1", "--estado", "NUEVA"],
    ["cambiar-estado", "--id", "1", "--estado", "EN_PROCESO"],
    ["cambiar-estado", "--id", "1", "--estado", "RESUELTA"],
    ["asignar", "--id", "99", "--responsable", "1"],
    ["asignar", "--id", "1", "--responsable", "99"],
    ["asignar", "--id", "1", "--responsable", "1"],
    ["asignar", "--id", "1", "--responsable", "2"],
    ["cambiar-estado", "--id", "1", "--estado", "CERRADA"],
    ["cambiar-estado", "--id", "1", "--estado", "NUEVA"],
    ["asignar", "--id", "1", "--responsable", "3"],
    ["buscar", "--estado", "xx"],
    ["buscar", "--tipo", "xx"],
    ["buscar", "--prioridad", "xx"],
    ["buscar", "--texto", "texto que no existe"],
]

SIN_BASE = [
    ["reporte"],
    ["registrar", "--legajo", "1001", "--tipo", "CERTIFICADO", "--descripcion", "x"],
    ["buscar"],
]

ESCENARIOS = {
    "flujo_completo": FLUJO_COMPLETO,
    "errores": ERRORES,
    "sin_base": SIN_BASE,
}
