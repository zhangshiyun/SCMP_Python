import numpy as np
from numpy import *
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle

pi,sin,cos = np.pi, np.sin, np.cos

def mkconfig(filename):
    xyd = np.loadtxt(filename)
    dim = xyd.shape
    nOfp = dim[0]
    xmax = int(np.amax(xyd))+1.5
    xmin = int(np.amin(xyd))-1.5

    theta = np.linspace(0,2*pi,64)
    fig = plt.figure(dpi=200)
    ax = fig.add_subplot(111,aspect='equal')
    ax.set_xlim((xmin,xmax))
    ax.set_ylim((xmin,xmax))

    for i in range(nOfp):
        rx = xyd[i,0]
        ry = xyd[i,1]
        d = xyd[i,2]/2.
        if (2*d==1):
            tcir = Circle(xy=(rx,ry),radius=d,color='r',alpha=0.3)
        else:
            tcir = Circle(xy=(rx,ry),radius=d,color='b',alpha=0.3)
        ax.add_patch(tcir)
    fig.savefig('ra1.png')
    plt.show()

def mkconfig1(filename):
    xyd = np.loadtxt(filename)
    dim = xyd.shape
    nOfp = dim[0]
    xmax = int(np.amax(xyd)) + 1.5
    xmin = int(np.amin(xyd)) - 1.5

    fig = plt.figure(dpi=200)
    ax = fig.add_subplot(111,aspect='equal')
    ax.set_xlim((xmin,xmax))
    ax.set_ylim((xmin,xmax))

    for i in range(nOfp):
        rx = xyd[i,0]/0.9
        ry = xyd[i,1]
        d = xyd[i,2]
        if (d==1):
            tcir = Circle(xy=(rx,ry),radius=d/2.0,color='r',alpha=0.3)
        else:
            tcir = Circle(xy=(rx,ry),radius=d/2.0,color='b',alpha=0.3)
        ax.add_patch(tcir)
    fig.savefig('ra2.png')
    plt.show()

def filenamelist(filename):
    fr = open(filename)
    nlines = len(fr.readlines())
    namelist = []
    fr = open(filename)
    for line in fr.readlines():
        namelist.append(line[:-1])
    fr.close()
    return namelist, nlines

def findsoft(drxyfile,strfeatfile,softStrfeat,indexsoft):
    drxy = np.loadtxt(drxyfile)
    n = len(drxy)
    strfeat = np.loadtxt(strfeatfile)
    for i in range(n):
        if drxy[i]<5 :
            if drxy[i]>1:
                softStrfeat[indexsoft,:] = strfeat[i,:]
                indexsoft += 1
    return softStrfeat, indexsoft

def findhard(drxyfile,strfeatfile,hardStrfeat,indexhard,indexsoft):
    drxy = np.loadtxt(drxyfile)
    n = len(drxy)
    strfeat = np.loadtxt(strfeatfile)
    for i in range(n):
        if drxy[i]<0.8 and indexhard<indexsoft :
            hardStrfeat[indexhard,:] = strfeat[i,:]
            indexhard += 1
    return hardStrfeat, indexhard

def svmdataformat(rawarray,filename,label0):
    dim = rawarray.shape
    for i in range(dim[0]):
        with open(filename,'a+') as f:
            label = str(label0)
            data = label + ' '
            f.write(data)
        for j in range(dim[1]):
            with open(filename,'a+') as f:
                order = str(j+1)
                temp = str(rawarray[i,j])
                if j+1 == dim[1]:
                    data = order + ':' + temp + '\n'
                else:
                    data = order + ':' + temp + ' '
                f.write(data)
    f.close()

def maintran(formatname,drxyfile,strfeatfile):
    drxynamelist, ndrxy = filenamelist(drxyfile)
    strfeatnamelist, nstrfeat = filenamelist(strfeatfile)
    print "We have %d drxyfiles and %d strfeatfiles." %(ndrxy,nstrfeat)
    print "The two number should be equal."
    soft = zeros((10000,160))
    hard = zeros((10000,160))
    indexsoft = 0
    indexhard = 0
    for i in range(ndrxy):
        soft, indexsoft = findsoft(drxynamelist[i],strfeatnamelist[i],soft,indexsoft)
        hard, indexhard = findhard(drxynamelist[i],strfeatnamelist[i],hard,indexhard,indexsoft)
    print "There are %d softspots and %d hardspots we choosed." %(indexsoft,indexhard)
    print "we want numbers be equal.for now."
    softspots = zeros((indexsoft,160))
    hardspots = zeros((indexhard,160))
    for i in range(indexsoft):
        softspots[i,:] = soft[i,:]
    for i in range(indexhard):
        hardspots[i,:] = hard[i,:]
    svmdataformat(softspots,formatname,1)
    svmdataformat(hardspots,formatname,0)

