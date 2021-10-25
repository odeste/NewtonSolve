import matplotlib.pyplot as plt
import numpy as np

import sys # to use stdout flush
import cmath # to use complex numbers. j^2 = -1 (caevat not j^3)
from cmath import sqrt

def valPoly (p,zeros):
    res = 1.0
    for r in zeros:
        res *= (p-r)
    return(res)

def valDeriv(p,zeros):
    res = 0.0
    for i in range(len(zeros)):
        acc = 1
        for  j in range(len(zeros)):
            if i != j:
                acc *= (p-zeros[j])
        res += acc
    return(res)

def newt (p,zeros):

    cpt = 0
    remain=valPoly (p,zeros)
    cont = True

    while cont:
        deriv =  valDeriv (p,zeros)
        p -= remain / deriv # TODO do not divide by zero

        cpt += 1
        remain=valPoly (p,zeros)
        cont =  (abs(remain) > 1E-20)
    return p

def nearestIndice(p,lp):
    res = -1
    distMin = 9466 #any value will be overided
    for i in range(len(lp)):
        dist = abs(p-lp[i])
        if (res == -1) or (dist<distMin):
            res = i
            distMin=dist
    return res


# Python program to swap two variables
def test(zeros):

    p = -10
    print('The poly val is: {}'.format(newt(p,zeros)))
    print('The deriv val is: {}'.format(valDeriv(p,zeros)))
    rac1 = newt(p,zeros)
    print('Rac1 is : {}'.format(rac1))
    print('Poly val for rac1 is : {}'.format(valPoly(rac1,zeros)))
    print('Rac1 indice in the zeros is : {}'.format(nearestIndice(rac1,zeros)))

def dessine(zeros):
    IndTimer = 0
    mat = np.empty([2001,2001],dtype=np.int8, order='C') # C-style [lig][col]

    for i in range(0,2000+1):
        curIndTimer = i*100 // 2000
        if curIndTimer != IndTimer:
            IndTimer = curIndTimer
            print("{}% ".format(curIndTimer),end='')
            sys.stdout.flush()
        for j in range(-1000,1000+1):
            p = (i/250)-4 + 1j*j/250
            rac1 = newt(p,zeros)
            res  =  nearestIndice(rac1,zeros)
            lig = 2000-(1000+j)
            col = i
            mat[lig][col] = res

    plt.matshow(mat)
    plt.axis(True)
    plt.cool()
    plt.title('Newtown Matrix {} roots'.format(len(zeros)))
    plt.colorbar()
    plt.show()

zeros = [1+0j,sqrt(3)*1j,-1+0j]
test(zeros)
dessine(zeros)
