from Pcool import app, csrf
from Pcool.conexiondb import mysql

if __name__ == '__main__':   
    csrf.init_app(app)
    mysql.init_app(app)
    
    app.run()