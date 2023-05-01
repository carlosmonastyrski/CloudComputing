# Arquitecturas Software en la Nube

# Paso 1: Crear un environment e instalar flask

```
python -m venv env
```
Y para activarlo solamente necesitamos ejecutar:
```
source env/bin/activate
```
Y ya dentro del environment instalamos nuestras dependencias:
```
pip install flask==2.2.3
pip install flask-restx==1.0.6
pip install mysql-connector-python
```

# Paso 2: Crear la base de datos:

Se debe crear una base de datos Mysql y cambiar en el apartado de conexión las credenciales correspondientes.
Para crear la tabla "Productos" puede simplemente utilizar:

```
CREATE TABLE productos (
	id BIGINT auto_increment NOT NULL PRIMARY KEY,
	nombre varchar(255) NULL,
	precio FLOAT NULL
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_0900_ai_ci;
```

# Paso 3: Creación del script api.py
Es una api sencilla de Flask, que tiene como modelo "Productos", donde ese objeto permite las cuatro operaciones de un CRUD, además de un get de todos los objetos de tipo producto.
Y para operaciones de inserción de nuevos productos se usa el método POST de /productos, y se pueden obtener todos con un GET de /productos.
Y para operaciones sobre un producto en concreto se utiliza "/products/id", donde con ese ID se puede obtener su información, editarla o eliminarla
* [api.py](api.py)

# Paso 4: Subirlo a PythonAnywhere
Para subir este proyecto, simplemente debemos ingresar a la web y realizar los siguientes pasos:
* En el apartado web crearemos una nueva aplicación con python 3.10 y reemplazaremos el archivo default por nuestro archivo con nuestra api
* En una nueva terminal debemos instalar las dependencias que están en el paso 1.
* En la pestaña de base de datos, creamos una nueva instancia de mysql y dentro de esta creamos la base de datos "products". 
* Abrimos una terminal de sql, y copiamos el script de creación de la tabla.
* Ya con esto modificamos el archivo .py con los datos de conexión de la base de datos creada
* Por último refrescamos la app para que tome estos últimos cambios, y ya está nuestra API funcionando.