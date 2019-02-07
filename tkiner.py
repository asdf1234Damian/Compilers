import threading
import tkinter as tk                # python 3
from tkinter import font  as tkfont 
import AFND


class myButton:
	def __init__( self, texto, frame ):
		self.texto = texto
		self.button = tk.Button( frame, text = texto, fg = "white", bg = "#496ba0", activeforeground = "#f2f4f7", activebackground = "#354154", relief = 'flat', width = 25, height = 2, font = ( "Helvetica", 16 ), command = lambda:self.operacion( texto ) )
		self.button.pack()
	
	def operacion( self, texto ):
		def callback():
			test = AFND.Graph('Opcional','a,b,c')
			test.basico('a')
			test.opcional()
			print(test.cEpsilon(test.estados,set()))
			print(test.alf)
			img = tk.PhotoImage(file = "resources\Opcional.png")
			label.config(image = img)
			label.image = img # keep a reference!
			label.pack()
		t = threading.Thread(target=callback)
		t.start()

def raise_frame(frame):
    frame.tkraise()




root = tk.Tk()
#root.resizable(width = 'false', height = 'false')
root.state("zoomed")
root.title( "AFND" )


container = tk.Frame( root, bg = "#496ba0")
container.pack( side = 'left', fill = 'both' )

f1 = tk.Frame(container)
f2 = tk.Frame(container)
f3 = tk.Frame(container)
f4 = tk.Frame(container)

for frame in (f1, f2, f3, f4):
    frame.grid(row=0, column=0, sticky='news')

bottomFrame = tk.Frame( root, bg = 'black' )
bottomFrame.pack( side = 'left', fill = 'both', expand = 1 )
label = tk.Label( bottomFrame, bg = "#f2f4f7" )
label.pack( fill = 'both', expand = 1 )
#------------------F1-----------------------------------
f1.config(bg = "#496ba0")
label_F1 = tk.Label( f1, text = 'Elegir operacion', fg = 'white', bg ="#354154" , font = ( "Helvetica", 16 ) )	
label_F1.pack( fill = 'x' )
button1 = myButton( "Base", f1)
button2 = myButton( "Opcional", f1)
button3 = myButton( "Cerradura positiva", f1)
button4 = myButton( "Cerradura de Kleene", f1)

buttonF1_F2 = tk.Button(f1, text = 'Crear autómata', fg = "white", bg = "#496ba0", activeforeground = "#f2f4f7", activebackground = "#354154", relief = 'flat', width = 25, height = 2, font = ( "Helvetica", 16 ), command = lambda:raise_frame(f2))
buttonF1_F2.pack()
#------------------F2-----------------------------------
f2.config(bg = "#496ba0")
label_F2 = tk.Label( f2, text = 'Crear autómata básico', fg = 'white', bg ="#354154" , font = ( "Helvetica", 16 ) )	
label2_F2 = tk.Label( f2, text = 'Inserte su símbolo', fg = 'white', bg ="#354154" , font = ( "Helvetica", 16 ) )	
text_F2 = tk.Text(f2, width = 25, height = 2, font = ( "Helvetica", 16 ))

label_F2.pack( fill = 'x' )
label2_F2.pack( fill = 'x' )
text_F2.pack()
#--------------------------------------------------------

raise_frame(f1)

root.mainloop()