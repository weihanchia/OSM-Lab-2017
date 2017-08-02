# necessary import for every use of TASMANIAN
#
import TasmanianSG
import numpy as np
from random import uniform
import math

grid = TasmanianSG.TasmanianSparseGrid()

# Generate Parameters for test functions
w1 = uniform(-1.0,1.0)
c = np.empty(2)
for i in range(2):
    c[i] = uniform(0,10)

# Loop over number of points
avec = np.arange(100,1000,100)
fError = np.empty(len(avec))
for k in range(len(avec)):
    # Result
    aPnts = np.empty((avec[k],2))
    for iI in range(avec[k]):
        for iJ in range(2):
            aPnts[iI,iJ] = uniform(-1.0,1.0)
    aTres = np.empty(avec[k])
    for iI in range(avec[k]):
        aTres[iI] = math.cos(2*math.pi*w1 + np.dot(c, aPnts[iI,:]))

    #Construting Sparse grids
    iDim  = 2
    iOut = 1
    iDepth = 5
    which_basis = 1
    grid.makeLocalPolynomialGrid(iDim, iOut, iDepth, which_basis, "localp")
    aPoints = grid.getPoints()
    iNumP1 = aPoints.shape[0]
    aVals = np.empty([aPoints.shape[0], 1])
    for iI in range(aPoints.shape[0]):
        aVals[iI] =  math.cos(2*math.pi*w1 + np.dot(c, aPoints[iI,:]))
    grid.loadNeededPoints(aVals)

    # Compute Errors
    aRes = grid.evaluateBatch(aPnts)
    fError[k] = max(np.fabs(aRes[:,0] - aTres))

# Print out Errors for plotting
f=open("errors_oscillatory.txt",'w')
np.savetxt(f, fError, fmt = '% 2.16f')
f.close()
