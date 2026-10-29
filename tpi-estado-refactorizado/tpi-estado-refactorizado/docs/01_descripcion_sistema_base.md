## 3. Descripción del sistema base

### 3.1 Dominio y alcance
Se trabajó sobre el caso sugerido por la cátedra: **Sistema de Gestión de Solicitudes Académicas**. El sistema permite que el personal administrativo de una institución registre solicitudes de estudiantes (certificados, equivalencias, reincorporaciones y consultas), las clasifique por tipo, prioridad y estado, les asigne un responsable, las consulte con filtros y obtenga un reporte resumido.

El alcance es deliberadamente acotado, como pide la consigna: *"no se busca construir un sistema grande, sino analizar y mejorar profesionalmente un módulo acotado"*. La funcionalidad visible es simple; el valor del trabajo está en el diagnóstico, las decisiones de diseño y la evidencia técnica.

### 3.2 Actores
| Actor | Rol |
|---|---|
| Personal administrativo | Registra solicitudes, cambia estados, asigna responsables, consulta y pide reportes (usa la línea de comandos). |
| Estudiante | Es la persona que origina la solicitud; está representado por su legajo (no interactúa directamente con el sistema). |
| Responsable / Área | Persona del área (Alumnado, Equivalencias, Bedelía) a la que se asigna la gestión. |

### 3.3 Entidades (requisito: al menos 3)

- **Estudiante** (`legajo`, `nombre`, `email`)
- **Responsable** (`id`, `nombre`, `area`)
- **Solicitud** (`id`, `legajo`, `tipo`, `prioridad`, `estado`, `responsable_id`, `descripcion`, `canal`, `creado_por`, `fecha`)
- **Estado** (NUEVA, EN_PROCESO, RESUELTA, CERRADA), **Tipo** y **Prioridad** como clasificaciones de la solicitud.

### 3.4 Operaciones funcionales (requisito: al menos 4)
| Comando | Caso de uso |
|---|---|
| `init-demo` | Crea la base con datos **sintéticos** (5 estudiantes, 3 responsables). |
| `registrar` | Registrar una solicitud (valida tipo, prioridad, descripción y existencia del estudiante). |
| `cambiar-estado` | Cambiar el estado respetando reglas de transición. |
| `asignar` | Asignar un responsable (una solicitud NUEVA pasa sola a EN_PROCESO). |
| `buscar` | Buscar/filtrar por estado, tipo, prioridad, legajo, texto, sin responsable o responsable. |
| `reporte` | Reporte básico con totales por estado, tipo, prioridad y carga por responsable. |

### 3.5 Reglas de negocio

1. Tipos válidos: CERTIFICADO, EQUIVALENCIA, REINCORPORACION, CONSULTA. Prioridades: BAJA, MEDIA, ALTA.
2. La descripción es obligatoria y tiene un máximo de 200 caracteres.
3. Una REINCORPORACION con prioridad BAJA se eleva automáticamente a MEDIA; una CONSULTA con prioridad ALTA se reduce a MEDIA.
4. Una solicitud CERRADA no admite cambios de estado ni nuevas asignaciones.
5. No se puede pasar a EN_PROCESO ni a RESUELTA sin responsable asignado.
6. No se puede "cambiar" al estado en que la solicitud ya está.

### 3.6 Tecnología
Python 3.10+ (solo biblioteca estándar), SQLite como persistencia, `argparse` para la interfaz de línea de comandos, `unittest` para las pruebas. Herramientas de análisis: `radon` (complejidad ciclomática e índice de mantenibilidad) y `flake8` (estilo).

### 3.7 Versión inicial y repositorio
La **versión inicial** (tag `estado-inicial`) funciona correctamente desde el punto de vista del usuario, pero fue escrita deliberadamente con problemas reales de diseño e implementación (concentrados en `gestor.py`, 214 líneas, una sola clase). La **versión mejorada** (tag `estado-refactorizado`) conserva exactamente el mismo comportamiento externo con una estructura profesional.

- Repositorio: `https://github.com/NazarenoAranda/TPI-MDS-II-ARANDA-NAZARENO.git`
- Evidencia de funcionamiento de la versión inicial: ver captura `docs/evidencias/01_inicial_funcionando.png`.
