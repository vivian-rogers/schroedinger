import numpy as np
from scipy import ndimage
from scipy.constants import value as c


import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

fig = mpl.pyplot.figure(figsize=(12,9))
ax1 = fig.add_subplot(111,projection='3d')

s = 61
widthbohr = 10
w = widthbohr * c(u'Bohr radius')
h = c(u'Planck constant')
m_e = c(u'electron mass')
e = c(u'atomic unit of charge')
e_0 = c(u'vacuum electric permittivity')
eV = c(u'electron volt')

h = 2*np.pi
e = 1
m_e = 1
w = widthbohr
hbar = h/(2*np.pi)


def indexToLoc(i,j,k):
    loc = np.zeros(3)
    loc[0] = (i/s - 1/2)*widthbohr
    loc[1] = (j/s - 1/2)*widthbohr
    loc[2] = (k/s - 1/2)*widthbohr
    return loc 

#print( str(indexToLoc(49,50,51)))

def hamiltonian(wfc):
    coeff1 = -hbar**2/(2 * m_e)
    coeff2 = -e**2/(4*e_0*np.pi)
    #c1 = -1 / (2*m_e)
    wfc2 = np.zeros((s,s,s))
    #wfc2.fill(0)
    #wfc2 = ndimage.filters.laplace(wfc, mode='constant', cval = 0.0)
    #wfc2 = np.add(coeff1*ndimage.filters.laplace(wfc, mode='constant', cval = 0.0), coeff2*hydrogenPot(wfc))
    wfc2 = np.add((-1/2)*ndimage.filters.laplace(wfc, mode='constant', cval = 0.0), (1)*hydrogenPot(wfc))
    #wfc2 = -(1)*hydrogenPot(wfc)
    #i = int(s/4)
    #print("<wfc2|wfc2> = " + str(measure(wfc2)) + ", <wfc1|wfc1> = " + str(measure(wfc))) 
    #E = innerProd(wfc,wfc2)
    #wfc2 = 10**19 * wfc2 
    return wfc2



def measure(wfc):
    return np.sqrt(innerProd(wfc,wfc))

def innerProd(wfc,wfc2):
    sum = 0
    for i in range(0,s):
        for j in range(0,s):
            for k in range(0,s):
                sum += wfc[i][j][k]*wfc2[i][j][k]
    return sum


def hydrogenPot(wfc):
    grid = np.zeros((s,s,s))
    err = 10 ** (-3)
    for i in range(0,len(grid)):
        for j in range(0,len(grid)):
            for k in range(0,len(grid)):
                loc = indexToLoc(i,j,k)
                #if(loc[0] != 0 and loc[1] != 0 and loc[2] != 0):
                pot = (1/(err + np.sqrt(loc.dot(loc))))
                #if(k < s): 
                #    grid[i][j][k] += 10
                grid[i][j][k] = wfc[i][j][k] * pot
                #else:
                #    grid[i][j][k] = wfc[i][j][k] * 10000000000
    return grid 
    


def plotSlice(wfc,filename):
    k = int(s / 2) + 1
    x = []
    y = []
    z = []
    print('Plotting ' + filename + "\n")
    for i in range(0,s):
        for j in range(0,s):
            xval = widthbohr*(i - s/2)/s
            yval = widthbohr*(j - s/2)/s
            x.append(xval)
            y.append(yval)
            z.append(np.log10(wfc[i][j][k]*wfc[i][j][k]))
    #surface = ax1.plot_trisurf(x,y,z, norm=mpl.colors.LogNorm(), cmap='inferno', linewidth=0.01, antialiased=False)
    surface = ax1.plot_trisurf(x,y,z, norm=mpl.colors.Normalize(), cmap='inferno', linewidth=0.01, antialiased=False)
    #fig.colorbar(surface, shrink=0.5, aspect=5)
    ax1.set_xlabel('X (bohr radii)')
    ax1.set_ylabel('Y (bohr radii)')
    ax1.set_zlabel('Log10(Ψ*Ψ)')
    plt.savefig("./results/" + filename)
    plt.cla()


Emin = (1+1+1)/(2*m_e*widthbohr**2) 
print("Predicted: " + str(Emin / eV))
wfc = np.random.rand(s,s,s) 
#wfc = np.ones((s,s,s))
#print("initial norm: "+ str(measure(wfc)))
wfc = wfc * 1/measure(wfc) 
#print("norm: "+ str(measure(wfc)))

#wfc2 = wfc.copy()
E2 = -10 ** (-40)
rat = 100
i = 0
# main loop
while (abs(rat) > 10**(-15)):
    filename = "slice" + str(i) + ".png"
    wfc2 = hamiltonian(wfc)
    E = innerProd(wfc,wfc2)
    wfc2 = wfc2 * 1/measure(wfc2)
    print("eigenval = " + str(E))
    rat = 100 * (E - E2)/ E2
    E2 = E
    print("ratio = " + str(rat))
    #print("eigenval = " + str(E/eV))
    #print(str(E/c(u'electron volt')))
    wfc = wfc2.copy()
    #if (i % 3 == 0):
    plotSlice(wfc, filename)
    i += 1
    #print("<wfc3|wfc3> = " + str(innerProd(wfc,wfc)))







#for i in space:
#    for j in space:
#        for k in space: 
