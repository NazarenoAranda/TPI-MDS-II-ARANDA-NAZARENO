## 4. Calidad externa e interna

### 4.1 Calidad externa: qué ve el usuario
Desde la mirada del usuario, la versión inicial **funciona correctamente**: registra solicitudes, rechaza datos inválidos con mensajes claros, aplica las reglas de prioridad, respeta las transiciones de estado, filtra y genera el reporte. Esto se comprobó con tres escenarios de ejecución (flujo completo, errores de negocio y base inexistente) que recorren los 6 comandos en 51 invocaciones (24 + 24 + 3). Todos terminan con los códigos de salida y mensajes esperados.

### 4.2 Calidad interna: qué ve el programador
Por dentro, el mismo sistema es difícil de mantener. El 100 % de la lógica (validación, reglas, SQL, armado de textos del reporte) está en una única clase, `Gestor`, y las métricas lo confirman:

| Métrica (herramienta) | Versión inicial | Lectura |
|---|---|---|
| Complejidad ciclomática promedio (radon) | **11,18 (rango C)** | Funciones difíciles de probar y entender |
| Peor función: `Gestor.buscar` | **33 (rango E)** | Muy alto riesgo de errores al modificarla |
| Índice de mantenibilidad `gestor.py` (radon) | **16,12 (B)** | Cerca del límite inferior de lo aceptable |
| Avisos de estilo (flake8, 120 col.) | **9** (incl. `bare except`) | Líneas de hasta 310 caracteres |
| Líneas de código en un solo archivo | 199 SLOC, 1 % comentarios | Sin documentación ni separación |

### 4.3 Relación con la evolución futura
La calidad interna no se ve en la interfaz, pero determina el **costo del cambio**. Ejemplos concretos sobre la versión inicial:

- **Agregar un nuevo tipo de solicitud** (p. ej. `BECA`) obliga a editar **cinco lugares** distintos de `gestor.py` (líneas 59, 78, 131, 185 y 190) y es fácil olvidar uno.
- **Cambiar de SQLite a otra base** o a una API implica reescribir toda la clase, porque el SQL está mezclado con las reglas.
- **Agregar una interfaz web** es imposible sin duplicar lógica: los métodos devuelven *texto ya formateado* con el prefijo `"ERROR:"` y el programa principal decide si hubo error con `res.startswith("ERROR")`.
- **Probar una regla de negocio** exige una base de datos real: no hay forma de aislarla.
- **Seguridad**: las consultas se arman concatenando texto, de modo que un descuido en un solo campo habilita inyección SQL.

La conclusión es la tesis central del trabajo: *un sistema puede pasar todas las pruebas funcionales y aun así ser una deuda técnica que encarece cada cambio futuro*. La versión refactorizada mantiene la calidad externa (idéntica) y mejora radicalmente la interna.
