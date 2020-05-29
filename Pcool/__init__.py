from flask import Flask
from config import ConfigDesarrollo
from flask_wtf import CsrfProtect

#inicializamos flask
app = Flask(__name__)
#configuraciones de nuestra app
app.config.from_object(ConfigDesarrollo)
#inicializamos csrfProtect
csrf = CsrfProtect()

from Pcool.routes import *
