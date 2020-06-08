from flask import Flask, render_template, request, redirect, url_for, jsonify, g, flash, session
from Pcool import app
from Pcool.conexiondb import mysql
from Pcool.producto import Producto
from Pcool.categorias import Categoria
from Pcool.marca import Marca
from Pcool.tienda import Tienda
from Pcool.login import Login
import json

@app.before_request
def before_request():
    #levanto conexion
    g.con = mysql.connect()
    g.cur = g.con.cursor()
    
@app.after_request
def after_request(response):
    #cierro conexion
    g.con.commit()
    g.cur.close()
    return response

@app.route('/', methods = ['GET'])
def inicio():
    if request.method == 'GET':
        if 'user' in session:
            usuario = session['user']
        else:
            usuario = ''
        return render_template('inicio.html', user=usuario)

@app.route('/login')
def login():
    login = Login(request.form)
    return render_template('login.html', login=login)

@app.route('/registro')
def registro():
    return render_template('Register.html')

@app.route('/validacion_login', methods=['POST'])
def validacion_login():
    v = Login(request.form)
    v.validar(g.cur)
    if request.method == 'POST':
        if 'ingreso_productos' == v.respuesta['url']:
            logo = v.respuesta['logo']
            session['userPropietario'] = v.respuesta['nombre']
            return redirect(url_for('ingreso_productos', logo=logo))
        elif 'inicio' == v.respuesta['url']:
            session['user'] = v.respuesta['nombre']       
            return redirect(url_for('inicio'))
        elif 'vacio' == v.respuesta['url']:
            return redirect(url_for('login'))

@app.route('/cerrarSesion', methods=['GET'])
def cerrarSesion():
    if request.method == 'GET':
        if 'user' in session:
            del session['user']
            return redirect(url_for('inicio'))
        elif 'userPropietario' in session:
            del session['userPropietario']
            return redirect(url_for('inicio'))
        else:
            redirect(url_for('inicio'))
            
        
@app.route('/kamell')
def kamell():
    producto = Producto(request.form)
    productos = producto.mostrarProducto(g.cur, 'kamell')
    if 'user' in session:
        user = session['user']
    else:
        user=''
    return render_template('kamell.html',productos = productos, user=user)
    
@app.route('/productosKamell')
def mostrarProductosKamell():
    tienda = request.args.get('nombreTienda')
    p = []
    product = Producto(request.form)
    productosKamell = product.mostrarProducto(g.cur, tienda)
    for item in range(len(productosKamell)):
        producto = productosKamell[item]
        p.append({'id':producto[0],'nombre':producto[1],'imagen':producto[8],'likes':producto[11]})
    return json.dumps(p)

@app.route('/ingresos', methods=['GET', 'POST'])
def ingresos():
    formCategoria = Categoria(request.form)
    formMarca = Marca(request.form)
    tienda = Tienda(request.form)
    tienda.listapropietario(g.cur)
    return render_template('ingresos.html', categorias=formCategoria, marca=formMarca, tienda=tienda)

 #Metodo para guardar Categorias
@app.route('/guardar_categorias', methods=['POST'])
def guardar_categorias():
    categoria = Categoria(request.form)
    if request.method == 'POST' and categoria.validate():
        categoria.guardar(g.cur)
    return redirect(url_for('ingresos'))

#metodo para guardar Marcas
@app.route('/guardar_marca', methods=['POST'])
def guardar_marca():
    fmarca = Marca(request.form)
    if request.method == 'POST' and fmarca.validate():
        fmarca.guardar(g.cur)
    return redirect(url_for('ingresos'))

#
@app.route('/ingreso_productos', methods=['GET'])
def ingreso_productos():
    if request.method == 'GET':
        formProducto = Producto(request.form)
        formProducto.listaCategoria(g.cur)
        formProducto.listaMarca(g.cur)
        if 'userPropietario' in session:
            propietario = session['userPropietario']
            return render_template('ingresoProductos.html', datos=formProducto, user = propietario)
        else:
            return redirect(url_for('inicio'))

#Metodo para guardar productos
@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    p = Producto(request.form)
    p.guardar(g.cur)
    '''if request.method == 'POST' and p.validate():
        p.guardar(g.cur)'''
    return redirect(url_for('ingreso_productos'))
    
@app.route('/mostrarModal')
def mostrarModal():
    # obtengo el id de producto en idP 
    idP = request.args.get('idP', "vacio")
    if idP != 'vacio':
        #conexion ala base de datos
        conn = mysql.connect()
        cursor = conn.cursor()
        #ejecuto la consulta
        cursor.execute("SELECT * FROM producto WHERE id={}".format(idP))
        #obtengo los datos en una tupla
        datos = cursor.fetchall()
        #cierro la conexion a bd
        cursor.close()
        #obtengo el primer arreglo de la tupla 
        producto = datos[0]
        #creo un diccionario con los datos para luego mandarlo como json con json.dumps
        res = {'nombre':producto[1], 'precio':str(producto[4]) ,'descripcion':producto[12],'imagen':producto[8]}
        #retorno el diccionario creado
    return json.dumps(res)
    
@app.route('/addLike', methods=['GET'])
def addLike():
    if request.method == 'GET':
        likes = request.args.get('likes')
        idProducto = request.args.get('id')
        product = Producto(request.form)
        product.addLikes(g.cur, idProducto, 1)
        product.obtenerProduct(g.cur, idProducto)
        return json.dumps(product.product)
    
@app.route('/mostrarTiendas', methods=['POST'])
def mostrarTiendas():
    if request.method == 'POST':
        tienda = []
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT idTienda,nombre FROM tienda")   
        resultados = cursor.fetchall()
        cursor.close()
        #Recorro las tuplas devueltas por la consulta
        for item in range(len(resultados)):
            #obtengo tupla por tupla
            t = resultados[item]
            #agrego cada item de cada tupla a diccionario
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
    

@app.route('/guardar_tienda',methods=['POST'])
def guardar_tienda():
    tienda = Tienda(request.form)
    if request.method == 'POST' and tienda.validate():
        tienda.guardar(g.cur)
    return redirect(url_for('ingresos'))
    
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