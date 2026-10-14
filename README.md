# Tp-Seminario-Python-UNLa

Proyecto realizado para la materia '11510 Seminario de Lenguajes (Opcion Python)' de la Licenciatura en Sistemas UNLa en el cual se desarrolla una API REST que permita la gestion de ventas de productos con enfoque en el aprendizaje del stack tecnologico, buenas practicas, manejo de datos, operaciones básicas CRUD, aprendizaje en la utilización de un ORM y generación de reportes.

**Alumno**: Garcia Ignacio Joaquin, **Legajo**: UNLA-77248 **(Plan 2024)**

## Instalación

1. Ejecutar "python -m venv .venv" para crear un nuevo entorno virtual
2. Ejecutar "source .venv/Scripts/activate" para activar el entorno virtual
3. Ejecutar "pip install -r requirements.txt" para instalar las librerias necesarias
4. Ejecutar "fastapi run" para ejecutar la aplicacion en localhost con un puerto predeterminado 8000

Con la app corriendo, la documentación interactiva está en http://localhost:8000/docs

## Stack Utilizado

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Borb](https://img.shields.io/badge/Borb-PDF-C0392B?style=for-the-badge)

## Endpoints Disponibles

Se pueden ver todos los endpoints mediante ./postman/collections/Test API Python. Ademas se pueden importar a cualquier tester de endpoints descargando e importando el archivo .json de ./postman/specs

### ABM de Productos
Todos los tipos de endpoints necesarios para crear, modificar, borrar y leer productos. 
Campos disponibles: nombre, precio
Relaciones con: carrito

- GET /
- GET /productos
- GET /productos/{id}
- POST /productos
- PUT /productos/{id}
- DELETE /productos/{id}

### ABM de Ventas
Todos los tipos de endpoints necesarios para crear, modificar, borrar y leer productos. Ademas se provee un endpoint para asociar un carrito a una venta que tenga el campo 'estado' en 'cerrado'
Campos disponibles: fecha, hora, id_carrito
Relaciones con: carrito

- GET /ventas
- GET /ventas/{id}
- POST /ventas
- PUT /ventas/{id}
- DELETE /ventas
- POST /ventas/{id}/carrito

### ABM de Carrito
Todos los tipos de endpoints necesarios para crear, modificar, borrar y leer carritos. Ademas se proveen endpoints para asociar/desasociar un carrito con un producto 
Campos disponibles: fecha_creacion, estado
Relaciones con: productos, venta 

- GET /carritos
- GET /carritos/{id}
- POST /carritos
- PUT /carritos/{id}
- DELETE /carritos/{id}
- POST /carritos/{id}/productos
- DELETE /carritos/{id}/productos/{product_id}

### Testing con Postman

Todos los endpoints se encuentran documentado mediante el swapper automatico de FastApi y tambien a traves de Postman. Se deja adjunto el archivo con la coleccion de endpoints listos para testear e importar a postman en la carpeta "postman/collections/Test API Python"

## Reglas de Negocio

- Una venta solo puede asociarse a un carrito existente, en estado "cerrado" y que no pertenezca a otra venta.
- Solo se pueden agregar o quitar productos de un carrito en estado "abierto".
- Si un producto ya está en el carrito, la cantidad se suma (no se duplica el registro).
- La cantidad al agregar un producto debe ser mayor a 0.
- Un carrito asociado a una venta no se puede modificar ni eliminar.
- No se puede eliminar un producto que esté en algún carrito.
- El "precio_total" de una venta lo calcula la API; no se acepta en el body.

## Documentacion Extendida del Proyecto

Para mayor informacion acerca del proyecto y documentacion se deja un enlace a un Notion con con todo el avance del proyecto y un resumen de la informacion aprendida sobre la materia "Seminario de Lenguajes Python"

[Notion Link](https://app.notion.com/p/Seminario-de-Lenguajes-Python-3b40f5cf994d802f812ec2d76dba3fad?source=copy_link)