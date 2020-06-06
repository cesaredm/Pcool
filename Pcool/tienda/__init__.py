from wtforms import Form, TextField, IntegerField, SelectField, validators
from flask import flash

class Tienda(Form):
    nombre = TextField("", [validators.required()])
    direccion = TextField("",[validators.required()])
    telefono = TextField("",[validators.required()])
    facebook = TextField("", [validators.required()])
    instagram = TextField("",[validators.required()])
    propietario = SelectField("s",choices=[('0','Selecciona un propietario')])

    def guardar(self, cur):
        try:
            cur.execute("INSERT INTO tiendas VALUES('{}','{}','{}','{}','{}',{})".format(self.nombre.data,self.direccion.data,self.telefono.data,self.facebook.data,self.instagram.data,self.propietario.data))
            print(self.propietario.data)
        except Exception as ex:
            print(ex)
    
    def listapropietario(self, cur):
        try:
            cur.execute("SELECT id, nombres FROM propietarios ORDER BY nombres")
            lista = cur.fetchall()
            for i in range(len(lista)):
                item = lista[i]
                self.propietario.choices.append(item)
        except Exception as ex:
            print(ex)
