#! /usr/bin/python

from fractions import gcd
import sys

def printFracts(inArray):
	print([i.getStr() for i in inArray])

def printMulti(inMultiArray):
	sys.stdout.write('[')
	for i in inMultiArray:
		printFracts(i)

class myFraction:
	
	def __init__(self, numerator, denominator):
		self.numerator = numerator
		self.denominator = denominator

	def simplifyTo(self):
		divisor = gcd(self.numerator, self.denominator)
		self.numerator /= divisor
		self.denominator /= divisor

	def getFloat(self):
		return(self.numerator / self.denominator)

	def getStr(self):
		self.simplifyTo()
		
		if self.denominator == 1:
			return(str(self.numerator))
		else:
			return(str(self.numerator) + " / " + str(self.denominator))

	def intMultiplyTo(self, multiplier):
		self.numerator *= multiplier

	def fractMultiplyTo(self, fractMultiplier):
		self.numerator *= fractMultiplier.numerator
		self.denominator *= fractMultiplier.denominator

	def fractMultiply(self, fractMultiplier):
		return(myFraction(self.numerator * fractMultiplier.numerator, self.denominator * fractMultiplier.denominator))

	def intDivideTo(self, divisor):
		self.denominator *= divisor

	def fractDivideTo(self, fractDivisor):
		self.numerator *= fractDivisor.denominator
		self.denominator *= fractDivisor.numerator

	def fractDivide(self, fractDivisor):
		return(myFraction(self.numerator * fractDivisor.denominator, self.denominator * fractDivisor.numerator))

	def intAddTo(self, addend):
		self.numerator += addend * self.denominator

	def fractAddTo(self, fractAddend):
		self.numerator = self.numerator * fractAddend.denominator + fractAddend.numerator * self.denominator
		self.denominator *= fractAddend.denominator

	def intSubtractTo(self, minuend):
		self.numerator -= minuend * self.denominator

	def fractSubtractTo(self, fractMinuend):
		self.numerator = self.numerator * fractMinuend.denominator - fractMinuend.numerator * self.denominator
		self.denominator *= fractMinuend.denominator
	
	def fractSubtract(self, fractMinuend):
		return(myFraction(self.numerator * fractMinuend.denominator - fractMinuend.numerator * self.denominator, fractMinuend.denominator * self.denominator))

	def exponentiateTo(self, exponent):
		if exponent == 0:
			self.numerator, self.denominator = 1, 1
		else:
			self.numerator = self.numerator**exponent
			self.denominator = self.denominator**exponent

	def exponentiate(self, exponent):
		if exponent == 0:
			return(myFraction(1, 1))
		else:
			return(myFraction(self.numerator ** exponent, self.denominator ** exponent))

if '-f' in sys.argv:
	inFile = file(sys.argv[2], 'r')
	a = [i.split('\t') for i in inFile]
	xCoOrds = [j[0] for j in a]
	yCoOrds = [j[1].rstrip() for j in a]
else:
	try:
		xCoOrds = sys.argv[1::2]
		yCoOrds = sys.argv[2::2]
	except Exception:
		try:
			xCoOrds = sX
			yCoOrds = sY
		except Exception:
			usrIn = input('enter space delimited coordinates in pairs').split(' ')
			xCoOrds = usrIn[::2]
			yCoOrds = usrIn[1::2]

polyArray = []

avgd = False

def avgMultis():
	global xCoOrds
	global yCoOrds

	multis = list(set([i for i in xCoOrds if xCoOrds.count(i) >= 2]))

	
	for i in multis:
		listToAvg = []
		for _ in range(xCoOrds.count(i)):
			listToAvg.append(yCoOrds.pop(xCoOrds.index(i)))
			xCoOrds.remove(i)
		xCoOrds.append(i)
		yCoOrds.append('{0}/{1}'.format(sum([int(i) for i in listToAvg]), len(listToAvg)))

print('\npre avg')
print(xCoOrds, yCoOrds)

if len(xCoOrds) != len(xCoOrds):
	raise ValueError('Coordinates do not match.')


if len(xCoOrds) != len(list(set(xCoOrds))):
	avgMultis()
	avgd = True


def toFraction(inStr):

	if '.' in inStr:
		return myFraction(int(inStr.replace('.', '')), 10**(len(inStr) - inStr.index('.') - 1))

	elif '/' in inStr:
		return myFraction(int(inStr[:inStr.index('/')].strip()), int(inStr[inStr.index('/') + 1:].strip()))

	else:
		return myFraction(int(inStr), 1)

def coOrdsToFractions(inCoOrds):
	return([toFraction(i) for i in inCoOrds])

def coOrdsToSimArray(inX, inY):

#	outArray = []
#
#	for i in range(len(inX)):
#		outSubArray = []
#		for j in range(len(inX), -1, -1):
#			outSubArray.append(inX[i].exponentiate(j))
#		outArray.append(outSubArray + [inY[i]])
#
#	return(outArray)

	return([[inX[j].exponentiate(i) for i in range(len(inX) - 1, -1, -1)] + [inY[j]] for j in range(len(inX))])

def gaussMakeEqual(inSimArray):

#	workArray = [inSimArray[0]]
#	for i in inSimArray[1:]:
#		subArray = []
#		for j in i:
#			subArray.append(inSimArray[0][0].fractMultiply(j))
#		workArray.append(subArray)
#
#
#	print('workArray:')
#	printMulti(workArray)
#	print('LCOMP: ')
#	printMulti([inSimArray[0]] + [[inSimArray[0][0].fractMultiply(j) for j in i] for i in inSimArray[1:]])

	return([inSimArray[0]] + [[inSimArray[0][0].fractMultiply(j) for j in i] for i in inSimArray[1:]])
	
def eliminate(inEqdArray):
#	outArray = []
#	
#	for i in range(len(inEqdArray))[1:]:
#		subArray = []
#		for j in range(len(inEqdArray[0]))[1:]:
#			subArray.append(inSimArray[0][0].fractMultiply(inEqdArray[i][0].fractDivide(inSimArray[0][0])).fractSubtract(inSimArray[i][j]))

#			factDiff = inEqdArray[i][0].fractDivide(inEqdArray[0][0])

#			print('\nfactdiff: \n{0}'.format(factDiff.getStr()))
#
#			print('\n({0}) / ({1})'.format(inEqdArray[i][0].getStr(), inSimArray[0][0].getStr()))
				
#			subArray.append(inEqdArray[i][j].fractSubtract(inEqdArray[0][j].fractMultiply(inEqdArray[i][0].fractDivide(inEqdArray[0][0]))))

	return([[inEqdArray[i][j].fractSubtract(inEqdArray[0][j].fractMultiply(inEqdArray[i][0].fractDivide(inEqdArray[0][0]))) for j in range(len(inEqdArray[0]))[1:]] for i in range(len(inEqdArray))[1:]])
#
#		outArray.append(subArray)
#	
#	return(outArray)
			
def substitute(inSimArray, inSubValue):
	outArray = inSimArray

	for i in range(len(outArray)):
		outArray[i][-1].fractSubtractTo(outArray[i].pop(-2).fractMultiply(inSubValue))

#
#	for i in range(len(inSimArray))[1:]:
#		outSubArray = []
#		for j in range(len(inSimArray[i]))[-2:]:
#			outSubArray.append(inSimArray[i][j])
#
#		outSubArray.append(inSimArray[i][-1].fractSubtract(inSimArray[i][-2].fractMultiply(inSubValue)))
#		outArray.append(outSubArray)

	return(outArray[1:])
	
def catchZero():
	global xCoOrds
	global yCoOrds
	global polyArray

	ind = xCoOrds.index('0')
	
	xCoOrds.remove('0')

	polyArray.append(toFraction(yCoOrds.pop(ind)))

	xCoOrds.insert(0, '0')
	yCoOrds.insert(0, polyArray[-1].getStr())

	


	
print('\ncoords after avg: ')

print(xCoOrds, yCoOrds)

if '0' in xCoOrds:
	catchZero()

	print('\nZero caught')

	caught = True

else:
	caught = False


xCoOrds = coOrdsToFractions(xCoOrds)
yCoOrds = coOrdsToFractions(yCoOrds)

print('\nFinalised fractional getStr method forms')
printFracts(xCoOrds)
printFracts(yCoOrds)

print('\npolarr')
printFracts(polyArray)

simArray = coOrdsToSimArray(xCoOrds, yCoOrds)

print('\nSuperSim')
printMulti(simArray)

if caught:
	simArray = substitute(simArray, polyArray[0])

while len(polyArray) != len(xCoOrds):

	elimArray = gaussMakeEqual(simArray)

	print('\neqd')

	printMulti(elimArray)

	while len(elimArray) != 1:
		elimArray = eliminate(elimArray)
		
		print('\nelimd:')
		printMulti(elimArray)
		
		print('\neqd')
		elimArray = gaussMakeEqual(elimArray)
		printMulti(elimArray)


	polyArray.insert(0, elimArray[0][1].fractDivide(elimArray[0][0]))

	print('poly: ')

	printFracts(polyArray)

	print('\nsubIn')

	printMulti(simArray)

	print('\nsubVal')

	print(polyArray[0].getStr())

	print('\nsubstd')

	simArray = substitute(simArray, polyArray[0])

	printMulti(simArray)

printFracts(polyArray)

print('\nFinal output:\n')

if avgd:
	sys.stdout.write('NOTE: x coordinates were averaged, as there were multiple coordinates with the same x value.\n\n')

sys.stdout.write('y = \n')

for i in range(len(polyArray)):
	charToUse = 'x'
	if len(sys.argv) >= 4:
		charToUse = sys.argv[3]
	
	sys.stdout.write(['({0}){2}^{1} {3}\n', '({0}){2}^{1} {3}'][len(sys.argv) >= 5].format(polyArray[i].getStr(), len(polyArray) - i - 1, charToUse, ['+', ''][i == len(polyArray) - 1]))

sys.stdout.write('\b\b\n\n')
