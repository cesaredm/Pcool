from wtforms import Form, PasswordField, validators
from wtforms.fields.html5 import EmailField
from flask import flash

class Login(Form):
    correo = EmailField("", [validators.required()])
    password = PasswordField("", [validators.required()])
    respuesta = {}
    
    def validar(self,cur):
        try:
            cur.execute("SELECT u.id,u.nombre,correo,password,permiso, t.logo FROM usuarios AS u LEFT JOIN seguidortienda AS s ON(u.id=s.seguidor) LEFT JOIN tiendas AS t ON(t.id=s.tienda) WHERE u.correo='{}' AND u.password = '{}'".format(self.correo.data, self.password.data))
            datos = cur.fetchall()
            if datos:
                for i in range(len(datos)):
                    item = datos[i]
                    if item:
                        if item[2] == self.correo.data and item[3] == self.password.data and item[4] == 'propietario':
                            self.respuesta['url'] = 'ingreso_productos'
                            self.respuesta['id'] = item[0]
                            self.respuesta['nombre'] = item[1]
                            self.respuesta['logo'] = item[5]
                        elif item[2] == self.correo.data and item[3] == self.password.data and item[4] == 'user':
                            self.respuesta['url'] = 'inicio'
                            self.respuesta['id'] = item[0]
                            self.respuesta['nombre'] = item[1]
                    else:
                        pass
            else:
                self.respuesta['url'] = 'vacio'
            print(self.respuesta)
        except Exception as ex:
            print(ex)