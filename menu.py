import os
import AFND

def menu():
	"""
	Función que limpia la pantalla y muestra nuevamente el menu
	"""
	os.system('cls') # NOTA para windows tienes que cambiar clear por cls
	print ("Selecciona una opción")
	print ("\t1 - Base")
	print ("\t2 - Opcional")
	print ("\t3 - Cerradura positiva")
	print ("\t4 - Cerradura de Kleene")
	print ("\t9 - salir")
 
 
while True:
	# Mostramos el menu
	menu()
 
	# solicituamos una opción al usuario
	opcionMenu = input("inserta un numero valor >> ")
 
	if opcionMenu=="1":
		test = AFND.Graph('Base')
		test.basico('a')
		test.plot()
	elif opcionMenu=="2":
		test = AFND.Graph('Opcional')
		test.basico('b')
		test.opcional()
		test.plot()
	elif opcionMenu=="3":
		test = AFND.Graph('CerraduraP')
		test.basico('c')
		test.cerradura_positiva()
	elif opcionMenu=="4":
		test = AFND.Graph('CerraduraK')
		test.basico('d')
		test.cerradura_kleene()
	elif opcionMenu=="9":
		break
	else:
		print ("")
		input("No has pulsado ninguna opción correcta...")
	input("\npulsa una tecla para continuar ")