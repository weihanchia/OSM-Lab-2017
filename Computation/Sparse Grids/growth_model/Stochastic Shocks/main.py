#======================================================================
#
#     This routine solves an infinite horizon growth model
#     with dynamic programming and sparse grids
#
#     The model is described in Scheidegger & Bilionis (2017)
#     https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2927400
#
#     external libraries needed:
#     - IPOPT (https://projects.coin-or.org/Ipopt)
#     - PYIPOPT (https://github.com/xuy/pyipopt)
#     - TASMANIAN (http://tasmanian.ornl.gov/)
#
#     Simon Scheidegger, 11/16 ; 07/17
#======================================================================

import nonlinear_solver_initial as solver     #solves opt. problems for terminal VF
import nonlinear_solver_iterate as solviter   #solves opt. problems during VFI
from parameters import *                      #parameters of model
import interpolation as interpol              #interface to sparse grid library/terminal VF
import interpolation_iter as interpol_iter    #interface to sparse grid library/iteration
import postprocessing as post                 #computes the L2 and Linfinity error of the model

import TasmanianSG                            #sparse grid library
import numpy as np


#======================================================================
# Start with Value Function Iteration

# terminal value function
if (numstart==0):
    valnew = {}
    for i in range(len(theta)):
        valnew[str(i)]=TasmanianSG.TasmanianSparseGrid()
        valnew[str(i)] = interpol.sparse_grid(n_agents, iDepth, refinement_level, fTol, i)
        valnew[str(i)].write("valnew_" + str(i) + str(numstart) + ".txt") #write file to disk for restart
# value function during iteration
else:
    valnew = {}
    valold = {}
    for i in range(len(theta)):
        valnew[str(i)].read("valnew_" + str(i) + str(numstart) + ".txt")  #write file to disk for restart
        valold[str(i)]=TasmanianSG.TasmanianSparseGrid()
        valold[str(i)]=valnew[str(i)]

valold=valnew

for i in range(numstart, numits):
    valnew = {}
    for k in range(len(theta)):
        valnew[str(k)]=TasmanianSG.TasmanianSparseGrid()
        valnew[str(k)]=interpol_iter.sparse_grid_iter(n_agents, iDepth, refinement_level, fTol, valold, k)
        valnew[str(k)].write("valnew_"+ str(k) + str(i+1) + ".txt")
    for j in range(len(theta)):
        valold[str(j)]=TasmanianSG.TasmanianSparseGrid()
        valold[str(j)]=valnew[str(j)]

#======================================================================
print "==============================================================="
print " "
print " Computation of a growth model of dimension ", n_agents ," finished after ", numits, " steps"
print " "
print "==============================================================="
#======================================================================

# compute errors
for i in range(len(theta)):
    avg_err = {}
    avg_err['str(i)']=post.ls_error(n_agents, numstart, numits, No_samples, i)

#======================================================================
print "==============================================================="
print " "
print " Errors are computed -- see errors.txt"
print " "
print "==============================================================="
#======================================================================
