from wtforms import Form ,TextField, DecimalField, SelectField, FileField, validators
from flask import flash
from Pcool.conexiondb import mysql

class Producto(Form):
    nombre = TextField("",[validators.required()])
    talla = TextField()
    color = TextField()
    precio = DecimalField("", [validators.required()])
    marca = SelectField("Seleccione una marca", choices=[('0','Seleccione una Marca')])
    categoria = SelectField("Seleccione una categoria", choices=[('0','Seleccione una categoria')])
    genero = SelectField("", choices=[(' ','Seleccione un genero'),('M','Masculino'), ('F','Femenino')])
    img1 = TextField("",[validators.required()])
    img2 = TextField()
    img3 = TextField()
    like = DecimalField()
    descripcion = TextField("",[validators.required()])
    product = {}
    listaProduct = []
    
    def guardar(self, cur):
        try:
            cur.execute("INSERT INTO producto VALUES(null,'{}','{}','{}',{},{},{},'{}','{}','{}','{}',{},'{}')".format(self.nombre.data, self.talla.data, self.color.data, self.precio.data, self.marca.data, self.categoria.data, self.genero.data, self.img1.data, self.img2.data, self.img3.data, self.like.data, self.descripcion.data))
            message = flash("Producto Guardado Exitosamente!.")
        except Exception as ex:
            print(ex)
            message = flash("No su puede guardar el producto")
    
    def listaCategoria(self, cur):
        try:
            cur.execute("SELECT id, nombre FROM categoria order by nombre")
            lista = cur.fetchall()
            for i in range(len(lista)):
                item = lista[i]
                self.categoria.choices.append(item)
        except mysql as err:
            pass
        
    
    def listaMarca(self, cur):
        try:
            cur.execute("SELECT id, nombre FROM marca order by nombre")
            lista = cur.fetchall()
            for i in range(len(lista)):
                item = lista[i]
                self.marca.choices.append(item)
        except mysql as err:
            pass
        
    def mostrarProducto(self, cur, NombreTienda):
        try:
            cur.execute("SELECT * FROM producto")
            lista = cur.fetchall()
            for item in range(len(lista)):
                p = lista[item];
                self.listaProduct.append({'id':str(p[0]),'nombre':p[1],'talla':p[2],'color':p[3],'precio':str(p[4]),'marca':str(p[5]),'categoria':str(p[6])})
        except Exception as ex:
            print(ex, "error en la funcion mostrarProducto")
        return lista
    
    def addLikes(self,cur, idP, likes):
        try:
            params = [idP ,likes]
            cur.callproc('addLike',params)
        except Exception as ex:
            print(ex)
        
    def obtenerLikeProduct(self, cur, id):
        try:
            cur.execute("SELECT * FROM producto WHERE id = {}".format(id))
            lista = cur.fetchall()
            p = lista[0]
            self.product['id'] = p[0]
            self.product['likes'] = p[11]
        except Exception as ex:
            print(ex)