import FirstFollow as FF

def algo:
	print("algo no esta bien")

class LL1:
	def __init__(self,path):
		self.gramatica = FF.Gramatica(path)
		

	def crarArchivo(self):
		f = open("LL1_","w+")
		for i in self.gramatica.reglas.items():
			f.write("%s" % self.gramatica.reglas.get(i)
		



pruebas = 