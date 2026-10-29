## 7. Refactorings aplicados con evidencia antes/después

Se aplicaron **8 refactorings** documentados (la consigna exige al menos 4, incluyendo Extract Method, Move Method e Introduce Parameter Object). Cada uno se hizo en pasos pequeños, **ejecutando las pruebas de caracterización después de cada paso**.

### R1 – Extract Method / Replace Magic Values with Enum (smells S2, S3, S7)
**Antes** (`gestor.py:59`, `61`, `91`, `127-137`; se repetía en 3 métodos):
```python
if tipo != "CERTIFICADO" and tipo != "EQUIVALENCIA" and tipo != "REINCORPORACION" and tipo != "CONSULTA":
    return "ERROR: Tipo invalido '" + tipo + "'. Valores validos: CERTIFICADO, EQUIVALENCIA, REINCORPORACION, CONSULTA."
```
**Después** (`modelos.py`): un único método extraído que valida y construye el mensaje a partir del propio enum.
```python
class TipoSolicitud(Enum):
    CERTIFICADO = "CERTIFICADO"; EQUIVALENCIA = "EQUIVALENCIA"
    REINCORPORACION = "REINCORPORACION"; CONSULTA = "CONSULTA"

    @classmethod
    def desde_texto(cls, texto: str) -> "TipoSolicitud":
        return _parsear(cls, texto, "Tipo invalido")
```
**Efecto:** 3 bloques duplicados → 1 función; agregar un valor válido = tocar solo el enum.

### R2 – Extract Class / Separate Presentation from Logic (smells S1, S6)
**Antes:** `Gestor` devolvía cadenas ya formateadas (`return "Solicitud #" + str(nuevo_id) + " registrada (…)"`) y `main.py:57` detectaba errores con `res.startswith("ERROR")`.
**Después:** `ServicioSolicitudes` devuelve objetos (`ResultadoRegistro`, `ResultadoAsignacion`…) o lanza `ErrorDeNegocio`; `presentacion.py` los convierte a texto; `cli.py` captura el error una sola vez.
```python
try:
    print(ejecutar(args, repositorio))
except ErrorDeNegocio as error:
    print(f"ERROR: {error}")
    return 1
```

### R3 – Move Method (smells S2, S11)
**Antes:** el `for` de `buscar` evaluaba 7 filtros con `continue` (complejidad 33) dentro de `Gestor`.
**Después:** la decisión "¿esta solicitud cumple el filtro?" se **movió** a `FiltroSolicitudes.coincide(detalle)`, junto a los datos del filtro. Del mismo modo, el plazo estimado se movió a `TipoSolicitud.plazo_estimado_dias` y el ajuste de prioridad a `reglas.ajustar_prioridad`.
```python
def buscar(self, filtro: FiltroSolicitudes) -> List[SolicitudDetallada]:
    return [d for d in self._repositorio.listar_solicitudes() if filtro.coincide(d)]
```

### R4 – Introduce Parameter Object (smell S10)
**Antes:** `reg(self, legajo, tipo, prioridad, descripcion, canal="CLI", creado_por="sistema", fecha=None)` y `buscar(self, estado, tipo, prioridad, legajo, texto, sin_resp, resp)`.
**Después:** `NuevaSolicitud` y `FiltroSolicitudes` (dataclasses inmutables).
```python
servicio.registrar(NuevaSolicitud(legajo, tipo, prioridad, descripcion))
servicio.buscar(FiltroSolicitudes.desde_texto(tipo="equivalencia", estado="nueva"))
```

### R5 – Parameterize Queries + Dependency Injection (smells S4, S9)
**Antes:** `self.q("SELECT … WHERE legajo = '" + e(legajo) + "'", True)` con `global DB`.
**Después:** `RepositorioSqlite(ruta_db)` con consultas parametrizadas y sin estado global:
```python
c.execute("SELECT legajo, nombre, email FROM estudiantes WHERE legajo = ?", (legajo,))
```

### R6 – Replace Error Code/Text with Exception; no swallowed exceptions (smell S5)
**Antes:** `except: return None`. **Después:** las excepciones de infraestructura se propagan (con *rollback* y cierre de conexión garantizados por un gestor de contexto) y las reglas de negocio lanzan `ErrorDeNegocio`.

### R7 – Rename Method / Rename Variable (smell S8)
`q → _conexion/execute`, `reg → registrar`, `asig → asignar_responsable`, `rep → calcular_reporte`, `cambiar → cambiar_estado`, `e → (eliminada, reemplazada por parámetros)`, `f[3] → solicitud.estado`.

### R8 – Remove Dead Code (smell S12)
Se eliminaron el método comentado `listar_todo`, los atributos `cnt` y `ult` y las ramas vacías `elif … pass`.

### Resumen
| Refactoring | Técnica | Smells que resuelve |
|---|---|---|
| R1 | Extract Method / enum | S2, S3, S7 |
| R2 | Extract Class (separar presentación) | S1, S6 |
| R3 | **Move Method** | S2, S11 |
| R4 | **Introduce Parameter Object** | S10 |
| R5 | Parametrizar consultas + DI | S4, S9 |
| R6 | Excepciones en lugar de texto/`None` | S5 |
| R7 | Rename | S8 |
| R8 | Remove Dead Code | S12 |
