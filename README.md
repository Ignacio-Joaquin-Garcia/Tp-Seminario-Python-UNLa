# Tp-Seminario-Python-UNLa

Proyecto realizado para la materia '11510 Seminario de Lenguajes (Opcion Python)' de la Licenciatura en Sistemas UNLa en el cual se desarrolla una API REST que permita la gestion de ventas de productos con enfoque en el aprendizaje del stack tecnologico, buenas practicas, manejo de datos, operaciones básicas CRUD, aprendizaje en la utilización de un ORM y generación de reportes.

**Alumno**: Garcia Ignacio Joaquin, **Legajo**: UNLA-77248 **(Plan 2024)**

## Instalación

1. Ejecutar "python -m venv .venv" para crear un nuevo entorno virtual
2. Ejecutar "source .venv/Scripts/activate" para activar el entorno virtual
3. Ejecutar "pip install -r requirements.txt" para instalar las librerias necesarias
4. Ejecutar "fastapi run" para ejecutar la aplicacion en localhost con un puerto predeterminado 8000

## Stack Utilizado

- Python 3.12
- FastAPI
- SQLite
- SQLAlchemy
- Pandas
- Borb

## Endpoints Disponibles

Se pueden ver todos los endpoints mediante ./postman/collections/Test API Python. Ademas se pueden importar a cualquier tester de endpoints descargando e importando el archivo .json de ./postman/specs

### ABM de Productos
- GET /
- GET /products
- GET /products/{id}
- POST /products
- PUT /products/{id}
- DELETE /products/{id}

### ABM de Ventas

### ABM de Carrito

## Documentacion Extendida del Proyecto

Para mayor informacion acerca del proyecto y documentacion se deja un enlace a un Notion con con todo el avance del proyecto y un resumen de la informacion aprendida sobre la materia "Seminario de Lenguajes Python"

[Notion Link](https://app.notion.com/p/Seminario-de-Lenguajes-Python-3b40f5cf994d802f812ec2d76dba3fad?source=copy_link)