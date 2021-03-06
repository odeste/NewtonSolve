import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import sys # to use stdout flush
import cmath # to use complex numbers. j^2 = -1 (caevat not j^3)
from cmath import sqrt
from math import pow

NBFRAMES = 1200
DIMH = 567
DIMV = 567
ficName = r"C://Users/Public/Videos/animation.mp4"
ficName = r"./animation.mp4"

def valPoly (p,zeros):
    """ :returns f(x) where f is (x-r0)*(x-r1)*(x-r2)... where r0,r1... are given in zeros
    p : float or complex
    zeros : list of floats or complexes"""
    res = 1.0
    for r in zeros:
        res *= (p-r)
    return(res)

def valDeriv(p,zeros):
    """ :returns f'(x) where f is (x-r0)*(x-r1)*(x-r2)... where r0,r1... are given in zeros
    i.e gives the value of the derivative of valPoly at point p
    p : float or complex
    zeros : list of floats or complexes"""
    res = 0.0
    for i in range(len(zeros)):
        acc = 1
        for  j in range(len(zeros)):
            if i != j:
                acc *= (p-zeros[j])
        res += acc
    return(res)

def newt (p,zeros,epsilon):
    """ :returns one approximative root of valPoly using newtown methods and also return nb of iterations.
    First guess is p
    p : float or complex
    zeros : list of floats or complexes beeing the true roots """
    cpt = 0
    remain=valPoly (p,zeros)
    cont = True

    while cont:
        deriv =  valDeriv (p,zeros)
        p -= remain / deriv # TODO do not divide by zero

        cpt += 1
        remain=valPoly (p,zeros)
        cont =  (abs(remain) > epsilon)
    return (p,cpt)

def nearestIndice(p,lp):
    """ :returns indice in lp of the lp[] that is the nearest to p.
    p : float or complex
    lp : list of floats or complexes """
    res = -1
    distMin = 9466 #any value will be overided
    for i in range(len(lp)):
        dist = abs(p-lp[i])
        if (res == -1) or (dist<distMin):
            res = i
            distMin=dist
    return res

def test():
    """ tests the previous functions and print some results """
    zeros = [1+0j,sqrt(3)*1j,-1+0j]
    p = -10
    print('The poly val is: {}'.format(valPoly(p,zeros)))
    print('The deriv val is: {}'.format(valDeriv(p,zeros)))
    (rac1, cpt) = newt(p,zeros,1e-18)
    print('Rac1 is : {} it was found after {} iterations.'.format(rac1,cpt))
    print('Poly val for rac1 is : {}'.format(valPoly(rac1,zeros)))
    print('Rac1 indice in the zeros is : {}'.format(nearestIndice(rac1,zeros)))


mat = np.empty([DIMH, DIMV], dtype=np.int8, order='C') # C-style [lig][col]

fig, ax = plt.subplots()
dessin = ax.matshow(mat, vmin=0, vmax=99, origin='lower', aspect='equal')
ax.set_title("Which root Newton's method find first")
ax.set_visible(True)

def dessine(zeros, xMin, xMax, yMin, yMax):

    IndTimer = 0

    for h in range(0, DIMH):
        x = xMin+h*(xMax-xMin)/(DIMH - 1)

        #From times to times, print the % of completion
        curIndTimer = h * 10 // DIMH
        if (curIndTimer != IndTimer):
            IndTimer = curIndTimer
            print("{}0% ".format(IndTimer),end='')
            sys.stdout.flush()

        for v in range(0, DIMV):
            y = yMin+v*(yMax-yMin)/(DIMV - 1)
            p = x + 1j*y
            (rac1,cpt) = newt(p,zeros,1e-4)
            racInd  =  nearestIndice(rac1,zeros)
            mat[v][h] = racInd
            mat[v][h] = cpt

    dessin.set_array(mat)

def anim(i):
    zeros = [1+0j,sqrt(3)*1j,-1+0j]
    xCenter = 1.0615075438391
    yCenter = 1.433647289170145
    halfSize = 16*(0.987654321) * pow(0.5, (i/25))
    print ('\nRemaing frame(s) : {rf:5} Half size is {hs:.9} '.format(rf = NBFRAMES-i, hs=halfSize), end='')
    dessine(zeros, xCenter-halfSize, xCenter+halfSize, yCenter-halfSize, yCenter+halfSize)
    if (NBFRAMES-i <= 1):
        print ('\nNewtown Matrix {} roots'.format(len(zeros)))
        print ('Center is {xc:+.12f} +  {xc:+.12f} i. Window size being {ws:+.12f}'.format(xc=xCenter, yc=yCenter, ws=2*halfSize ))

#print ('Preview of the last frame. Please close it')
#anim(NBFRAMES)
#plt.show()

fic = open(ficName,"w")
ani = animation.FuncAnimation(fig, anim, frames=NBFRAMES, interval=40, repeat=False)
print ("ffmpeg shall be installed before using this code. Tentative de creation du fichier video ",ficName )
writervideo = animation.FFMpegWriter(fps=25)
ani.save(ficName, writer=writervideo)