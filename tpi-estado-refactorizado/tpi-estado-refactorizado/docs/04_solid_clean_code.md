## 6. Aplicación de SOLID y Clean Code

### 6.1 Nueva estructura (límites entre componentes)
```
solicitudes/
├── errores.py             ErrorDeNegocio (un solo tipo de error del dominio)
├── modelos.py             Entidades, enums, Parameter Objects (sin dependencias externas)
├── reglas.py              Reglas de negocio puras (prioridad, descripción, transiciones)
├── repositorio.py         Abstracción de persistencia (interfaz)
├── repositorio_sqlite.py  Implementación SQLite (única parte que conoce SQL)
├── servicio.py            Casos de uso (orquesta reglas + repositorio)
├── reporte.py             Cálculo del reporte (datos, sin formato)
├── presentacion.py        Formato de salida por consola
└── cli.py                 Interfaz de línea de comandos (argparse)
```
Dirección de las dependencias: `cli → servicio → (reglas, modelos, repositorio←abstracto)`; `repositorio_sqlite` implementa la abstracción. El dominio **no conoce** a SQLite ni a la consola.

### 6.2 Principios SOLID

| Principio | Problema en la versión inicial | Mejora aplicada | Dónde se ve |
|---|---|---|---|
| **SRP** (responsabilidad única) | `Gestor` validaba, aplicaba reglas, ejecutaba SQL, calculaba y formateaba. | Cada módulo tiene un único motivo de cambio: reglas, persistencia, casos de uso, reporte y presentación están separados. | `reglas.py`, `repositorio_sqlite.py`, `servicio.py`, `presentacion.py` |
| **OCP** (abierto/cerrado) | Un tipo nuevo obligaba a editar 5 lugares; las reglas de prioridad eran `if/elif`. | El plazo vive en el propio `TipoSolicitud`; las reglas de prioridad son **datos** (`REGLAS_DE_PRIORIDAD`). Agregar `BECA` = 1 entrada en el enum + 1 plazo. Agregar una regla = 1 línea en la tupla. | `modelos.py`, `reglas.py` |
| **LSP** (sustitución de Liskov) | No había abstracciones que sustituir. | `RepositorioSqlite` y `RepositorioEnMemoria` (de las pruebas) cumplen el mismo contrato; el servicio funciona igual con cualquiera de los dos (pruebas unitarias con la versión en memoria; pruebas de caracterización con SQLite). | `repositorio.py`, `tests/repositorio_en_memoria.py` |
| **ISP** (segregación de interfaces) | — | La interfaz del repositorio es pequeña y específica: 8 operaciones de consulta/escritura, sin métodos que un cliente no use. El servicio de reporte solo usa `listar_solicitudes` y `listar_responsables`. | `repositorio.py` |
| **DIP** (inversión de dependencias) | `Gestor` creaba conexiones SQLite directamente y usaba una variable global. | `ServicioSolicitudes` recibe un `RepositorioSolicitudes` (abstracción) por constructor; también recibe el reloj. Se prueba sin base de datos real. | `servicio.py` (constructor) |

### 6.3 Clean Code

| Práctica | Antes | Después |
|---|---|---|
| **Nombres que revelan intención** | `q`, `reg`, `asig`, `rep`, `e`, `r`, `rr`, `f`, `nom` | `registrar`, `asignar_responsable`, `calcular_reporte`, `obtener_estudiante`, `solo_sin_responsable`… |
| **Funciones pequeñas** | `buscar`: 42 líneas, complejidad 33 | Métodos de 3–10 líneas; el filtrado vive en `FiltroSolicitudes.coincide` |
| **Manejo de errores** | `except:` que devuelve `None`; errores como texto con prefijo `"ERROR"` | Excepción `ErrorDeNegocio` con el mensaje; la CLI la captura **en un solo lugar** y la convierte en `ERROR: …` + código de salida 1. Los errores de infraestructura **no se ocultan**. |
| **Sin valores mágicos** | `"NUEVA"`, `5/15/10/3`, `200` sueltos | `Estado`, `TipoSolicitud.plazo_estimado_dias`, `LONGITUD_MAXIMA_DESCRIPCION` |
| **Cohesión y acoplamiento** | Un módulo con todo (baja cohesión, alto acoplamiento a SQLite y a la consola) | Módulos cohesivos; el dominio depende solo de abstracciones |
| **Seguridad** | SQL concatenado | Consultas parametrizadas (`?`) — verificado con una prueba que inserta comillas y `DROP TABLE` como texto |
| **Datos inmutables** | Tuplas y listas sin nombre (`f[3]`, `f[6]`) | `dataclass(frozen=True)` con campos con nombre |

### 6.4 Resultado medido

| Métrica | Inicial | Refactorizada |
|---|---|---|
| Complejidad ciclomática promedio (radon) | 11,18 (C) | **2,33 (A)** |
| Función más compleja | `buscar` = 33 (E) | `FiltroSolicitudes.coincide` = 15 (C) |
| Archivos de código fuente | 2 | 10 módulos con responsabilidad única |
| Avisos flake8 (código fuente) | 9 | **0** |
| Índice de mantenibilidad | `gestor.py` = 16,12 (B) | Todos los módulos en rango A (31–100) |
| Pruebas automáticas | 3 (caracterización) | **22** (3 caracterización + 19 unitarias) |

> **Nota metodológica:** el promedio de la versión refactorizada se calcula sobre 67 bloques (incluye muchas clases de datos triviales de complejidad 1), mientras que la inicial tiene 11 bloques. Por eso un indicador más honesto es la **cantidad de funciones con complejidad ≥ 10**: **5** en la inicial (`buscar` 33, `reg` 20, `rep` 18, `cambiar` 13, `main` 11) contra **2** en la refactorizada (`coincide` 15 y `calcular_reporte` 10), y la función más compleja baja de 33 a 15.
