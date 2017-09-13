#! /usr/bin/python

from cs_fractions import *
import sys
import os

autoSimplify = False

def verbp(*toP):
	if verbose:
		for i in toP:
			if autoSimplify:
				if type(i) == list:
					print [j.simplify() for j in i]
				elif isinstance(i, myFraction):
					print i.simplify()
				else:
					print i
			else:
				print i

def verbPMulti(toP):
	if verbose:
		for i in toP:
			if autoSimplify:
				print [j.simplify() for j in i]
			else:
				print i

lookForFile = True
verbose = False
varChr = 'x'
newL = ' '
inFile = ''
nums = []
optIsPoss = True
powVar = '^'
betweenSim = ''
lookForNums = False
libFunc = ''
libSep = '/'

args = sys.argv[1:]

helpStr = '\
A program to calculate a polynomial designed to pass through a set of co-ordinates. Options:\n\
\t-c char: set char to use as variable in polynomial\n\
\t-b: toggle newlines in polynomial output\n\
\t-n x1 y1 x2 y2 x3 y3... : use numeric input for co-ordinates, as shown\n\
\t-v: set the program to be verbose, and print steps\n\
\t-s: set the program to automatically simplify fractional output when verbose\n\
\t-p: set the program to have pythonic output: an expression that is valid python. does not override other options set\n\
\t-h: print this menu and exit\n\
\t-l: write output appropriate to cs_fractions library'

if 'h' in ''.join([i for i in args if i[0] == '-']):
	print helpStr
	sys.exit()

if 'v' in ''.join([i for i in args if i[0] == '-']):
	verbose = True

for i in args:
	if i[0] == '-' and optIsPoss:
		if i == '--':
			optIsPoss = False

		else:
			for j in i[1:]:
				if j == 'c':
					varChr = args.pop(args.index(i)+1)
				elif j == 'b':
					newL = '\n'
				elif j == 'n':
					lookForNums = True
				elif j == 'v':
					verbose = True
				elif j == 's':
					autoSimplify = True
				elif j == 'p':
					powVar = '**'
					betweenSim = '*'
				elif j == 'l':
					libFunc = 'myFraction'
					libSep = ','
				else:
					sys.exit('Invalid option -{0}\nMaybe you wanted to input a negative integer? If, so, put a -- argument to not parse following arguments as options.'.format(j))

	else:
		if (not lookForNums) and os.path.isfile(i):
			verbp('Using arg file {0}'.format(i))
			inFile = file(i, 'r')
			
		elif lookForNums:
			verbp('Found number in args: {0}.'.format(i))
			nums.append(i)
			
if lookForNums:
	if len(nums) & 1:
		sys.exit('Error: odd number of ordinates')

	else:
		xCoOrds = [toFraction(i) for i in nums[::2]]
		yCoOrds = [toFraction(i) for i in nums[1::2]]
		verbp('Using command line args {0}'.format((xCoOrds, yCoOrds)))

else:
	if inFile == '':
		if not sys.stdin.isatty():
			verbp('Using stdin')
			inFile = sys.stdin
					
	rows = [row for row in inFile][:]

	xCoOrds = [toFraction(row.split('\t')[0]) for row in rows]
	yCoOrds = [toFraction(row.split('\t')[1]) for row in rows]

if len(xCoOrds) * len(yCoOrds) == 0:
	sys.exit('no input for co-ords')

polyArray = []

avgd = False

def purifyFracts(fracts):
	out = []
	for i in fracts:
		if not (i in out):
			out.append(i)

	return out

def avgMultis():
	global xCoOrds
	global yCoOrds

	multis = purifyFracts([i for i in xCoOrds if xCoOrds.count(i) >= 2])
	
	for i in multis:
		listToAvg = []
		for _ in range(xCoOrds.count(i)):
			listToAvg.append(yCoOrds.pop(xCoOrds.index(i)))
			xCoOrds.remove(i)
		xCoOrds.append(i)
		yCoOrds.append(myFraction(sum([int(i) for i in listToAvg]), len(listToAvg)))

verbp('\nCo-ordinates before averaging:')
verbp(xCoOrds, yCoOrds)

if len(xCoOrds) != len(purifyFracts(xCoOrds)):
	avgMultis()
	avgd = True

def coOrdsToSimArray(inX, inY):

	return([[inX[j] ** (i) for i in range(len(inX) - 1, -1, -1)] + [inY[j]] for j in range(len(inX))])

def gaussMakeEqual(inSimArray):
	return([inSimArray[0]] + [[inSimArray[row][i] / (inSimArray[row][0] / inSimArray[0][0]) for i in range(len(inSimArray[0]))] for row in range(len(inSimArray))[1:]])
	
def eliminate(inEqdArray):
	return([[inEqdArray[row][j] - inEqdArray[0][j] for j in range(len(inEqdArray[0]))[1:]] for row in range(len(inEqdArray))[1:]])

def substitute(inSimArray, inSubValue):
	outArray = inSimArray

	for i in range(len(outArray)):
		outArray[i][-1] -= outArray[i].pop(-2) * (inSubValue)

	return(outArray[1:])
	
def catchZero():
	global xCoOrds
	global yCoOrds
	global polyArray

	ind = xCoOrds.index(myFraction(0, 1))
	
	xCoOrds.remove(myFraction(0, 1))

	polyArray.append(yCoOrds.pop(ind))

	xCoOrds.insert(0, myFraction(0, 1))
	yCoOrds.insert(0, polyArray[-1])

verbp('\nCo-ordinates before averaging: ')

verbp(xCoOrds, yCoOrds)

if '0' in xCoOrds:
	catchZero()

	verbp('\nZero caught')

	caught = True

else:
	caught = False


verbp('\nFinalised co-ordinates')
verbp(xCoOrds)
verbp(yCoOrds)

verbp('\nState of polynomial:')
verbp(polyArray)

simArray = coOrdsToSimArray(xCoOrds, yCoOrds)

verbp('\nFirst simultaneous array:')
verbPMulti(simArray)

if caught:
	simArray = substitute(simArray, polyArray[0])

while len(polyArray) != len(xCoOrds):

	elimArray = gaussMakeEqual(simArray)

	verbp('\nEqualised simultaneous array:')

	verbPMulti(elimArray)

	while len(elimArray) != 1:
		elimArray = eliminate(elimArray)
		
		verbp('\nEliminated simultaneous array:')
		verbPMulti(elimArray)
		
		verbp('\nEqualised simultaneous array:')
		elimArray = gaussMakeEqual(elimArray)
		verbPMulti(elimArray)


	polyArray.insert(0, elimArray[0][1] / elimArray[0][0])

	verbp('\nPolynomial array:')

	verbp(polyArray)

	verbp('\nSubstituting array:')

	verbPMulti(simArray)

	verbp('\nSubstitution value:')

	verbp(polyArray[0])

	verbp('\nSubstituted array:')

	simArray = substitute(simArray, polyArray[0])

	verbPMulti(simArray)

verbp(polyArray)

verbp('\nFinal output:\n')

if avgd:
	sys.stdout.write('NOTE: x coordinates were averaged, as there were multiple coordinates with the same x value.\n\n')

sys.stdout.write('y = \n')

for i in range(len(polyArray))[:-1]:
	charToUse = 'x'
	if len(sys.argv) >= 4:
		charToUse = sys.argv[3]
	
	sys.stdout.write('{libf}({coeff}){between}({char}{powSim}{exp}) +{newVar}'.format(coeff='{num} {sep} {den}'.format(num=polyArray[i].simplify().numerator, den=polyArray[i].simplify().denominator, sep=libSep), char=varChr, powSim=powVar, exp=len(polyArray) - i - 1, newVar=newL, between=betweenSim, libf=libFunc))

sys.stdout.write('{libf}({coeff}){between}({char}{powSim}{exp}) \n'.format(coeff='{num} {sep} {den}'.format(num=polyArray[-1].simplify().numerator, den=polyArray[-1].simplify().denominator, sep=libSep), char=varChr, powSim=powVar, exp=0, between=betweenSim, libf=libFunc))
