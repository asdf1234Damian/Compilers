import threading
from tkinter import *# python 3
import AFND
import Image

# ----------------------------------------------Guarda el autómata seleccionado
automats= {}
currAutomat = None

class myButton:
	def __init__( self, texto, frame ):
		self.texto = texto
		self.button = Button( frame, text = texto, fg = "white", bg = "#496ba0", activeforeground = "#f2f4f7", activebackground = "#354154", relief = 'flat', width = 25, height = 2, font = ( "Helvetica", 16 ) )
		self.button.pack()
	
	def operacion( operacion, simbolo ):
		def callback():
			if operacion == "Opcional":
				print(operacion)
			if operacion == "Cerradura positiva":
				print(operacion)
			if operacion == "Cerradura de Kleene":
				print(operacion)
		t = threading.Thread(target=callback)
		t.start()
#Coloca el frame seleccionado hasta el frente
def raise_frame(frame):
    frame.tkraise()

#Al crear un nuevo autómata, recibe el símbolo del área de texto del formulario
def valores(simbolo):
	#Obtiene el aultómata seleccionado de la lista
	value = [listbox.get(i) for i in listbox.curselection()]
	#Verifica que se seleccionó un autómata
	if value:
		valor = value[0]
		sim = simbolo.get()
		labelM_F1.config( text = "  ")
		#
		if len(sim) > 0 :
			f = AFND.Graph(valor, sim)
			f.basico(sim)
			f.plot()
			labelM_F1.config( text = "  ")
			filename = 'resources\Base.jpg'  
		else:
			labelM_F1.config( text = "Ingrese un símbolo válido")
	else:
		labelM_F1.config( text = "Seleccione un autómata")


#------------------Crear ventana
            filename = 'resources/' + valor + '.png'
            filename = 'images/' + valor + '.png'
            Image.ImageWidow(bottomFrame, path=filename)
#Funcion para cambiar la imagen mostrada
def cambiar_Imagen(id):
    global currAutomat
    if id in automats.keys():
        automats[id].plot()
        Image.ImageWidow(bottomFrame, path='images/'+id+'.png')
        err_lbl_VerGrafo.config(text = '')
        currAutomat = id
    else:
        err_lbl_VerGrafo.config(text = 'No existe un autómata con esa ID')
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+%d+0" % (w/2, h, w/2))
root.title("AFND")
# -------------------------------------------------------------Menú de opciones
container = Frame(root, bg="#496ba0")
container.pack(side='left', fill='both')

menuPrincipal   = Frame(container)
menuCrearBasico = Frame(container)
menuOperacion    = Frame(container)
menuVerGrafo    = Frame(container)

for frame in (menuPrincipal, menuCrearBasico, menuOperacion, menuVerGrafo):
    frame.grid(row=0, column=0, sticky='news')

# -----------------------------------------------------------------------Imagen
filename = 'resources/Portada.jpg'
bottomFrame = Frame(root, bg='black')
bottomFrame.pack(side='left', fill='both', expand=1)
Image.ImageWidow(bottomFrame, path=filename)


# ---------------------------------------------------------------Menu Principal
menuPrincipal.config(bg="#496ba0")
lbl_ElegirOperacionP = Label(menuPrincipal, text='Elegir operacion', fg='white',
                            bg="#354154", font=("Helvetica", 16))
lbl_ElegirOperacionP.pack(fill='x')

bttn_CrearAutómata = myButton("Crear Autómata", menuPrincipal)
bttn_CrearAutómata.button.config(command=lambda:raise_frame(menuCrearBasico))

bttn_ElegirOperacion = myButton("Elegir operacion", menuPrincipal)
bttn_ElegirOperacion.button.config(command=lambda: raise_frame(menuOperacion))

bttn_VerGrafo = myButton("Ver Otro Grafo", menuPrincipal)
bttn_VerGrafo.button.config(command=lambda:raise_frame(menuVerGrafo))

#------------------Menu---------------------------------
menu.config(bg = "#496ba0")
label_M = Label( menu, text = 'Elegir operacion', fg = 'white', bg ="#354154" , font = ( "Helvetica", 16 ) )
label_M.pack( fill = 'x' )
# ------------------------------------------------------------Menu Crear Basico
menuCrearBasico.config(bg="#496ba0")
lbl_CrearBasico = Label(menuCrearBasico, text='Crear autómata básico',
                        fg='white', bg="#354154", font=("Helvetica", 16))
lbl_CrearBasico.pack(fill='x')

lbl_InsertSimb = Label(menuCrearBasico, text='Inserte su símbolo',
                        fg='white', bg="#354154", font=("Helvetica", 16))
lbl_InsertSimb.pack(fill='x')

inSimbol = Entry(menuCrearBasico, font=("Helvetica", 16), width=4)
inSimbol.pack()

lstbox_Crear = Listbox(menuCrearBasico, width=25, height=4, font=("Helvetica", 16))
lstbox_Crear.pack()

for item in ["F1", "F2", "F3", "F4"]:
    lstbox_Crear.insert(END, item)
lstbox_Crear.select_set(1)

bttn_CrearBasico = myButton("Seleccionar", menuCrearBasico)
bttn_CrearBasico.button.config(command=lambda: basico(lstbox_Crear.get(ACTIVE),inSimbol.get()))
#TODO cambiar funcion valores

bttn_back_CrearBasico = myButton("Volver al menú", menuCrearBasico)
bttn_back_CrearBasico.button.config(command=lambda: raise_frame(menuPrincipal))

err_lbl_CrearBasico = Label(menuCrearBasico, text=" ", fg="red", bg="#496ba0",
font=("Helvetica", 16))
err_lbl_CrearBasico.pack()

label_F1.pack( fill = 'x' )

listbox = Listbox( f1, width = 25, height = 4, font = ( "Helvetica", 16 ) )
listbox.pack()

for item in ["F1", "F2", "F3", "F4"]:
    listbox.insert(END, item)


buttonLB = myButton( "Seleccionar", f1)
buttonLB.button.config( command = lambda:valores(simbol) )

buttonF1M = myButton( "Volver al menú", f1 )
buttonF1M.button.config( command = lambda:raise_frame(menu) )
# ---------------Ver Otro Grafo--------------------------
menuVerGrafo.config(bg="#496ba0")
label_VerGrafo = Label(menuVerGrafo, text='Elega un grafo', fg='white',
                 bg="#354154", font=("Helvetica", 16))
label_VerGrafo.pack(fill='x')

lstboxVG = Listbox(menuVerGrafo, width=25, height=4, font=("Helvetica", 16))
lstboxVG.pack()

for item in ["F1", "F2", "F3", "F4"]:
    lstboxVG.insert(END, item)
lstboxVG.select_set(0)

buttonVer = myButton("Ver", menuVerGrafo)
buttonVer.button.config(command=lambda:cambiar_Imagen(lstboxVG.get(ACTIVE)))

bttn_back_VerGrafo = myButton("Volver al menú", menuVerGrafo)
bttn_back_VerGrafo.button.config(command=lambda:raise_frame(menuPrincipal))

err_lbl_VerGrafo = Label(menuVerGrafo, text=" ", fg="red", bg="#496ba0",
font=("Helvetica", 16))
err_lbl_VerGrafo.pack()

# --------------------------------------------------------
raise_frame(menuPrincipal)
root.mainloop()
