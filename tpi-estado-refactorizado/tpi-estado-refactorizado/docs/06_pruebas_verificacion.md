## 8. Pruebas y verificaciones realizadas

### 8.1 Estrategia: pruebas de caracterización ("golden master")
Para refactorizar con seguridad primero hay que **congelar el comportamiento externo**. Antes de tocar el código se escribieron tres escenarios que ejecutan el programa real por línea de comandos, y se guardó la salida completa (texto + código de salida) de la **versión inicial** en `tests/golden/*.txt`. La versión refactorizada debe reproducir esos archivos **byte a byte**.

| Escenario | Invocaciones | Qué cubre |
|---|---|---|
| `flujo_completo` | 24 | Registro de los 4 tipos, normalización (mayúsculas/espacios), ajustes de prioridad, asignaciones (con cambio automático a EN_PROCESO), cambios de estado, los 7 filtros de búsqueda y el reporte final |
| `errores` | 24 | Tipo/prioridad/estado inválidos, descripción vacía/201 caracteres/200 exactos (límite), legajo inexistente, **intento de inyección SQL**, solicitud/responsable inexistente, transiciones prohibidas, solicitud cerrada |
| `sin_base` | 3 | Comandos sin ejecutar `init-demo` antes |

Los archivos golden **no se regeneran** con la versión refactorizada (hacerlo anularía la prueba): se generaron una sola vez con el tag `estado-inicial`.

### 8.2 Pruebas unitarias (versión refactorizada)
19 pruebas nuevas, posibles solo gracias a la separación de responsabilidades:

- **Reglas** (7): ajustes de prioridad, límites de la descripción (200 ok / 201 error / vacía), parseo de enums.
- **Servicio con repositorio en memoria** (11): registro, estudiante inexistente, transición sin responsable, asignación que pasa a EN_PROCESO, reasignación sin cambiar estado, solicitud cerrada, filtros combinados, reporte.
- **Repositorio SQLite** (1): un texto con comillas y `DROP TABLE` se guarda como texto y la tabla sigue existiendo (consultas parametrizadas).

### 8.3 Cómo ejecutarlas
```
python -m unittest discover -s tests -v
```

### 8.4 Resultados

| Versión | Pruebas | Resultado |
|---|---|---|
| Inicial (`estado-inicial`) | 3 de caracterización | ✅ 3/3 — fija el comportamiento de referencia |
| Refactorizada (`estado-refactorizado`) | 3 de caracterización + 19 unitarias | ✅ 22/22 |

Las capturas de ambas ejecuciones están en `docs/evidencias/` (`02_tests_inicial.png`, `03_tests_refactorizado.png`).

### 8.5 La prueba detectó una regresión real
En la primera ejecución sobre la versión refactorizada, el escenario `errores` **falló**: el mensaje para una prioridad inválida decía *"Prioridad **invalido**"* en lugar de *"Prioridad **invalida**"* (concordancia de género que la versión inicial escribía a mano). Se corrigió parametrizando el texto del mensaje y la prueba volvió a pasar. Este episodio es la justificación práctica del método: sin el *golden master* la regresión habría pasado inadvertida.

### 8.6 Comparación antes/después de salidas
Ejemplo (idéntico en ambas versiones):
```
$ asignar --id 1 --responsable 1
Solicitud #1 asignada a Laura Medina (Alumnado).
Solicitud #1 paso automaticamente a EN_PROCESO.
[exit 0]
```
