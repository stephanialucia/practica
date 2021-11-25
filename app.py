from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pymysql
import requests
from bs4 import BeautifulSoup 
from lxml import etree 
from flask_cors import CORS

app=Flask(__name__)
CORS(app)

app.secret_key="mysecretkey"

app.secret_key = "191132"

@app.route("/")
def login():
	return render_template("login.html")

@app.route("/login", methods=["POST"])
def inicio():
	if request.method=="POST":
		email=request.form["email"]
		password=request.form["password"]
		session["user"]=email
		return redirect(url_for("index"))
	else:
		return "bad request"

@app.route("/index")
def index():
	conexion = pymysql.connect(host="localhost", user="root", password="191132", database="apidolcerossi")
	cur=conexion.cursor()
	cur.execute("SELECT*FROM inventario")
	data=cur.fetchall()
	return render_template("index.html", inventario=data)


@app.route("/add_inventarios", methods=["POST"])
def add_inventarios():
	if request.method=="POST":
		productos=request.form["productos"]
		preciodolar=request.form["preciodolar"]
		preciobs=request.form["preciobs"]
		stock=request.form["stock"]
		conexion = pymysql.connect(host="localhost", user="root", password="191132", database="apidolcerossi")
		cur=conexion.cursor()
		cur.execute("INSERT INTO inventario (productos, preciodolar, preciobs, stock) VALUES (%s, %s, %s, %s)", (productos, preciodolar, preciobs, stock))
		conexion.commit()
		flash("Producto agregado al inventario")
		return redirect(url_for("index"))

@app.route("/edit/<idinventarios>")
def get_inventarios(idinventarios):
	conexion = pymysql.connect(host="localhost", user="root", password="191132", database="apidolcerossi")
	cur=conexion.cursor()
	cur.execute("SELECT*FROM inventario WHERE id=%s", (idinventarios))
	data=cur.fetchall()
	return render_template("edit-contact.html", inventarios=data[0])

@app.route("/update/<id>", methods=["POST"])
def update_contact(id):
	if request.method=="POST":
		productos=request.form["productos"]
		preciodolar=request.form["preciodolar"]
		preciobs=request.form["preciobs"]
		stock=request.form["stock"]
	conexion = pymysql.connect(host="localhost", user="root", password="191132", database="apidolcerossi")
	cur=conexion.cursor()
	cur.execute("""
		UPDATE inventario
		SET productos=%s,
			preciodolar=%s,
			preciobs=%s,
			stock=%s
		WHERE id=%s
	""", (productos, preciodolar,preciobs, stock, id))
	conexion.commit()
	flash("Inventario actualizado")
	return redirect(url_for("index"))

	

@app.route("/delete/<string:id>")
def delete_inventarios(id):
	conexion = pymysql.connect(host="localhost", user="root", password="191132", database="apidolcerossi")
	cur=conexion.cursor()
	cur.execute("DELETE FROM inventario WHERE id={0}" .format(id))
	conexion.commit()
	flash("producto eliminado")
	return redirect(url_for("index"))

@app.route("/dolar")
def dolar():
	URL = "http://www.bcv.org.ve/"
	webpage = requests.get(URL) 
	soup = BeautifulSoup(webpage.content, "html.parser")
	dom = etree.HTML(str(soup)) 
	dolar = dom.xpath('//*[@id="dolar"]/div/div/div[2]/strong')[0].text
	print(dolar)
	return jsonify(dolar = str(dolar))
	

@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for("login"))

if __name__=="__main__":
	app.run(debug=True,port=3000)

#@app.route("/add_clientes", methods=["POST"])
#def add_clientes():
	#if request.method=="POST":
		#cliente=request.form["cliente"]
		#documentoid=request.form["documentoid"]
		#telefono=request.form["telefono"]
		#conexion = pymysql.connect(host="localhost", user="root", password="191132", database="apidolcerossi")
		#cur=conexion.cursor()
		#cur.execute("INSERT INTO clientes (cliente, documentoid, telefono) VALUES (%s, %s, %s)", (cliente, documentoid, telefono))
		#conexion.commit()
		#flash("Venta generada")
		#return render_template("index2.html")

#@app.route("/index2")
#def select():
		#conexion = pymysql.connect(host="localhost", user="root", password="191132", database="apidolcerossi")
		#cur=conexion.cursor()
		#cur.execute("SELECT*FROM inventario")
		#resultados= cur.fetchall()
		#ids=[]
		#nombres=[]
		#for fila in resultados:
			#ids.append(fila[0])	
			#nombres.append(fila[1])
		#print(ids,nombres)
		#return render_template("index2.html", nombres = nombres, ids = ids)

#@app.route("/dolar")
#def dolar():
	#URL = "http://www.bcv.org.ve/"
	#webpage = requests.get(URL) 
	#soup = BeautifulSoup(webpage.content, "html.parser")
	#dom = etree.HTML(str(soup)) 
	#dolar = dom.xpath('//*[@id="dolar"]/div/div/div[2]/strong')[0].text
	#print(dolar)
	#return jsonify(dolar = str(dolar))
	#

