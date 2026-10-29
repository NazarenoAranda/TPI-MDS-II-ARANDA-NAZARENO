# Gestión de Solicitudes Académicas — VERSIÓN REFACTORIZADA (`estado-refactorizado`)

Trabajo Práctico Integrador — **Metodología de Sistemas II** · Tecnicatura Universitaria en Programación a Distancia (UTN)
Autor: Nazareno Aranda · Comisión 6
Docentes: Londero Oscar Alberto · Aristiaran Martín León · Londero Guillermo Humberto

## Descripción
Versión mejorada del sistema base (`estado-inicial`). **El comportamiento externo es idéntico** (comprobado con pruebas de caracterización), pero la estructura interna fue refactorizada aplicando SOLID y Clean Code: separación de responsabilidades, abstracción de la persistencia, consultas parametrizadas, manejo de errores explícito y pruebas unitarias.

Resultados medidos (radon / flake8): complejidad ciclomática promedio **11,18 → 2,33**, función más compleja **33 → 15**, avisos de estilo **9 → 0**, pruebas **3 → 22**.

## Instalación y uso
Requisitos: Python 3.10 o superior. **No hay que instalar paquetes** para ejecutar el sistema ni las pruebas.
```bash
python main.py init-demo
python main.py registrar --legajo 1001 --tipo CERTIFICADO --prioridad MEDIA --descripcion "Certificado de alumno regular"
python main.py asignar --id 1 --responsable 1
python main.py cambiar-estado --id 1 --estado RESUELTA
python main.py buscar --estado RESUELTA
python main.py reporte
```
(En algunos sistemas el comando es `python3`.) Ayuda: `python main.py --help`.

### Ejecutar las pruebas
```bash
python -m unittest discover -s tests -v
```
### Análisis de calidad (opcional)
```bash
pip install radon flake8
python -m radon cc -s -a solicitudes
python -m flake8 --max-line-length=120 solicitudes main.py
```

## Funcionalidades
| Comando | Descripción |
|---|---|
| `init-demo` | Crea la base con datos sintéticos (5 estudiantes, 3 responsables) |
| `registrar` | Registra una solicitud (valida y aplica reglas de prioridad) |
| `cambiar-estado` | Cambia el estado respetando las transiciones permitidas |
| `asignar` | Asigna responsable (NUEVA → EN_PROCESO automáticamente) |
| `buscar` | Filtra por `--estado --tipo --prioridad --legajo --texto --sin-responsable --responsable` |
| `reporte` | Totales por estado, tipo, prioridad y carga por responsable |

## Arquitectura
```
solicitudes/
├── errores.py             ErrorDeNegocio
├── modelos.py             Entidades, enums y Parameter Objects
├── reglas.py              Reglas de negocio puras
├── repositorio.py         Abstracción de persistencia (DIP)
├── repositorio_sqlite.py  Implementación SQLite (consultas parametrizadas)
├── servicio.py            Casos de uso
├── reporte.py             Cálculo del reporte
├── presentacion.py        Formato de salida
└── cli.py                 Interfaz de línea de comandos
tests/                     3 pruebas de caracterización + 19 unitarias
docs/                      Informe, diagnóstico, refactorings, checklist de code review, evidencias
```

## Documentación (`/docs`)
Diagnóstico de code smells · SOLID y Clean Code · Refactorings · Pruebas · **Checklist de code review** · Decisiones técnicas · Conclusiones · Declaración de uso de IA · Evidencias (capturas) · Informe PDF.

## Tecnologías
Python 3 · SQLite · argparse · unittest · radon · flake8.

## Tags del repositorio
`estado-inicial` · `etapa-diagnostico` · `etapa-refactoring` · `etapa-pruebas` · `etapa-docs` · `estado-refactorizado`
