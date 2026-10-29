## 9. Code review profesional y checklist técnico

### 9.1 Checklist técnico
Se aplicó sobre el repositorio en ambos estados. ✅ cumple · ⚠️ cumple parcialmente · ❌ no cumple.

| # | Criterio | Inicial | Refactorizada |
|---|---|---|---|
| **Diseño** | | | |
| 1 | Cada módulo/clase tiene una única responsabilidad (SRP) | ❌ | ✅ |
| 2 | Agregar un tipo/regla no obliga a modificar código existente (OCP) | ❌ | ✅ |
| 3 | Las dependencias apuntan a abstracciones (DIP) | ❌ | ✅ |
| 4 | La lógica de negocio no depende de la consola ni de SQL | ❌ | ✅ |
| **Legibilidad** | | | |
| 5 | Nombres que revelan intención | ❌ | ✅ |
| 6 | Funciones cortas (complejidad ciclomática ≤ 10) | ❌ (máx. 33) | ⚠️ (máx. 15 en `coincide`) |
| 7 | Sin valores mágicos ni duplicación | ❌ | ✅ |
| 8 | Sin código muerto | ❌ | ✅ |
| **Robustez y seguridad** | | | |
| 9 | Consultas parametrizadas | ❌ | ✅ |
| 10 | No se ocultan excepciones (`except:` desnudo) | ❌ | ✅ |
| 11 | Errores de negocio con tipo propio y mensaje claro | ❌ | ✅ |
| 12 | Recursos (conexiones) cerrados con *commit/rollback* garantizado | ⚠️ | ✅ |
| **Pruebas** | | | |
| 13 | Existen pruebas automáticas que se ejecutan con un comando | ⚠️ (solo caracterización) | ✅ |
| 14 | Las reglas se pueden probar sin base de datos | ❌ | ✅ |
| 15 | El comportamiento externo se conserva (golden master) | — (referencia) | ✅ |
| **Repositorio y documentación** | | | |
| 16 | README con descripción, instalación, uso, funcionalidades y tecnologías | ✅ | ✅ |
| 17 | Carpeta `/docs` con decisiones, evidencias y checklist | ❌ | ✅ |
| 18 | Datos sintéticos (sin datos personales reales) | ✅ | ✅ |
| 19 | Estilo uniforme (flake8 sin avisos en el código fuente) | ❌ (9) | ✅ (0) |

### 9.2 Observaciones del review (feedback técnico) y acciones

| ID | Observación | Severidad | Acción | Estado |
|---|---|---|---|---|
| O1 | Regresión: el mensaje "Prioridad invalida" salía en masculino | Alta | Se parametrizó el texto del mensaje; la prueba golden pasó | ✅ Corregida |
| O2 | `RepositorioSqlite._conexion` usaba una clase interna difícil de leer | Media | Se reemplazó por `@contextmanager` | ✅ Corregida |
| O3 | `repositorio.py` tenía una línea de 125 caracteres (flake8 E501) | Baja | Se reordenó el `import` | ✅ Corregida |
| O4 | `FiltroSolicitudes.coincide` tiene complejidad 15 (rango C) | Media | Aceptada: es una cadena de guardas simples y legibles; se documenta como mejora futura (pasar a lista de predicados) | ⏳ Pendiente (futura) |
| O5 | `buscar` carga todas las filas y filtra en memoria (igual que la versión inicial) | Media | Se mantiene para preservar el comportamiento; futura mejora: filtrar en SQL | ⏳ Pendiente (futura) |
| O6 | Cada operación abre y cierra una conexión SQLite | Baja | Aceptable para una CLI; si hubiera concurrencia, usar pool | ⏳ Pendiente (futura) |
| O7 | `cli.ejecutar` usa una cadena `if` por comando | Baja | Futura mejora: diccionario comando → manejador | ⏳ Pendiente (futura) |
| O8 | `existe()` e `inicializar_con_datos_demo()` no forman parte de la interfaz abstracta | Baja | Decisión: son operaciones de infraestructura propias de SQLite, no del dominio | ✅ Decisión documentada |

### 9.3 Criterios de aceptación técnica
La versión refactorizada se acepta cuando **todos** se cumplen:

1. Las 3 pruebas de caracterización pasan sin modificar los golden files.
2. Todas las pruebas unitarias pasan (22/22).
3. flake8 sin avisos en el código fuente.
4. Complejidad ciclomática promedio en rango A y ninguna función en rango D o peor.
5. Ningún `except:` desnudo ni SQL concatenado.
6. Documentación completa en `/docs`.

**Resultado del review: ACEPTADA** (criterios 1 a 6 cumplidos; las observaciones O4–O7 quedan registradas como mejoras futuras).
