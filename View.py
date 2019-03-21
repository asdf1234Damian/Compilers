import threading
from tkinter import Tk,Frame,Button,Label,Entry,Listbox,END,ACTIVE
import AFND
import Image

# ----------------------------------------------Guarda el autómata seleccionado
automats= {}
currAutomat = None

# ---------------------------------------------------------Crea botones iguales
class myButton:
    def __init__(self, texto, frame):
        self.texto = texto
        self.button = Button(frame, text=texto, fg="white", bg="#496ba0",
        activeforeground="#f2f4f7", activebackground="#354154", relief='flat', width=25, height=1,
        font=("Helvetica", 16))
        self.button.pack()

# Coloca el frame seleccionado hasta el frente
def raise_frame(frame):
    frame.tkraise()
    err_lbl_Operacion.config(text = "")
    err_lbl_CrearBasico.config(text = "")
    err_lbl_VerGrafo.config(text = "")

#Funcion para cambiar la imagen mostrada
def cambiar_Imagen(id):
    global currAutomat
    if id in automats.keys():
        automats[id].plot(id)
        Image.ImageWidow(bottomFrame, path='images/'+id+'.png')
        err_lbl_VerGrafo.config(text = '')
        #lbl_Sel.config(text=id)
        currAutomat = id
    else:
        err_lbl_VerGrafo.config(text = 'No existe autómata con esa ID')

# Al crear un nuevo autómata, recibe el símbolo del área de texto del formulario

def basico(id,exp):
    if (len(exp)):
        if id in automats.keys():
            err_lbl_CrearBasico.config(text = 'Ya existe un autómata')
        else:
            automats[id] = AFND.Automata(exp)
            cambiar_Imagen(id)
    else:
        err_lbl_CrearBasico.config(text = 'Ingrese un símbolo válido')

def opcional():
    global currAutomat
    if currAutomat:
        automats[currAutomat].opcional()
        cambiar_Imagen(currAutomat)
    else:
        err_lbl_CrearBasico.config(text='Primero cree un automata')

def unirM(seleccion):
    global currAutomat
    if len(seleccion)>1:
        keys = ['F'+str(i+1) for i in list(seleccion)]
        #seleccion = []
        seleccion = set()
        if  not currAutomat in keys:
            currAutomat = keys[0]
        for k in keys:
            if k != currAutomat and k in automats.keys():
                seleccion[k] = automats[k]
        if len(seleccion):
            automats[currAutomat].unirM(seleccion)
            cambiar_Imagen(currAutomat)
        else:
             mainAutomata = keys[0]
             keys.remove(keys[0])
        automatasAUnir = []
        for k in keys:
            if k in automats.keys():
                automatasAUnir.append(automats[k])
        automats[mainAutomata].unirM(automatasAUnir)
        currAutomat = mainAutomata
        cambiar_Imagen(currAutomat)
    else:
        err_lbl_Operacion.config(text='Seleccion al menos 2 automatas')

def cerrPos():
    global currAutomat
    if currAutomat:
        automats[currAutomat].cerradura_positiva()
        cambiar_Imagen(currAutomat)
    else:
        err_lbl_Operacion.config(text='Primero cree un automata')

def cerrKle():
    global currAutomat
    if currAutomat:
        automats[currAutomat].cerradura_kleene()
        cambiar_Imagen(currAutomat)
    else:
        err_lbl_Operacion.config(text='Primero cree un automata')

def Pertenece(sigma):
    global currAutomat
    if not len(sigma):
        sigma=AFND.EPS
    if currAutomat:
        if automats[currAutomat].pertenece(sigma):
            lbl_Pertenece.config(text='Cadena valida')
        else:
            lbl_Pertenece.config(text='Cadena NO valida')
        err_lbl_Operacion.config(text='')
    else:
        err_lbl_Operacion.config(text='Primero cree un automata')


def CrearTabla(sigma):
	global currAutomat
	if currAutomat:
		path = str(currAutomat)+'.txt';
		automats[currAutomat].conversion_A_Archivo(path)
		#automats[currAutomat].crearDeTablas(currAutomat+'.txt')
	else:
		err_lbl_Operacion.config(text = "Primero cree un automata")
    
def Union(f2):
    global currAutomat
    if f2 and currAutomat:
        automats[currAutomat].unir(automats[f2])
        cambiar_Imagen(currAutomat)
        del automats[f2]
    else:
        err_lbl_Operacion.config(text='')


def Operaciones(operacion, f2 = None, sigma=''):
    global currAutomat
    if f2:
        if f2 in automats.keys():
            if currAutomat == f2:
                err_lbl_Operacion.config(text='Seleccione otro autómata')
            else:
                if operacion == 'Union':
                    automats[currAutomat].unir(automats[f2])
                    del automats[f2]
                elif operacion == 'Concat':
                    automats[currAutomat].concat(automats[f2])
                    del automats[f2]
                else:
                    print('Error no existe operacion', operacion)
                cambiar_Imagen(currAutomat)
                err_lbl_Operacion.config(text = '')
        else:
            err_lbl_Operacion.config(text='No existe ese autómata')
    else:
        err_lbl_Operacion.config(text = 'No existe ese autómata')

# ----------------------------------------------------------------Crear ventana
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("AFND")
# -------------------------------------------------------------Menú de opciones
container = Frame(root, bg="#496ba0",height='20')
container.pack(side='left', fill='both')

menuPrincipal   = Frame(container)
menuCrearBasico = Frame(container)
menuOperacion   = Frame(container)
menuVerGrafo    = Frame(container)
menuCrearTabla   = Frame(container)

for frame in (menuPrincipal, menuCrearBasico, menuOperacion, menuVerGrafo):
    frame.grid(row=0, column=0, sticky='news')

# -----------------------------------------------------------------------Imagen
filename = 'resources/Portada.png'
bottomFrame = Frame(root, bg='black')
bottomFrame.pack(side='left', fill='both', expand=1)
Image.ImageWidow(bottomFrame, path=filename)

# ---------------------------------------------------------------Menu Principal
menuPrincipal.config(bg="#496ba0")
lbl_ElegirOperacionP = Label(menuPrincipal, text='Seleccionar opción', fg='white',
                            bg="#354154", font=("Helvetica", 16))
lbl_ElegirOperacionP.pack(fill='x')

bttn_CrearAutómata = myButton("Crear Autómata", menuPrincipal)
bttn_CrearAutómata.button.config(command=lambda:raise_frame(menuCrearBasico))

bttn_ElegirOperacion = myButton("Elegir operacion", menuPrincipal)
bttn_ElegirOperacion.button.config(command=lambda: raise_frame(menuOperacion))

bttn_VerGrafo = myButton("Ver Otro Grafo", menuPrincipal)
bttn_VerGrafo.button.config(command=lambda:raise_frame(menuVerGrafo))

# ------------------------------------------------------------Menu Crear Basico
menuCrearBasico.config(bg="#496ba0")
lbl_CrearBasico = Label(menuCrearBasico, text='Crear autómata básico',
                        fg='white', bg="#354154", font=("Helvetica", 16))
lbl_CrearBasico.pack(fill='x')

lbl_InsertSimb = Label(menuCrearBasico, text='Inserte su símbolo',
                        fg='white', bg="#354154", font=("Helvetica", 16))
lbl_InsertSimb.pack(fill='x', pady = ( 10, 10 ))

inExp = Entry(menuCrearBasico, font=("Helvetica", 16), width=4)
inExp.pack(pady = (0, 10))

lbl_SelAut = Label(menuCrearBasico, text='Seleccione una opción',
                        fg='white', bg="#354154", font=("Helvetica", 16))
lbl_SelAut.pack(fill = "x", pady = (0, 10))

lstbox_Crear = Listbox(menuCrearBasico, width=25, height=4, font=("Helvetica", 16))
lstbox_Crear.pack(pady = (0,10))

for item in ["F1", "F2", "F3", "F4"]:
    lstbox_Crear.insert(END, item)
lstbox_Crear.select_set(1)

bttn_CrearBasico = myButton("Seleccionar", menuCrearBasico)
bttn_CrearBasico.button.config(command=lambda: basico(lstbox_Crear.get(ACTIVE),inExp.get()))

bttn_back_CrearBasico = myButton("Volver al menú", menuCrearBasico)
bttn_back_CrearBasico.button.config(command=lambda: raise_frame(menuPrincipal), bg = "#39547f")

err_lbl_CrearBasico = Label(menuCrearBasico, text=" ", fg="red", bg="#496ba0",
font=("Helvetica", 16))
err_lbl_CrearBasico.pack()

# -----------------------------------------------------------------------Menu Operaciones
menuOperacion.config(bg="#496ba0")
lbl_ElegirOperacionO = Label(menuOperacion, text='Elegir operacion', fg='white',
                 bg="#354154", font=("Helvetica", 16))
lbl_ElegirOperacionO.pack(fill='x')
lbl_Op_Unarias = Label(menuOperacion, text='Operaciones Unarias', fg='white',
                 bg="#354154", font=("Helvetica", 16))
lbl_Op_Unarias.pack(fill='x', pady=(10,0))

bttn_Opcional = myButton("Opcional", menuOperacion)
bttn_Opcional.button.config(command=lambda:opcional())

bttn_Cerr_Pos = myButton("Cerradura Positiva", menuOperacion)
bttn_Cerr_Pos.button.config(command=lambda:cerrPos())

bttn_Cerr_Pos = myButton("Cerradura de Kleene", menuOperacion)
bttn_Cerr_Pos.button.config(command=lambda:cerrKle())

lbl_Op_Binarias = Label(menuOperacion, text='Operaciones Binarias', fg='white',
                 bg="#354154", font=("Helvetica", 16))
lbl_Op_Binarias.pack(fill='x')

lstbox_Binarias = Listbox(menuOperacion, height=4, font=("Helvetica", 16), selectmode='multiple')
lstbox_Binarias.pack(fill='x')

for item in ["F1", "F2", "F3", "F4"]:
    lstbox_Binarias.insert(END, item)
lstbox_Binarias.select_set(0)

bttn_Union = myButton("Union", menuOperacion)
bttn_Union.button.config(command=lambda:Operaciones('Union',lstbox_Binarias.get(ACTIVE)))

bttn_Concat = myButton("Concatenar", menuOperacion)
bttn_Concat.button.config(command=lambda:Operaciones('Concat',lstbox_Binarias.get(ACTIVE)))

bttn_UnirM = myButton("Unir selecciones", menuOperacion)
bttn_UnirM.button.config(command=lambda: unirM(lstbox_Binarias.curselection()))

lbl_Pertenece = Label(menuOperacion, text='Analiza una cadena', fg='white',
                        bg="#354154", font=("Helvetica", 16))
lbl_Pertenece.pack(fill='x')

in_Sigma = Entry(menuOperacion, font=("Helvetica", 16), width=4)
in_Sigma.pack(fill = "x")

bttn_Cerr_Pos = myButton("Pertenece", menuOperacion)
bttn_Cerr_Pos.button.config(command=lambda: Pertenece(sigma=in_Sigma.get()))

bttn_CrearTabla = myButton("Crear tabla AFD", menuOperacion)
bttn_CrearTabla.button.config(command=lambda: CrearTabla(sigma = in_Sigma.get()))

bttn_back_Operacion = myButton("Volver al menú", menuOperacion)
bttn_back_Operacion.button.config(command=lambda: raise_frame(menuPrincipal), bg = "#39547f" )

err_lbl_Operacion = Label(menuOperacion, text=" ", fg="red", bg="#496ba0",
font=("Helvetica", 16))
err_lbl_Operacion.pack()
# ---------------Ver Otro Grafo--------------------------
menuVerGrafo.config(bg="#496ba0")
label_VerGrafo = Label(menuVerGrafo, text='Eliga un grafo', fg='white',
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
bttn_back_VerGrafo.button.config(command=lambda:raise_frame(menuPrincipal), bg = "#39547f")

err_lbl_VerGrafo = Label(menuVerGrafo, text=" ", fg="red", bg="#496ba0",
font=("Helvetica", 16))
err_lbl_VerGrafo.pack()



# --------------------------------------------------------
raise_frame(menuPrincipal)
"""basico('F1', 'D')
cerrPos()
basico('F2', 'D')
cerrPos()
basico('F3', '.')
automats['F3'].concat(automats['F2'])
opcional()
automats['F3'].concat(automats['F2'])"""
root.mainloop()
#AFND.delImages()
