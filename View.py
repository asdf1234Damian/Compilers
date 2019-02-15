import threading
from tkinter import *               # python 3
#from tkinter import font  as tkfont 
import AFND
import Image
#Crea botones iguales
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
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title( "AFND" )

#-----menú de opciones
container = Frame( root, bg = "#496ba0")
container.pack( side = 'left', fill = 'both' )

menu = Frame(container)
f1 = Frame(container)
f2 = Frame(container)
f3 = Frame(container)
f4 = Frame(container)

for frame in (menu, f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

#----------Imagen
filename = 'resources\Portada.jpg'  

bottomFrame = Frame( root, bg = 'black' )
bottomFrame.pack( side = 'left', fill = 'both', expand = 1 )
app = Image.ImageWidow(bottomFrame, path=filename)


#------------------Menu---------------------------------
menu.config(bg = "#496ba0")
label_M = Label( menu, text = 'Elegir operacion', fg = 'white', bg ="#354154" , font = ( "Helvetica", 16 ) )
label_M.pack( fill = 'x' )

buttonF1 = myButton( "Crear Autómata", menu )
buttonF1.button.config( command = lambda:raise_frame(f1) )

buttonF2 = myButton( "Elegir operacion", menu )
buttonF2.button.config( command = lambda:raise_frame(f2) )

buttonF3 = myButton( "Volver al menú", menu )
buttonF3.button.config( command = lambda:raise_frame(f3) )


#------------------F2-----------------------------------
f1.config(bg = "#496ba0")
label_F1 = Label( f1, text = 'Crear autómata básico', fg = 'white', bg ="#354154" , font = ( "Helvetica", 16 ) )	
label2_F1 = Label( f1, text = 'Inserte su símbolo', fg = 'white', bg ="#354154" , font = ( "Helvetica", 16 ) )	
labelM_F1 = Label( f1, text = " ", fg = "red", bg = "#496ba0", font = ( "Helvetica", 16 ))

label2_F1.pack( fill = 'x' )

simbol = Entry(f1, font = ( "Helvetica", 16 ), width = 1)
simbol.pack()

label_F1.pack( fill = 'x' )

listbox = Listbox( f1, width = 25, height = 4, font = ( "Helvetica", 16 ) )
listbox.pack()

for item in ["F1", "F2", "F3", "F4"]:
    listbox.insert(END, item)


buttonLB = myButton( "Seleccionar", f1)
buttonLB.button.config( command = lambda:valores(simbol) )

buttonF1M = myButton( "Volver al menú", f1 )
buttonF1M.button.config( command = lambda:raise_frame(menu) )

labelM_F1.pack()

#------------------F1-----------------------------------
f2.config(bg = "#496ba0")
label_F2 = Label( f2, text = 'Elegir operacion', fg = 'white', bg ="#354154" , font = ( "Helvetica", 16 ) )	
label_F2.pack( fill = 'x' )
buttonO = myButton( "Opcional", f2)
buttonCP = myButton( "Cerradura positiva", f2)
buttonCK = myButton( "Cerradura de Kleene", f2)

buttonO.button.config(command = lambda:myButton.operacion( buttonO.texto, "a" ))
buttonCP.button.config(command = lambda:myButton.operacion( buttonCP.texto, "a" ))
buttonCK.button.config(command = lambda:myButton.operacion( buttonCK.texto, "a" ))

buttonF2M = myButton( "Volver al menú", f2 )
buttonF2M.button.config( command = lambda:raise_frame(menu) )

#--------------------------------------------------------
raise_frame(menu)
root.mainloop()
