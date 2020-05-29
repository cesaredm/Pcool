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