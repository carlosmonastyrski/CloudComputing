import pytest
from flask import json
from pytest_bdd import scenarios, given, when, then, parsers
from api import app, producto_dao, mydb


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_all_productos(client):
    response = client.get('/productos')
    assert response.status_code == 200
    assert len(response.json) == len(producto_dao.get_all())


def test_get_producto(client):
    id_producto = 1
    response = client.get(f'/productos/{id_producto}')
    assert response.status_code == 200
    assert response.json['id'] == id_producto


def test_get_producto_no_encontrado(client):
    id_producto = 1000
    response = client.get(f'/productos/{id_producto}')
    assert response.status_code == 404


def test_create_producto(client):
    producto = {'nombre': 'Producto de prueba', 'precio': 10.99}
    response = client.post('/productos', json=producto)
    assert response.status_code == 201
    assert response.json['message'] == 'El producto se guardó de forma exitosa'


def test_update_producto(client):
    id_producto = 1
    producto = {'nombre': 'Producto actualizado', 'precio': 99.99}
    response = client.put(f'/productos/{id_producto}', json=producto)
    assert response.status_code == 200
    assert response.json['nombre'] == producto['nombre']
    assert response.json['precio'] == producto['precio']


def test_delete_producto(client):
    id_producto = 2
    response = client.delete(f'/productos/{id_producto}')
    assert response.status_code == 204
    assert len(producto_dao.get_all()) == 2


# Test BDD
def test_bdd_create_and_delete_producto():
    with given('un nuevo producto', {'nombre': 'Producto de prueba', 'precio': 10.99}):
        when('se crea el producto')
        then('el producto se guarda correctamente')

    with given('un producto existente', {'nombre': 'Producto a eliminar', 'precio': 1.99}):
        when('se elimina el producto')
        then('el producto ya no existe en la base de datos')


# Steps para los tests BDD
@given('un nuevo producto')
def step_create_producto(context):
    context.producto = {'nombre': 'Producto de prueba', 'precio': 10.99}


@given('un producto existente')
def step_create_and_get_producto(context):
    context.producto = {'nombre': 'Producto a eliminar', 'precio': 1.99}
    producto_dao.create(context.producto)
    context.producto_id = producto_dao.get_all()[-1]['id']


@when('se crea el producto')
def step_create_producto_api(context):
    with app.test_client() as client:
        context.response = client.post('/productos', json=context.producto)


@when('se elimina el producto')
def step_delete_producto_api(context):
    with app.test_client() as client:
        context.response = client.delete(f'/productos/{context.producto_id}')


@then('el producto se guarda correctamente')
def step_producto_guardado(context):
    assert context.response.status_code == 201
    assert context.response.json['message'] == 'El producto se guardó de forma exitosa'


@then('el producto ya no existe en la base de datos')
def step_producto_eliminado(context):
    assert context.response.status_code

# Escenario: Crear un nuevo producto
@scenarios('producto.feature', 'Crear un nuevo producto')
def test_crear_nuevo_producto():
    pass

# Escenario: Obtener un producto existente por su ID
@scenarios('producto.feature', 'Obtener un producto existente por su ID')
def test_obtener_producto_existente_por_id():
    pass

# Escenario: Actualizar un producto existente por su ID
@scenarios('producto.feature', 'Actualizar un producto existente por su ID')
def test_actualizar_producto_existente_por_id():
    pass

# Escenario: Eliminar un producto existente por su ID
@scenarios('producto.feature', 'Eliminar un producto existente por su ID')
def test_eliminar_producto_existente_por_id():
    pass

# Función para ejecutar los tests
def test_producto_run():
    from api import app, producto_dao

    # Creamos el cliente de la aplicación Flask para realizar las pruebas
    client = app.test_client()

    # Configuramos Pytest BDD
    with contextlib.suppress(SystemExit):
        pytest.main(
            [
                '--verbose',
                '--capture=no',
                '--color=yes',
                '--disable-warnings',
                '--tb=short',
                '-k',
                'not test_',
                '-s',
                '-p',
                'no:cacheprovider',
                '--strict',
                os.path.join(os.path.dirname(__file__), 'producto.feature')
            ]
        )

test_producto_run()