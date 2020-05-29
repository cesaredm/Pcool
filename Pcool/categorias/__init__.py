from wtforms import Form,TextField, validators
from flask import flash
from Pcool.conexiondb import mysql
class Categoria(Form):
    nombre = TextField("",[validators.required()])
    
    def guardar(self, cur):
        try:
            cur.execute("INSERT INTO categoria(nombre) VALUES('{}')".format(self.nombre.data))
            message = flash("Categoria Guardada Exitosamente")
        except mysql as err:
            message = flash("No se puede guardar la categoria")
            
        


        