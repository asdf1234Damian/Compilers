import threading
from tkinter import *# python 3
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
        activeforeground="#f2f4f7", activebackground="#354154", relief='flat', width=25, height=2,
        font=("Helvetica", 16))
        self.button.pack()

# Coloca el frame seleccionado hasta el frente
def raise_frame(frame):
    frame.tkraise()

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


# Al crear un nuevo autómata, recibe el símbolo del área de texto del formulario
def basico(id,simbolo):
    if len(simbolo)>1:
        err_lbl_CrearBasico.config(text = 'Ingrese un símbolo válido')
    else:
        if id in automats.keys():
            err_lbl_CrearBasico.config(text = 'Ya existe un autómata')
        else:
            automats[id] = AFND.Graph(id,simbolo)
            automats[id].basico(simbolo)
            cambiar_Imagen(id)

def Operaciones(operacion, f2 = None):
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
        if currAutomat:
            if operacion == 'Opcional':
                automats[currAutomat].opcional()
            elif operacion == 'CerrPos':
                automats[currAutomat].cerradura_positiva()
            elif operacion == 'CerrKle':
                automats[currAutomat].cerradura_kleene()
            else:
                print('Error no existe operacion', operacion)
            cambiar_Imagen(currAutomat)
            err_lbl_Operacion.config(text = '')
        else:
            err_lbl_Operacion.config(text = 'No existe ese autómata')

# ----------------------------------------------------------------Crear ventana
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

# -----------------------------------------------------------------------Menu Operaciones
menuOperacion.config(bg="#496ba0")
lbl_ElegirOperacionO = Label(menuOperacion, text='Elegir operacion', fg='white',
                 bg="#354154", font=("Helvetica", 16))
lbl_ElegirOperacionO.pack(fill='x')
lbl_Op_Unarias = Label(menuOperacion, text='Operaciones Unarias', fg='white',
                 bg="#354154", font=("Helvetica", 16))
lbl_Op_Unarias.pack(fill='x')

bttn_Opcional = myButton("Opcional", menuOperacion)
bttn_Opcional.button.config(command=lambda:Operaciones('Opcional'))

bttn_Cerr_Pos = myButton("Cerradura Positiva", menuOperacion)
bttn_Cerr_Pos.button.config(command=lambda:Operaciones('CerrPos'))

bttn_Cerr_Pos = myButton("Cerradura de Kleene", menuOperacion)
bttn_Cerr_Pos.button.config(command=lambda:Operaciones('CerrKle'))

lbl_Op_Binarias = Label(menuOperacion, text='Operaciones Binarias', fg='white',
                 bg="#354154", font=("Helvetica", 16))
lbl_Op_Binarias.pack(fill='x')

lstbox_Binarias = Listbox(menuOperacion, width=25, height=4, font=("Helvetica", 16))
lstbox_Binarias.pack()

for item in ["F1", "F2", "F3", "F4"]:
    lstbox_Binarias.insert(END, item)
lstbox_Binarias.select_set(0)

bttn_Union = myButton("Union", menuOperacion)
bttn_Union.button.config(command=lambda:Operaciones('Union',lstbox_Binarias.get(ACTIVE)))

bttn_Concat = myButton("Concatenar", menuOperacion)
bttn_Concat.button.config(command=lambda:Operaciones('Concat',lstbox_Binarias.get(ACTIVE)))

bttn_back_Operacion = myButton("Volver al menú", menuOperacion)
bttn_back_Operacion.button.config(command=lambda: raise_frame(menuPrincipal))

err_lbl_Operacion = Label(menuOperacion, text=" ", fg="red", bg="#496ba0",
font=("Helvetica", 16))
err_lbl_Operacion.pack()
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
