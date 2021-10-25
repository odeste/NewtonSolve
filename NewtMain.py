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
    dimH = 1001
    dimV = 1001
    (xMin, xMax) = (0.7, 1.6)
    (yMin, yMax) = (0.8, 1.7)
    mat = np.empty([dimH,dimV],dtype=np.int8, order='C') # C-style [lig][col]
    for h in range(0, dimH):
        x = xMin+h*(xMax-xMin)/(dimH-1)

        #From times to times, print the % of completion
        curIndTimer = h * 100 // dimH
        if curIndTimer != IndTimer:
            IndTimer = curIndTimer
            print("{}% ".format(curIndTimer),end='')
            sys.stdout.flush()

        for v in range(0, dimV):
            y = yMin+v*(yMax-yMin)/(dimV-1)
            p = x + 1j*y
            rac1 = newt(p,zeros)
            res  =  nearestIndice(rac1,zeros)
            mat[v][h] = res

    plt.matshow(mat, origin='lower', aspect='equal')
    plt.axis(True)
    plt.suptitle('Newtown Matrix {} roots'.format(len(zeros)))
    plt.title('real:[{xmin} to {xmax}] and img:[{ymin} to {ymax}] '.format(xmin=xMin,xmax=xMax,ymin=yMin,ymax=yMax))
    plt.colorbar()
    plt.show()

zeros = [1+0j,sqrt(3)*1j,-1+0j]
test(zeros)
dessine(zeros)
