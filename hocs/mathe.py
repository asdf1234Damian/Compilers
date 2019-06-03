import math
from errno import EDOM, ERANGE

errno = None

def Log(x):
	return errcheck(log(x), "log")

def Log10(x):
	return errcheck(log10(x), "log10")

def Exp(x):
	return errcheck(exp(x), "exponentiation")

def Sqrt(x):
	return errcheck(sqrt(x), "sqrt")

def Pow(x, y):
	return errcheck(pow(x, y), "pow")

#define integer

def errcheck(d, s):
	global errno
	if errno == EDOM:
		errno = 0
	elif errno == ERANGE:
		errno = 0

	return d