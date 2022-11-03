import tkinter as tk
from tkinter import ttk

###########################################




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

boton_salir = tk.Button(text="Salir")
boton_salir.place(x=30, y=405, width=100, height=50)
boton_cancelar = tk.Button(text="Cancelar pedido")
boton_cancelar.place(relx=0.5, anchor="center", y=430, width=100, height=50)
boton_confirmar = tk.Button(text="Confirmar pedido")
boton_confirmar.place(x=360, y=405, width=100, height=50)

#################################

ventana_principal.mainloop()