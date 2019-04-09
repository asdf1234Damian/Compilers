from tkinter import Tk,Frame,Button,Label,Entry,Listbox,END,ACTIVE, Menu, ttk, messagebox
from Calculadora import calculadora
import AFND
import Image
import os.path
# -----------Guarda autómatas seleccionados-----#
automats= {}
cantidades = list()
currAutomat = None
optionLists = list()
global fram
class Operaciones:
	def basico(id,exp,frame):
		if (len(exp)):
			automats[id] = AFND.Automata(exp)
			Operaciones.cambiar_Imagen(id,frame)
			OptionList.actualizar()
		else:
			messagebox.showinfo("Error de entrada", "Ingrese un símbolo válido")

	def opcional(frame):
		global currAutomat
		if currAutomat:
			automats[currAutomat].opcional()
			Operaciones.cambiar_Imagen(currAutomat, frame)
		else:
			messagebox.showinfo("Error de entrada", "Ingrese un símbolo válido")

	def unirM(seleccion, frame):
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
				Operaciones.cambiar_Imagen(currAutomat, frame)
			else:
				mainAutomata = keys[0]
				keys.remove(keys[0])
			automatasAUnir = []
			for k in keys:
				if k in automats.keys():
					automatasAUnir.append(automats[k])
					automats[mainAutomata].unirM(automatasAUnir)
					currAutomat = mainAutomata
					Operaciones.cambiar_Imagen(currAutomat, frame)
			OptionList.actualizar()
		else:
			messagebox.showinfo("Error de entrada", "Seleccione al menos 2 autómatas")

	def cerrPos(frame):
		global currAutomat
		if currAutomat:
			automats[currAutomat].cerradura_positiva()
			Operaciones.cambiar_Imagen(currAutomat, frame)
		else:
			messagebox.showinfo("Error de entrada", "Seleccione un autómata")

	def cerrKle(frame):
		global currAutomat
		if currAutomat:
			automats[currAutomat].cerradura_kleene()
			Operaciones.cambiar_Imagen(currAutomat, frame)
		else:
			messagebox.showinfo("Error de entrada", "Seleccione un autómata")

	def cambiar_Imagen(id, frame):
		global currAutomat
		if id in automats.keys():
			automats[id].plot(id)
			Image.ImageWidow(frame, path='images/'+id+'.png')
			#err_lbl_VerGrafo.config(text = '')
			#lbl_Sel.config(text=id)
			currAutomat = id
		else:
			messagebox.showinfo("Error de entrada", "Seleccione un autómata")

	def Union(f2, frame):
		global currAutomat
		if f2 and currAutomat:
			automats[currAutomat].unir(automats[f2])
			Operaciones.cambiar_Imagen(currAutomat, frame)
			del automats[f2]
		else:
			messagebox.showinfo("Error de entrada", "Seleccione al menos 2 autómatas")



	def Operacion(operacion, frame, f2 = None, sigma=''):
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
					Operaciones.cambiar_Imagen(currAutomat, frame)
			else:
				messagebox.showinfo("Error de entrada", "No existe ese autómata")
		else:
			messagebox.showinfo("Error de entrada", "No existe ese autómata")

class OptionList(Listbox):
	def __init__(self, master):
		Listbox.__init__(self, master)

	def desplegar(self,num):
		for item in ["F1", "F2", "F3", "F4", "F5"]:
			if num == 0: #No ha sido creado
				if item not in automats.keys():
					self.insert(END, item)

			if num == 1:
				if item != currAutomat:
					if item in automats.keys():
						self.insert(END, item)

		self.config(height = 0)

	def actualizar():
		for num in range((len(optionLists))):
			optionLists[num].delete(0,END)
			if num == 0:
				optionLists[num].desplegar(0)
			else:
				optionLists[num].desplegar(1)

class Automata(Frame):
	def __init__(self,master):
		Frame.__init__(self, master)

		frameMenu = Frame(self)
		frameImagen = Frame(self)
		frameMenu.pack(side = "left", fill = "both")
		frameImagen.pack(side = "left", fill = "both", expand = True)
		oper = Operaciones()
		#------------Labels----------#
		lblCrear = Label(frameMenu, text = "Crear", width = 30) #bg
		lblSimbolos = Label(frameMenu, text = "Ingresa los símbolos del autómata")
		lblCambiarAut = Label(frameMenu, text = "Cambiar autómata") #bg
		lblOper = Label(frameMenu, text = "Operaciones") #bg
		lblOperU = Label(frameMenu, text = "Operaciones unarias")
		lblOperB = Label(frameMenu, text = "Operaciones binarias")

		#-----------Text------------#
		txtSimbolos = Entry(frameMenu, width = 4)

		#----------Option List------#
		lbCrearAut = OptionList(frameMenu)
		lbCrearAut.desplegar(0)
		lbCambiar = OptionList(frameMenu)
		lbCambiar.desplegar(1)
		lbOper = OptionList(frameMenu)
		lbOper.desplegar(1)
		optionLists.append(lbCrearAut)
		optionLists.append(lbCambiar)
		optionLists.append(lbOper)

		#------------Buttons----------#
		btnCrear = Button(frameMenu, text = "Crear autómata")
		btnCrear.config(command = lambda: Operaciones.basico(lbCrearAut.get(ACTIVE),txtSimbolos.get(),frameImagen))

		btnCambiar = Button(frameMenu, text = "Cambiar de autómata")
		btnOpcional = Button(frameMenu, text = "Opcional (?)")
		btnOpcional.config(command = lambda:Operaciones.opcional(frameImagen))
		btnCerraduraP = Button(frameMenu, text = "Cerradura positiva (+)")
		btnCerraduraP.config(command = lambda:Operaciones.cerrPos(frameImagen))
		btnCerraduraK = Button(frameMenu, text = "Cerradura kleene (*)")
		btnCerraduraK.config(command = lambda:Operaciones.cerrKle(frameImagen))
		btnUnion = Button(frameMenu, text = "Unión (|)")
		btnUnion.config(command = lambda: Operaciones.Operacion('Union', frameImagen,lbOper.get(ACTIVE)))
		btnConcat = Button(frameMenu, text = "Concatenar (&)")
		btnConcat.config(command = lambda: Operaciones.Operacion('Concat', frameImagen,lbOper.get(ACTIVE)))
		btnUnirSel = Button(frameMenu, text = "Unir seleccionados (.|.|.)")
		btnUnirSel.config(command = lambda: Operaciones.unirM(frameImagen, lstbox_Binarias.curselection()))

		lblCrear.pack(fill = "x")
		lblSimbolos.pack(fill = "x")
		txtSimbolos.pack(fill = "x")
		lbCrearAut.pack(fill = "x")
		btnCrear.pack(fill = "x")

		lblCambiarAut.pack(fill = "x")
		lbCambiar.pack(fill = "x")
		btnCambiar.pack(fill = "x")

		lblOper.pack(fill = "x")
		lblOperU.pack(fill = "x")
		btnOpcional.pack(fill = "x")
		btnCerraduraP.pack(fill = "x")
		btnCerraduraK.pack(fill = "x")
		lblOperB.pack(fill = "x")
		btnUnion.pack(fill = "x")
		btnConcat.pack(fill = "x")
		btnUnirSel.pack(fill = "x")
		lbOper.pack(fill = "x")

class Analizar(Frame):
	def __init__(self, master):
		ttk.Frame.__init__(self, master)

		frameMenu = Frame(self)
		frameImagen = Frame(self)
		frameMenu.pack(side = "left", fill = "both")
		frameImagen.pack(side = "left", fill = "both", expand = True)

		#--------Labels
		lblAcutal = Label(frameImagen, text = currAutomat)
		lblAcutal.pack(side = "top", fill = "x")
		lblSelecAut = Label(frameMenu, text = "Seleccionar autómata"  , width = 30)
		lblResultado = Label(frameMenu, text = "",  )
		lblIngresaCad = Label(frameMenu, text = "Ingresa una cadena"  )

		#-------Entry
		txtCadena = Entry(frameMenu  )

		#-----------Buttons
		btnSelecAut = Button(frameMenu, text = "Ver condiciones")
		btnAnalizar = Button(frameMenu, text = "Analizar")

		#-----------Listbox
		lbSelecAut = OptionList(frameMenu)
		lbSelecAut.desplegar(1)
		optionLists.append(lbSelecAut)

		lblSelecAut.pack(fill = "x")
		lbSelecAut.pack(fill = "x")
		btnSelecAut.pack(fill = "x")

		lblIngresaCad.pack(fill = "x")
		txtCadena.pack(fill = "x")
		lblResultado.pack(fill = "x")
		btnAnalizar.pack(fill = "x")

class Calculadora(Frame):
	def __init__(self, master):
		master.grid_rowconfigure(0, weight=1)
		master.grid_columnconfigure(0, weight=1)
		master.option_add("*font", "Helvetica 28")
		Frame.__init__(self, master)
		self.config(bg = "white")

		self.rowconfigure(0, weight = 1)
		self.rowconfigure(1, weight = 1)
		self.rowconfigure(2, weight = 1)
		self.rowconfigure(3, weight = 1)
		self.rowconfigure(4, weight = 1)

		self.columnconfigure(0, weight = 1)
		self.columnconfigure(1, weight = 1)
		self.columnconfigure(2, weight = 1)
		self.columnconfigure(3, weight = 1)
		self.columnconfigure(4, weight = 1)
		self.columnconfigure(5, weight = 1)
		self.columnconfigure(6, weight = 1)

		s = ttk.Style()
		s.configure("TButton", anchor = "center", background = "#496ba0", foreground = "white", font = ("Helvetica", 28), border = "classic")
		s.map("TButton",
				foreground = [("disabled", "white"),
							("pressed", "#f2f4f7")],
				background = [("disabled", "#496ba0"),
							("pressed", "#354154")])
		sEqual = ttk.Style()
		sEqual.configure("Equal.TButton",  anchor = "center", background = "red", foreground = "white", font = ("Helvetica", 28), border = "classic")
		sEqual.map("Equal.TButton",
			foreground = [("selected", "#ffffff")],
			background = [("pressed", "gray")])
		#sEqual.theme_use("Equal.TButton")
		"""sEqual.map("TButton",
				foreground = [("disabled", "white"),
							("pressed", "#f2f4f7")],
				background = [("disabled", "#496ba0"),
							("pressed", "#354154")])"""
		#-------Entrada
		txtCadena = Label(self, bg = "white", text = "0")

		#----Operaciones-----
		btnMas = ttk.Button(self, text = "+", command = lambda:Calculadora.escribe(txtCadena, "+"))
		btnMenos = ttk.Button(self, text = "-", command = lambda:Calculadora.escribe(txtCadena, "-"))
		btnMult = ttk.Button(self, text = "*", command = lambda:Calculadora.escribe(txtCadena, "*"))
		btnDiv = ttk.Button(self, text = "/", command = lambda:Calculadora.escribe(txtCadena, "/"))
		btnExpo = ttk.Button(self, text = "^", command = lambda:Calculadora.escribe(txtCadena, "^"))

		btnSen = ttk.Button(self, text = "sen", command = lambda:Calculadora.escribe(txtCadena, "sen("))
		btnCos = ttk.Button(self, text = "cos", command = lambda:Calculadora.escribe(txtCadena, "cos("))
		btnTan = ttk.Button(self, text = "tan", command = lambda:Calculadora.escribe(txtCadena, "tan"))
		btnLn = ttk.Button(self, text = "ln", command = lambda:Calculadora.escribe(txtCadena, "ln("))
		btnLog = ttk.Button(self, text = "log", command = lambda:Calculadora.escribe(txtCadena, "log("))
		btnE = ttk.Button(self, text = "exp", command = lambda:Calculadora.escribe(txtCadena, "exp("))

		#------Números-----
		btnCero = ttk.Button(self, text = "0", command = lambda:Calculadora.escribe(txtCadena, "0"))
		btnUno = ttk.Button(self, text = "1", command = lambda:Calculadora.escribe(txtCadena, "1"))
		btnDos = ttk.Button(self, text = "2", command = lambda:Calculadora.escribe(txtCadena, "2"))
		btnTres = ttk.Button(self, text = "3", command = lambda:Calculadora.escribe(txtCadena, "3"))
		btnCuatro = ttk.Button(self, text = "4", command = lambda:Calculadora.escribe(txtCadena, "4"))
		btnCinco = ttk.Button(self, text = "5", command = lambda:Calculadora.escribe(txtCadena, "5"))
		btnSeis = ttk.Button(self, text = "6", command = lambda:Calculadora.escribe(txtCadena, "6"))
		btnSiete = ttk.Button(self, text = "7", command = lambda:Calculadora.escribe(txtCadena, "7"))
		btnOcho = ttk.Button(self, text = "8", command = lambda:Calculadora.escribe(txtCadena, "8"))
		btnNueve = ttk.Button(self, text = "9", command = lambda:Calculadora.escribe(txtCadena, "9"))

		#-----Símbolos
		btnPunto = ttk.Button(self, text = ".", command = lambda:Calculadora.escribe(txtCadena, "."))
		btnParI = ttk.Button(self, text = "(", command = lambda:Calculadora.escribe(txtCadena, "("))
		btnParD = ttk.Button(self, text = ")", command = lambda:Calculadora.escribe(txtCadena, ")"))

		#------Otros :u
		btnIgual = ttk.Button(self, text = "=", style = "Equal.TButton", command = lambda:Calculadora.resultado(txtCadena))
		btnBorra = ttk.Button(self, text = "←", command = lambda: Calculadora.borra(txtCadena))
		btnBorraTodo = ttk.Button(self, text = "C", command = lambda:Calculadora.borraTodo(txtCadena))

		txtCadena.grid(row = 0, column = 0, columnspan = 7, sticky = "e")

		btnSen.grid(row = 1, column = 0, sticky = "nsew")
		btnLn.grid(row= 1, column = 1, sticky = "nsew")
		btnSiete.grid(row = 1, column = 2, sticky = "nsew")
		btnOcho.grid(row = 1, column = 3, sticky = "nsew")
		btnNueve.grid(row = 1, column = 4, sticky = "nsew")
		btnMas.grid(row = 1, column = 5, sticky = "nsew")
		btnMenos.grid(row = 1, column = 6, sticky = "nsew")


		btnCos.grid(row = 2, column = 0, sticky = "nsew")
		btnLog.grid(row = 2, column = 1, sticky = "nsew")
		btnCuatro.grid(row = 2, column = 2, sticky = "nsew")
		btnCinco.grid(row = 2, column = 3, sticky = "nsew")
		btnSeis.grid(row = 2, column = 4, sticky = "nsew")
		btnMult.grid(row = 2, column = 5, sticky = "nsew")
		btnDiv.grid(row = 2, column = 6, sticky = "nsew")


		btnTan.grid(row = 3, column = 0, sticky = "nsew")
		btnExpo.grid(row = 3, column = 1, sticky = "nsew")
		btnUno.grid(row = 3, column = 2, sticky = "nsew")
		btnDos.grid(row = 3, column = 3, sticky = "nsew")
		btnTres.grid(row = 3, column = 4, sticky = "nsew")
		btnBorra.grid(row = 3, column = 5, sticky = "nsew")
		btnBorraTodo.grid(row = 3, column = 6, sticky = "nsew")

		btnE.grid(row = 4, column = 0, sticky = "nsew")
		btnParI.grid(row = 4, column = 1, sticky = "nsew")
		btnParD.grid(row = 4, column = 2, sticky = "nsew")
		btnCero.grid(row = 4, column = 3, sticky = "nsew")
		btnPunto.grid(row = 4, column = 4, sticky = "nsew")
		btnIgual.grid(row = 4, column = 5, columnspan = 2, sticky = "nsew")

	def escribe(label, texto):
		cantidades.append(texto)
		label.config(text = cantidades)

	def borraTodo(label):
		del cantidades[:]
		label.config(text = "0")

	def borra(label):
		if len(cantidades) > 1:
			cantidades.pop()
			label.config(text = cantidades)
		else:
			del cantidades[:]
			label.config(text = "0")

	def resultado(label):
		file = os.path.join("Calculadora", "p.txt")
		f = open(file, "w+")
		"""for i in range (len(cantidades)):
			f.write(cantidades[i])"""
		del cantidades[:]
		res = ":B no funciona"
		label.config(text = res)
		#f.truncate(0)


root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("AFND")
root.config(bg = "white")
root.option_add("*font", "Helvetica 11")

tab_control = ttk.Notebook(root)
mygreen = "#a9c1e8"
myred = "#2d4263"

style = ttk.Style()

style.theme_create( "Barra", parent="alt", settings={"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": mygreen, "font" : "Helvetica 11"},
            "map":       {"background": [("selected", myred)], "foreground" : [("selected", "#ffffff")],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )
style.theme_use("Barra")

crearAutomata = Automata(tab_control)
tab_control.add(crearAutomata, text = "Crear Autómata")
analizarAutomata = Analizar(tab_control)
tab_control.add(analizarAutomata, text = "Analizar Autómata")

calcula = Calculadora(tab_control)
tab_control.add(calcula, text = "Calculadora")

tab_control.pack(fill = "both", expand = True)

root.mainloop()