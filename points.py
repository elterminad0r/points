#!/usr/bin/python

from __future__ import division


import sys
import copy

def dc (list):
    return copy.deepcopy(list)

xcoords = [2, 5, 0, 7, 6.3, 3]
ycoords = [1, 3, 5.3, 0, 4, 5]

rnd = 3

if len(xcoords) != len(ycoords):
    sys.exit('ERROR: coordinates do not match up')

polyn_order = len(xcoords) - 1

sim_eqs = []
working_list1 = []
working_list2 = []
final_polynomial = []
working_var1 = 0
working_var2 = 0
confirmation = 0

for i in range (0, len(xcoords)):
    if xcoords.count(xcoords[i]) != 1:
        sys.exit("ERROR: duplicate x co-ordinates")


        
for i in range (0, len(xcoords)):
    for a in range (0, polyn_order + 1):
        sim_eqs.append(xcoords[i]**(polyn_order - a))
    sim_eqs.append(ycoords[i])

if 0 in xcoords:
#    sys.exit("work in progress")
    final_polynomial.insert(0, ycoords[xcoords.index(0)])
    for i in range(polyn_order+1):
        sim_eqs[(polyn_order + 2)*i+polyn_order + 1] = sim_eqs[(polyn_order + 2)*i+polyn_order + 1] - ycoords[xcoords.index(0)]
    for i in range(polyn_order+1):
        working_var1 = polyn_order-i
        del sim_eqs[(polyn_order + 2)*working_var1+polyn_order]
        working_var1 = 0
    for i in range(polyn_order + 1):
        del sim_eqs[(polyn_order + 1) * (xcoords.index(0))]
    polyn_order += -1

#print(0, ycoords[xcoords.index(0)])

#print (sim_eqs)
#print (working_list1)
#print (working_list2)
#print (final_polynomial)
#print(polyn_order)

p_polyn_order = dc(polyn_order)
sp_polyn_order = dc(polyn_order)
p_sim_eqs = dc(sim_eqs)
sp_sim_eqs = dc(sim_eqs)
p_xcoords = dc(xcoords)
p_ycoords = dc(ycoords)

for kdljf in range(p_polyn_order + 1):
    
    while polyn_order > 0 :
        
        del working_list1[:]
        del working_list2[:]

        for a in range (0, len(sim_eqs) - polyn_order - 2):
            working_list1.append(sim_eqs[0] * sim_eqs[a + polyn_order + 2])
        for c in range (0, polyn_order):
            for b in range (0, polyn_order + 2):
                    working_list2.append(sim_eqs[b] * sim_eqs[(polyn_order + 2) * (c + 1)])

        del sim_eqs[:]

        for a in range (0, len(working_list1)):
            sim_eqs.append(working_list1[a] - working_list2[a])
        for a in range(0, polyn_order):
             del sim_eqs[(polyn_order + 2) * (polyn_order - a - 1)]

        polyn_order = polyn_order - 1

    final_polynomial.insert(0, sim_eqs[1]/sim_eqs[0])
    sim_eqs = dc(sp_sim_eqs)
    polyn_order = dc(sp_polyn_order)
    for i in range(polyn_order+1):
        sim_eqs[(polyn_order + 2)*i+polyn_order + 1] = sim_eqs[(polyn_order + 2)*i+polyn_order + 1] - final_polynomial[0]*sim_eqs[(polyn_order + 2)*i+polyn_order]
    for i in range(polyn_order+1):
        working_var1 = polyn_order-i
        del sim_eqs[(polyn_order + 2)*working_var1+polyn_order]
        working_var1 = 0
    for i in range(polyn_order + 1):
        del sim_eqs[len(sim_eqs)-1]
    sp_sim_eqs = dc(sim_eqs)
    sp_polyn_order += -1
    polyn_order += -1

#print (sim_eqs)
#print (working_list1)
#print (working_list2)
for b in (final_polynomial):
    print ("%.3f" % b)
#print(polyn_order)
