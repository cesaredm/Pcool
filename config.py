import os
#from flaskext.mysql import MySQL

class Config(object):
    SECRET_KEY='MY_SECRET_KEY'
    #Configuracion de Servidor mysql
    MYSQL_DATABASE_HOST ='localhost'
    MYSQL_DATABASE_PORT =3306
    MYSQL_DATABASE_USER ='root'
    MYSQL_DATABASE_PASSWORD ='19199697tsoCD'
    MYSQL_DATABASE_DB ='Pcool'
    
class ConfigDesarrollo(Config):
    DEBUG = True
    
class ConfigProduction(Config):
    DEBUG = False