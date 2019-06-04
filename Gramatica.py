import itertools
import sys
EPS = 'ε'

#Funcion para eliminar repeticiones sin usar set
def delRep(l):
	l = list(l)
	l.sort()
	return list(l for l,_ in itertools.groupby(l))

class Gramatica:
	def __init__(self, path,type):
		self.siva = False
		self.tabla = {}
		self.reglas = {}
		self.terminales = set()
		self.noTerminales = set()
		self.raiz = None
		self.tipo = type
		self.recursiva=False
		self.errorAlCrear = False
		#Crea el diccionario de reglas segun el archivo
		with open(path, "r") as file:
			file = file.readlines()
			# El estado incial es el primer elemento en la primer linea
			self.raiz = file[0].split()[0]
			#Set con todos los simbolos en la gramatica, terminales y no terminales
			simbolos = set()
			# Se guardan todas las reglas en un mapa
			for line in file:
				line = line.split()
				#Se borra la flecha de la tabla
				del line[1]
				simbolos.update(set(line))
				izq = line[0]
				self.noTerminales.add(izq)
				der = line[1:]
				if izq == der[0]:
					print('recursion en',izq,der)
					self.recursiva=True
				if izq in self.reglas.keys():
					self.reglas[izq].append(der)
				else:
					self.reglas[izq] = [der]
			#Se calcula terminales
			self.terminales = simbolos - self.noTerminales
			if not EPS in self.terminales:
				self.terminales.add(EPS)
			self.terminales.add('$')
			self.terminales = delRep(self.terminales)
			self.noTerminales = delRep(self.noTerminales)
		if self.tipo == 'LL1':
			self.genTablaLL1()
		elif self.tipo == 'LR0':
			self.genTablaLR0()
		else:
			self.errorAlCrear='el tipo de analisis nol es valido'

	def __str__(self):
		res = ''
		if self.errorAlCrear:
			return res
		res += 'Raiz: ' + self.raiz + '\n'
		res += 'Vt: {' + ','.join(self.terminales) + '} \n'
		res += 'Vn: {' + ','.join(self.noTerminales) + '\n'
		res +='Reglas'.center(50,'-')+ '\n'
		i=0
		for izq,derArr in self.reglas.items():
			for der in derArr:
				res += str(i)+') ' + izq + ' -> ' + ''.join(der) + '\n'
				i+=1
		if self.tipo == 'LL1':
			res += 'Tabla LL1'.center(50,'-')+'\n'
			terminales = self.terminales[:]
			terminales.remove(EPS)
			terminales.append('$')
			res+=''.center(6)+'| '
			for t in terminales:
				res += t.center(6)+'| '
			res += '\n'
			for x in self.noTerminales:
				res += '-'*8*(len(terminales)+1) + '\n'
				res += x.ljust(6)+'| '
				for y in terminales:
					res += (''.join(self.tabla[x][y][:-1])).center(6) + '| '
				res += '\n'
		if self.tipo == 'LR0':
			print(''.rjust(50,'-'))
			simbolos = self.terminales[:]
			simbolos.remove(EPS)
			simbolos.append('$')
			simbolos += self.noTerminales[:]
			print(''.center(6),'|',end = '')
			for s in simbolos:
				print(s.center(6),'|',end = '')
			print()
			for i in range(len(self.tabla.keys())):
				print(str(i).center(6),'|',end = '')
				for s in simbolos:
					if s in self.tabla[i].keys():
						print((''.join(map(str,self.tabla[i][s]))).center(6),'|',end = '')
					else:
						print(''.center(6),'|',end = '')
				print()
		return res

	def print(self):
		print('Raiz:', self.raiz)
		print('Vt:', self.terminales)
		print('Vn:', self.noTerminales)
		print(''.rjust(50,'-'))
		i=0
		for izq,derArr in self.reglas.items():
			for der in derArr:
				print(str(i)+')',izq,'->', der)
				i+=1
		if self.tipo == 'LL1':
			print(''.rjust(50,'-'))
			terminales = self.terminales[:]
			terminales.remove(EPS)
			terminales.append('$')
			print(''.center(6),'|',end = '')
			for t in terminales:
				print(t.center(6),'|',end = '')
			print()
			for x in self.noTerminales:
				print('-'*8*(len(terminales)+1))
				print(x.center(6),'|',end = '')
				for y in terminales:
					print((''.join(self.tabla[x][y][:-1])).center(6),'|',end = '')
				print()
		if self.tipo == 'LR0':
			print(''.rjust(50,'-'))
			simbolos = self.terminales[:]
			simbolos.remove(EPS)
			simbolos.append('$')
			simbolos += self.noTerminales[:]
			print(''.center(6),'|',end = '')
			for s in simbolos:
				print(s.center(6),'|',end = '')
			print()
			for i in range(len(self.tabla.keys())):
				print(str(i).center(6),'|',end = '')
				for s in simbolos:
					if s in self.tabla[i].keys():
						print((''.join(map(str,self.tabla[i][s]))).center(6),'|',end = '')
					else:
						print(''.center(6),'|',end = '')
				print()


	def first(self, simb,getDer):
		# res será el resultado
		res = []
        # Se limpia la entrada
		if isinstance(simb, str):
			simb = list(simb.split())
		if EPS in simb:
			res.append(EPS)
			simb.remove(EPS)
		# Mientras simb tenga un elementos (despues de borrar eps)
		if len(simb):
            # Si encuentra un terminal, regresa el resultado
			if simb[0] in self.terminales:
				res.append(simb[0])
				return delRep(res)
            # Si no, busca las reglas donde el simbolo esta en la izq
			for der in self.reglas[simb[0]]:
				f = self.first(der+simb[1:],False)
				res+=f
		return res


	# alpha - > gamma A beta
	# Hay que mandar a llamar con una lista vacia en stack
	def follow(self, A, stack =[]):
		fllwA = []
		if A in stack:
			return delRep(fllwA)
		stack.append(A)
		if A == self.raiz:
			fllwA.append('$')
		for alpha, derArr in self.reglas.items():
			for der in derArr:
				if A in der:
					i = der.index(A)
					beta=der[i+1:]
					if len(beta):
						frstB = self.first(beta,False)
						fllwA += frstB
						if EPS in frstB:
							fllwA += self.follow(alpha,stack[:])
					else:
						fllwA += self.follow(alpha,stack[:])
		return delRep(fllwA)


	def genTablaLL1(self):
		if self.recursiva:
			self.errorAlCrear = 'no se puede usar LL1 para una gramatica recursiva'
			return
		terminales = self.terminales[:]
		terminales.remove(EPS)
		terminales.append('$')
		self.tabla = {n : {t : [] for t in terminales} for n in self.noTerminales}
		i = 0
		for izq, derArr in self.reglas.items():
			for der in derArr:
				i+=1
				if EPS in der:
					f = self.follow(izq,[])
				else:
					f = self.first(der[:],True)
				for s in f:
					self.tabla[izq][s] = (der[:]+[','+str(i)])

	def analyzeLL1(self, cad):
		output = ''
		cad =cad+'$'
		stack = ['$', self.raiz]
		output += '-'*85+'\n'
		output +='| '+'Analisis lexico'.center(81)+'|\n'
		output += '-'*85+'\n'
		while len(stack) and len(cad):
			output += (' '.join(stack)).ljust(30)+'| '
			output += (' '.join(cad)).ljust(50)+ '|\n'
			sp = stack.pop()
			simb  = cad [0]
			if sp == EPS:
				pass
			elif (sp in self.terminales):
				if simb == sp:
					if simb == '$':
						return output + 'Cadena valida!'
					cad = cad[1:]
				else:
					return output+'Cadena invalida!'
			else:
				if not simb in self.terminales:
					return output+'Cadena invalida!'
				contTabla  = self.tabla[sp][simb][:-1]
				if(len(contTabla)):
					stack += contTabla[::-1]
				else:
					return output+'Cadena invalida!'
		return output+'Cadena invalida!'

	# Extiende la gramatica si es necesario
	def extendGram(self):
		#Si la raiz tiene mas de una regla
		if len(self.reglas[self.raiz])>1:
			#Busca un simbolo disponible
			for i in range (ord('A'), ord('Z')+1):
				if not chr(i) in self.reglas.keys():
					#Crea la nueva raiz
					nRaiz= chr(i)
					#Crea una transicion de la nueva raiz a la vieja raiz
					self.reglas[nRaiz] = [[self.raiz]]
					#Cambia la raiz por la nueva raiz
					self.raiz = nRaiz
					#Regresa true porque pues por que no?
					return True

	def getRuleIndex(self,ls,rs):
		k = 0
		for l,rlst in self.reglas.items():
			for r in rlst:
				if ls == l and rs==r:
					return k
				k+=1



	def genTablaLR0(self):
		#Extiende la gramatica si es necesario
		self.extendGram()
		#Left side
		ls = self.raiz
		#Right side
		rs = self.reglas[ls][0]
		# Lista de todas las s
		s = []
		#Se inicializa S0 con la cerradura de la raiz
		s.append(self.cerraduraLR0(ls,rs,0,set()))
		i = 0
		while i != len(s):
			simbols = set()
			print('Analisis de S'+str(i))
			for item in s[i]:
				pos = item[2]
				rs  =item[1]
				if pos < len(rs) and not rs[pos] in simbols :
					simbols.add(rs[pos])
					sj = self.IrA(s[i],rs[pos])
					print('(S'+str(i)+',\''+rs[pos],end='\')=')
					if len(sj)>0 and not sj in s:
						s.append(sj)
						print('S'+str(len(s)-1)+':',sj)
					elif not len(sj):
						print(sj)
					else:
						print('(S'+str(s.index(sj)),end=')\n')
			i+=1
		j = 0
		for sj in s:
			self.tabla[j] = {}
			for i in sj:
				ls, rs, pos = i
				# En caso de punto final
				if pos == len(rs):
					simbs = self.follow(ls,[])
					index= self.getRuleIndex(ls, rs)
					for s in simbs:
						self.tabla[j][s] = ('R',index)
				else:
					if rs[pos] in self.noTerminales:
						index= self.getRuleIndex(ls, rs)
						self.tabla[j][rs[pos]] = [index]
					else:
						self.tabla[j][rs[pos]] = ('D',index)
			j+=1



	def IrA(self,sj,simb):
		# resultado
		res = []
		# Busca en el conjunto las reglas a las que se les puede aplicar moverA
		for i in sj:
			mov= None
			# right side of the rule
			rs = i[1]
			# position of item
			pos = i[2]
			if pos >= len(rs):
				# print('debug',i,rs, pos)
				pass
			elif simb == rs[pos]:
				mov = self.moverA(i)
				res += self.cerraduraLR0(mov[0],mov[1],mov[2],set())
		return res

	def moverA(self,rule):
		#Porque las tuplas son inmutables
		pos = rule[2]+1
		return (rule[0],rule[1],pos)

	def cerraduraLR0(self,ls,rs,tokePos,stack):
		c = [(ls,rs,tokePos)]
		# Mi bloque de prints para cuando se cicla infinitamente :3
		# print(ls,'->',end=' ')
		# for i in range(len(rs)):
		# 	if i==tokePos:
		# 		print('•',end='')
		# 	print(rs[i],end='')
		# input()
		if tokePos >= len(rs):
			return c
		if not rs[tokePos] in self.reglas.keys():
			return c
		if not rs[tokePos] in stack:
			stack.add(rs[tokePos])
			for r in self.reglas[rs[tokePos]]:
				cerr = self.cerraduraLR0(rs[tokePos],r,0,stack)
				c += cerr
		return c


# print('Gram')
# gram = Gramatica('testFiles/Gramatica.txt', 'LL1')
# gram.print()
# gram.analyzeLL1('n+n')
