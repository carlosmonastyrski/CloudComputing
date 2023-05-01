from flask import Flask, request, jsonify, make_response
from flask_restx import Api, Resource, fields
import mysql.connector

app = Flask(__name__)
api = Api(app, version='1.0', title='API de Productos', description='API para realizar operaciones CRUD en la entidad Productos')

# Configuración de la base de datos
mydb = mysql.connector.connect(
  host="carlosmonas.mysql.pythonanywhere-services.com",
  user="carlosmonas",
  password="passroot",
  database="carlosmonas$products"
)

mycursor = mydb.cursor()

# Definición del modelo Producto
producto_model = api.model('Producto', {
    'id': fields.Integer(required=True, description='ID del producto'),
    'nombre': fields.String(required=True, description='Nombre del producto'),
    'precio': fields.Float(required=True, description='Precio del producto')
})

# Clase para manejar las operaciones CRUD de la entidad Producto
class ProductoDAO(object):
    def get(self, id):
        mycursor.execute("SELECT * FROM productos WHERE id=%s", (id,))
        producto = mycursor.fetchone()
        if producto is not None:
            return {'id': producto[0], 'nombre': producto[1], 'precio': producto[2]}
        api.abort(404, "Producto con id {} no encontrado".format(id))

    def create(self, data):
        sql = "INSERT INTO productos (nombre, precio) VALUES (%s, %s)"
        values = (data['nombre'], data['precio'])
        mycursor.execute(sql, values)
        mydb.commit()
        return "El producto se guardó de forma exitosa"

    def update(self, id, data):
        sql = "UPDATE productos SET nombre=%s, precio=%s WHERE id=%s"
        values = (data['nombre'], data['precio'], id)
        mycursor.execute(sql, values)
        mydb.commit()
        return data

    def delete(self, id):
        mycursor.execute("DELETE FROM productos WHERE id=%s", (id,))
        mydb.commit()

    def get_all(self):
        mycursor.execute("SELECT * FROM productos")
        productos = mycursor.fetchall()
        return [{'id': producto[0], 'nombre': producto[1], 'precio': producto[2]} for producto in productos]

# Instanciamos la clase ProductoDAO
producto_dao = ProductoDAO()

# Definimos la ruta y los métodos disponibles para obtener todos los productos
@api.route('/productos')
class ProductoList(Resource):
    @api.doc('list_productos')
    @api.marshal_list_with(producto_model)
    def get(self):
        '''Obtiene todos los productos'''
        return producto_dao.get_all()

    @api.doc('create_producto')
    @api.expect(producto_model)
    def post(self):
        '''Crea un nuevo producto'''
        return make_response(jsonify({"message" : producto_dao.create(api.payload)}), 201)

# Definimos la ruta y los métodos disponibles para obtener, actualizar y eliminar un producto
@api.route('/productos/<int:id>')
@api.response(404, 'Producto no encontrado')
@api.param('id', 'ID del producto')
class Producto(Resource):
    @api.doc('get_producto')
    def get(self, id):
        '''Obtiene un producto por su ID'''
        return producto_dao.get(id)

    @api.doc('update_producto')
    @api.expect(producto_model)
    def put(self, id):
        '''Actualiza un producto por su ID'''
        return producto_dao.update(id, api.payload)

    @api.doc('delete_producto')
    @api.response(204, 'Producto eliminado')
    def delete(self, id):
        '''Elimina un producto por su ID'''
        producto_dao.delete(id)
        return 'Se eliminó el producto', 204

if __name__ == '__main__':
    app.run(debug=True, port=8123)