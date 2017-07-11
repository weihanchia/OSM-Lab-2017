# Import packages
import numpy as np
import matplotlib.pyplot as plt
import numba

def pi2(k, z, w, r, params):
    alpha_k, alpha_l, delta, psi, beta, h = params
    return alpha_k * ((alpha_l / w)) ** (alpha_l / (1 - alpha_l)) * z ** (1 / (1 - alpha_l)) * \
           k ** ((alpha_k + alpha_l - 1)/(1 - alpha_l))

def c2(kprime, k, w, r, params):
    alpha_k, alpha_l, delta, psi, beta, h = params
    return (psi / 2) * (2*(kprime - (1 - delta)*k)*(delta - 1)*k - (kprime - (1 - delta)*k)**2)/(k**2)
# Define inverse function to get k

def kinv(kprime, expectedvalue,w, r, params):
    alpha_k, alpha_l, delta, psi, beta, h = params
    return ( psi * kprime )/( beta * expectedvalue + psi*(1 - delta) - 1)

def egpsolve(kvec, zvec, pi, w, r, params, tol=1e-06, maxiter=3000):
    '''
    kvec = k by 1 Vector of Capital Grid
    zvec = z by 1 Vector of Shock grid
    pi = Transition Probabilities
    params = Other exogenous parameters
    tol = tolerance of error
    maxiter = maximum number of iterations

    Purpose: Solving for policy functions for firms facing stochastic shocks and
    quadratic adjustment costs using EGP method

    Returns: k by z vector of optimal choice of kprime in the next period'''
    alpha_k, alpha_l, delta, psi, beta, h = params
    size_k = kvec.shape[0]
    size_z = zvec.shape[0]
    PFtol = tol
    PFdist = 7.0
    PFmaxiter = maxiter
    kchoice = np.arange(0, size_k, 1)
    PF = np.reshape(np.repeat(kchoice, 9, axis=0), (size_k, size_z))  # k by z size matrix of indexes
    PF = kvec[PF] # Initial guess of policy function
    kinvgrid = np.zeros(size_k) # Grid to store inverted K values
    kprimeprime = np.zeros(size_z) # Grid of second period choice of investment
    PFiter = 1

    while PFdist > PFtol and PFiter < PFmaxiter:
        TPF = np.copy(PF)
        for j in range(size_z): # Loop over z
            for i in range(size_k): # Loop over k
                for k in range(size_z): # Loop over z'
                    kprimeprime[k] = np.interp(TPF[i,j], kvec, TPF[:,k])
                expectedvalue = (pi2(TPF[i,j], zvec, w, r, params) + (1 - delta) - c2(kprimeprime,TPF[i,j], w, r,params)).dot(pi[:,j])
                kinvgrid[i] = kinv(TPF[i,j], expectedvalue, w, r, params)
            PF[:,j] = np.interp(kvec, kinvgrid, TPF[:,j])
        PFdist = (np.absolute(PF - TPF)).max()
        PFiter += 1

    return PF  # solution to the functional equation
