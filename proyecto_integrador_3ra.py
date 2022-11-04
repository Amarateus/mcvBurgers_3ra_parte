import tkinter as tk
from tkinter import messagebox
import time
import sqlite3
import requests
import sys

###########################################

def validar(dato):
	try:
		dato = int(dato)
		return dato
	except ValueError:
		return -1

def vaciar_entrys():
    # No borro el nombre del encargado
    entry_simple.delete(0, tk.END)
    entry_doble.delete(0, tk.END)
    entry_triple.delete(0, tk.END)
    entry_postre.delete(0, tk.END)
    entry_cliente.delete(0, tk.END)

def cancelar_pedido():
    respuesta = messagebox.askyesno(title="Pregunta", message="¿Desea cancelar el pedido?")
    if respuesta:
        vaciar_entrys()


def cotizar():
    try:
        r = requests.get("https://api-dolar-argentina.herokuapp.com/api/dolaroficial")
        valor = r.json()["venta"]
        valor = round(float(valor))
        return valor
    except:
        messagebox.showerror(title="Error grave", message="Sin internet para cotizar. Terminado")
        sys.exit()


def guardar_venta(pedido):
    datos = tuple(pedido)
    conn = sqlite3.connect("comercio.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ventas VALUES (null, ?, ?, ?, ?, ?, ?, ?)", datos)
    except sqlite3.OperationalError:
        cursor.execute("""CREATE TABLE ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha TEXT,
            combo_simple INT,
            combo_doble INT,
            combo_triple INT,
            postre INT,
            total REAL
        )""")

        cursor.execute("INSERT INTO ventas VALUES (null, ?, ?, ?, ?, ?, ?, ?)", datos)
    conn.commit()
    conn.close()
    

def guardar_encargado(encargado):
    datos_ingreso = (encargado["nombre"], encargado["ingreso"], "IN", encargado["facturado"])
    datos_egreso = (encargado["nombre"], encargado["egreso"], "OUT", encargado["facturado"])
    conn = sqlite3.connect("comercio.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO registros VALUES (null, ?, ?, ?, ?)", datos_ingreso)
        cursor.execute("INSERT INTO registros VALUES (null, ?, ?, ?, ?)", datos_egreso)
    except sqlite3.OperationalError:
        cursor.execute("""CREATE TABLE registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            fecha TEXT,
            evento TEXT,
            caja REAL
        )""")

        cursor.execute("INSERT INTO registros VALUES (null, ?, ?, ?, ?)", datos_ingreso)
        cursor.execute("INSERT INTO registros VALUES (null, ?, ?, ?, ?)", datos_egreso)
    conn.commit()
    conn.close()

def pedir():
    cant_simple = validar(entry_simple.get())
    cant_doble = validar(entry_doble.get())
    cant_triple = validar(entry_triple.get())
    cant_postre = validar(entry_postre.get())
    if cant_simple >= 0 and cant_doble >= 0 and cant_triple >= 0 and cant_postre >= 0:
        nombre_cliente = entry_cliente.get()
        nombre_encargado = entry_encargado.get()
        if nombre_cliente and nombre_encargado:       
            valor_dolar = cotizar()
            fecha = time.asctime()
            total_pedido = valor_dolar * (precios["combo_simple"] * cant_simple + precios["combo_doble"] * cant_doble + precios["combo_triple"] * cant_triple + precios["postre"] * cant_postre)
            messagebox.askyesno(title="Confirmar pedido", message=f"Total: ${total_pedido}\n ¿Confirmar pedido?")
            pedido = [nombre_cliente, fecha, cant_simple, cant_doble, cant_triple, cant_postre, total_pedido]
            guardar_venta(pedido)
            messagebox.showinfo(title="Guardar", message="¡Pedido guardado con exito!")
            vaciar_entrys()
            if nombre_encargado != datos_encargado["nombre"] and datos_encargado["egreso"] == "":
                datos_encargado["nombre"] = nombre_encargado
                datos_encargado["egreso"] = "Sin fecha"
                datos_encargado["facturado"] += total_pedido
            elif nombre_encargado == datos_encargado["nombre"]:
                datos_encargado["facturado"] += total_pedido
            else:
                datos_encargado["egreso"] = fecha
                guardar_encargado(datos_encargado)
                datos_encargado["nombre"] = nombre_encargado
                datos_encargado["ingreso"] = fecha
                datos_encargado["facturado"] = 0
                datos_encargado["facturado"] += total_pedido
        else:
            messagebox.showwarning(title="Advertencia", message="Advertencia, ingrese bien los datos")
    else:
        messagebox.showwarning(title="Advertencia", message="Advertencia, ingrese bien los datos")


def salir():
    respuesta = messagebox.askyesno(title="Salir", message="¿Desea salir del programa?")
    if respuesta:
        datos_encargado["egreso"] = time.asctime()
        guardar_encargado(datos_encargado)    
        sys.exit()         




##########################################################################

precios = {"combo_simple":5, "combo_doble":6, "combo_triple":7, "postre":2}
datos_encargado = {"nombre":"", "ingreso":time.asctime(), "egreso":"", "facturado":0}

########### VENTANA #################

ventana_principal = tk.Tk()
ventana_principal.title("MCV Burgers")
ventana_principal.config(width=500, height=500)

########## LABELS ###########

label_pedidos = tk.Label(text="------ Pedidos ------")
label_pedidos.place(relx=0.5, y=25, anchor="center")
label_encargado = tk.Label(text="Nombre encargado:")
label_encargado.place(x=50, y=70)
label_simple = tk.Label(text="Combo simple cantidad:")
label_simple.place(x=50, y=120)
label_doble = tk.Label(text="Combo doble cantidad:")
label_doble.place(x=50, y=170)
label_triple = tk.Label(text="Combo triple cantidad:")
label_triple.place(x=50, y=220)
label_postre = tk.Label(text="Postre cantidad:")
label_postre.place(x=50, y=270)
label_cliente = tk.Label(text="Nombre cliente:")
label_cliente.place(x=50, y=320)

############# ENTRYS ############

entry_encargado = tk.Entry()
entry_encargado.place(x=300, y=70)
entry_simple = tk.Entry()
entry_simple.place(x=300, y=120)
entry_doble = tk.Entry()
entry_doble.place(x=300, y=170)
entry_triple = tk.Entry()
entry_triple.place(x=300, y=220)
entry_postre = tk.Entry()
entry_postre.place(x=300, y=270)
entry_cliente = tk.Entry()
entry_cliente.place(x=300, y=320)

########## BOTTONS #############

boton_salir = tk.Button(text="Salir", command=salir)
boton_salir.place(x=30, y=405, width=100, height=50)
boton_cancelar = tk.Button(text="Cancelar pedido", command=cancelar_pedido)
boton_cancelar.place(relx=0.5, anchor="center", y=430, width=100, height=50)
boton_confirmar = tk.Button(text="Confirmar pedido", command=pedir)
boton_confirmar.place(x=360, y=405, width=100, height=50)

########### LOOP ###############

ventana_principal.mainloop()