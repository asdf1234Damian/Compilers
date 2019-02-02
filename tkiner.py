from tkinter import *
import AFND

class myButton:
	def __init__(self,texto,fila):
		self.texto = texto
		self.button = Button(topFrame,text=texto, fg="white", bg="#496ba0",activeforeground="#f2f4f7",activebackground="#354154",relief=FLAT,width = 20,font=("Helvetica", 16), command=lambda:self.saluda(texto))
		self.button.grid(row=fila,sticky=("N", "S", "W","E"))
	
	def saluda(self,texto):
		if texto == "Base":
			test = AFND.Graph('Base')
			test.basico('a')
			test.plot()
		elif texto == "Opcional":
			test = AFND.Graph('Opcional')
			test.basico('b')
			test.opcional()
			test.plot()
		elif texto == "Cerradura positiva":
			test = AFND.Graph('CerraduraP')
			test.basico('c')
			test.cerradura_positiva()
			test.plot()
		elif texto == "Cerradura de Kleene":
			test = AFND.Graph('CerraduraK')
			test.basico('d')
			test.cerradura_kleene()
			test.plot()
			

root = Tk()
topFrame = Frame(root)
topFrame.pack(side=LEFT)
bottomFrame = Frame(root)
bottomFrame.pack(side=RIGHT)

button1 = myButton("Base",0)
button2 = myButton("Opcional",1)
button3 = myButton("Cerradura positiva",2)
button4 = myButton("Cerradura de Kleene",3)


label= Label(topFrame,text="°u°",bg="#f2f4f7",height = 30, width = 100).grid(rowspan=4,column=1,row=0,sticky=("N", "S", "W","E"))

topFrame.pack_propagate(0)

root.mainloop()

