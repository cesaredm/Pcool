from flask import Flask, render_template, request, redirect, url_for, jsonify
from flaskext.mysql import MySQL
import json

''' inicializamos flask '''
app = Flask(__name__)
'''Configuracion de Servidor mysql'''
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_PORT']=3306
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='tiendaonline'
''' inicializamos modulo mysql '''
mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def inicio():
     return render_template('inicio.html')

@app.route('/kamell')
def kamell():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto INNER JOIN producto_tienda ON(producto.idProucto=producto_tienda.producto) INNER JOIN tienda ON(tienda.idTienda=producto_tienda.tienda) WHERE tienda.nombre='Kamell'")
    productosKamell = cursor.fetchall()
    cursor.close()
    return render_template('kamell.html', productos=productosKamell)
    
def mostrarProductosKamell():
    p = []
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto INNER JOIN producto_tienda ON(producto.idProucto=producto_tienda.producto) INNER JOIN tienda ON(tienda.idTienda=producto_tienda.tienda) WHERE tienda.nombre='Kamell'")
    productosKamell = cursor.fetchall()
    cursor.close()
    for item in range(len(productosKamell)):
        producto = productosKamell[item]
        p.append({'id':producto[0],'nombre':producto[1],'descripcion':producto[2],'precio':producto[3],'categoria':producto[4],'imagen':producto[5],'likes':producto[6]})
    return json.dumps(p)

@app.route('/ingresos')
def ingresos():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT idcategoria,nombre FROM categoria")
    datos = cursor.fetchall()
    cursor.close()
    return render_template('ingresos.html', categorias=datos)

''' Metodo para guardar Categorias '''
@app.route('/guardar_categorias', methods=['POST'])
def guardar_categorias():
    if request.method == 'POST':
        var = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categoria(nombre) VALUES('{}')".format(var['nombreCategoria']))
        conn.commit()
        conn.close()
    return redirect(url_for('ingresos'))

''' Metodo para guardar productos '''
@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    if request.method == 'POST':
        d = request.form
        nombre = request.form['nombre']
        precio = request.form['precio']
        descripcion = request.form['descripcion']
        categoria = request.form['categoria']
        imagen = request.form['imagen']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO producto(nombre, descripcion, precio, categoria, imagen, MeGusta) VALUES('{}', '{}', {}, {}, '{}',{})".format(d['nombre'],d['descripcion'],d['precio'],d['categoria'],d['imagen'],d['like']))
        conn.commit()
        cursor.close()
    return redirect(url_for('ingresos'))
    
@app.route('/mostrarModal')
def mostrarModal():
    ''' obtengo el id de producto en idP '''
    idP = request.args.get('idP')
    '''conexion ala base de datos'''
    conn = mysql.connect()
    cursor = conn.cursor()
    '''ejecuto la consulta'''
    cursor.execute("SELECT * FROM producto WHERE idProucto='{}'".format(idP))
    '''obtengo los datos en una tupla'''
    datos = cursor.fetchall()
    '''cierro la conexion a bd'''
    cursor.close()
    '''obtengo el primer arreglo de la tupla '''
    producto = datos[0]
    '''creo un diccionario con los datos para luego mandarlo como json con json.dumps'''
    res = {'nombre':producto[1], 'descripcion':producto[2], 'precio': producto[3], 'imagen':producto[5]}
    '''retorno el diccionario creado '''
    return json.dumps(res)
    
@app.route('/obtenerLike',methods=['POST'])
def obtenerLike():
    if request.method == 'POST':
        likes = request.args.get('like')
        idProducto = request.args.get('idP')
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('agregarLike',[idProducto, likes])
        cursor.close()
        print(likes,idProducto)
        res = {'status':200, 'id':idProducto,'likes':likes}
    return json.dumps(res)
    
@app.route('/mostrarTiendas', methods=['POST'])
def mostrarTiendas():
    if request.method == 'POST':
        tienda = []
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idTienda,nombre FROM tienda")   
        resultados = cursor.fetchall()
        cursor.close()
        '''Recorro las tuplas devueltas por la consulta'''
        for item in range(len(resultados)):
            '''obtengo tupla por tupla'''
            t = resultados[item]
            '''agrego cada item de cada tupla a diccionario'''
            tienda.append({'id':t[0],'nombre':t[1]})
    return json.dumps(tienda) 

@app.route('/mostrarProducto',methods=['POST'])
def mostrarProducto():
    if request.method == 'POST':
        arreglo = []
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idProucto,nombre FROM producto")   
        resultados = cursor.fetchall()
        cursor.close()
        for item in range(len(resultados)):
            p = resultados[item]
            arreglo.append({'id':p[0],'nombre':p[1]})
    return json.dumps(arreglo)
    

@app.route('/guardarTienda',methods=['POST'])
def guardarTienda():
    if request.method == 'POST':
        tienda = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tienda(nombre, direccion,tel1,tel2,facebook,whatsapp,instagram) VALUES('{}','{}','{}','{}','{}','{}','{}')".format(tienda['nombreTienda'],tienda['direccionTienda'],tienda['tel1'],tienda['tel2'],tienda['facebookTienda'],tienda['whatsappTienda'],tienda['instagramTienda']))   
        conn.commit()
        cursor.close()
    return redirect(url_for('/ingresos')),json.dumps({'estado':'Tienda Agregada Exitosamente'})
    
@app.route('/guardarProductoTienda', methods = ['POST'])
def guardarProductoTienda():
    if request.method == 'POST':
        dataSave = request.form
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO producto_tienda(tienda,producto) VALUES({},{})".format(dataSave['tienda'],dataSave['producto']))
        conn.commit()
        cursor.close()
    return json.dumps({'status':'Guardado'})

@app.route('/busquedaGeneral')
def busquedaGeneral():
    arregloProducts = []
    dataSearch = request.args.get('valorBuscar')
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE producto.nombre LIKE '%{}%'".format(dataSearch))
    products = cursor.fetchall()
    cursor.close()
    for item in range(len(products)):
        p = products[item]
        print(p)
        arregloProducts.append({'id':p[0],'nombre':p[1],'descripcion':p[2],'precio':p[3],'categoria':p[4],'imagen':p[5],'likes':p[6]})
    return json.dumps(arregloProducts)

if __name__ == '__main__':   
    app.run(debug=True)