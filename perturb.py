import numpy as np
from scipy import ndimage
from scipy.constants import value as c

s = 200
w = 1 * c(u'Bohr radius')
h = c(u'Planck constant')
m_e = c(u'electron mass')
e = c(u'Planck constant')
e_0 = c(u'vacuum electric permittivity')
eV = c(u'Planck constant')

def indexToLoc(i,j,k):
    loc = np.zeros(3)
    loc[0] = (i/s - 1/2)*w
    loc[1] = (j/s - 1/2)*w
    loc[2] = (k/s - 1/2)*w
    return loc 

print( str(indexToLoc(60,2,18)))

def hamiltonian(wfc):
    coeff1 = -h**2/(8 * np.pi**2 * m_e)
    coeff2 = -e**2/(4*e_0*np.pi)
    wfc2 = np.zeros((s,s,s))
    #wfc2.fill(0)
    wfc2 = np.add(coeff1*ndimage.filters.laplace(wfc, mode='constant', cval = 0.0), coeff2*hydrogenPot(wfc))
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
    for i in range(0,len(grid)):
        for j in range(0,len(grid)):
            for k in range(0,len(grid)):
                loc = indexToLoc(i,j,k)
                if(loc[0] != 0 and loc[1] != 0 and loc[2] != 0):
                    grid[i][j][k] = wfc[i][j][k] * (1/(loc.dot(loc)))
                else:
                    grid[i][j][k] = wfc[i][j][k] * 10000000000
    return grid 
    


wfc = np.random.rand(s,s,s) 
#print("initial norm: "+ str(measure(wfc)))
wfc = wfc * 1/measure(wfc) 
#print("norm: "+ str(measure(wfc)))

#wfc2 = wfc.copy()

# main loop
for i in range(1,20):
    wfc2 = hamiltonian(wfc)
    E = innerProd(wfc,wfc2)
    wfc2 = wfc2 * 1/measure(wfc2)
    print("eigenval = " + str(E/eV))
    #print("eigenval = " + str(E/eV))
    #print(str(E/c(u'electron volt')))
    wfc = wfc2.copy()
    #print("<wfc3|wfc3> = " + str(innerProd(wfc,wfc)))








#for i in space:
#    for j in space:
#        for k in space: 
