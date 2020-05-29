from flask import Flask, render_template, request, redirect, url_for, jsonify, g
from Pcool import app
from Pcool.conexiondb import mysql
from Pcool.producto import Producto
from Pcool.categorias import Categoria
from Pcool.marca import Marca
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

@app.route('/')
def inicio():
     return render_template('inicio.html')

@app.route('/login')
def loginPropietarios():
    return render_template('login.html')

@app.route('/registro')
def registro():
    return render_template('Register.html')

@app.route('/validarSesion')
def validarSesion():
    nombre = request.args.get('nombre')
    password = request.args.get('password')
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    return render_template('ingresos.html')

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

@app.route('/ingresos', methods=['GET', 'POST'])
def ingresos():
    formProducto = Producto(request.form)
    formProducto.listaCategoria(g.cur)
    formCategoria = Categoria(request.form)
    formMarca = Marca(request.form)
    formProducto.listaMarca(g.cur)
    return render_template('ingresos.html',datos=formProducto, categorias=formCategoria, marca=formMarca)

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

#Metodo para guardar productos
@app.route('/guardar_producto', methods=['POST'])
def guardar_producto():
    p = Producto(request.form)
    p.guardar(g.cur)
    '''if request.method == 'POST' and p.validate():
        p.guardar(g.cur)'''
    return redirect(url_for('ingresos'))
    
@app.route('/mostrarModal')
def mostrarModal():
    # obtengo el id de producto en idP 
    idP = request.args.get('idP')
    #conexion ala base de datos
    conn = mysql.connect()
    cursor = conn.cursor()
    #ejecuto la consulta
    cursor.execute("SELECT * FROM producto WHERE idProucto='{}'".format(idP))
    #obtengo los datos en una tupla
    datos = cursor.fetchall()
    #cierro la conexion a bd
    cursor.close()
    #obtengo el primer arreglo de la tupla 
    producto = datos[0]
    #creo un diccionario con los datos para luego mandarlo como json con json.dumps
    res = {'nombre':producto[1], 'descripcion':producto[2], 'precio': producto[3], 'imagen':producto[5]}
    #retorno el diccionario creado
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