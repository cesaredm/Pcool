from wtforms import Form, TextField, validators
from Pcool.conexiondb import mysql
from flask import flash

class Marca(Form):
    nombre = TextField("", [validators.required()])
    
    def guardar(self, cur):
        try:
            cur.execute("INSERT INTO marca(nombre) VALUES('{}')".format(self.nombre.data))
            message = flash("Marca Saved Succefully.")
        except Exception as err:
            message = flash("No se puede guardar la marca por el error" + err)
        