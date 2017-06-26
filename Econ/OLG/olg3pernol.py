# We will write a script to solve for the OLG model

import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt


class olg3pernol(object):

    def __init__(self, lvec, args):
        # We take all model parameters, as well as the exogenous
        # labor supply as initial inputs when defining the model class
        beta, sigma, A, alpha, delta = args
        self.ntot = lvec.sum()
        self.beta = beta ** 20
        self.sigma = sigma
        self.A = A
        self.alpha = alpha
        self.delta =1 - ((1 - delta) ** 20)

    def __str__(self):
        #Define this to print key parameters of the model
        return "\033[4mIndividual Parameters:\033[0m\nDiscount Rate:\t" + str(self.beta) + \
        "\nRelative Risk Aversion:\t" + str(self.sigma) + \
        "\nFirm Parameters: \nTechnology:\t" + str(self.A) + \
        "\nCapital Share:\t" + str(self.alpha) + \
        "\nDepreciation:\t" + str(self.delta)

    def MUC(self, consumption):
        #Function to compute marginal utility given consumption
        return consumption ** (- self.sigma)

    def get_r(self, K):
        #Solving for r using firm FOC
        return self.alpha * self.A * (self.ntot / K) ** (1 - self.alpha) - self.delta

    def get_w(self, K):
        #Solving for w using firm FOC
        return (1 - self.alpha) * self.A * (K / self.ntot) ** (self.alpha)

    def get_c(self, bvec, Kvec):
        #Solving for c using budget constraint
        res = np.ones((3))
        r2 = self.get_r(Kvec[1])
        r3 = self.get_r(Kvec[2])
        w1 = self.get_w(Kvec[0])
        w2 = self.get_w(Kvec[1])
        w3 = self.get_w(Kvec[2])
        res[0] = w1 - bvec[0]
        res[1] = w2 + (1 + r2)*bvec[0] - bvec[1]
        res[2] = 0.2*w3 + (1 + r3)*bvec[1]
        return res

    def eulererror(self, bvec, Kvec):
        #Using Euler Equation System to back out Errors
        c = self.get_c(bvec, Kvec)
        res = np.ones((2))
        r2 = self.get_r(Kvec[1])
        r3 = self.get_r(Kvec[2])
        res[1] = self.MUC(c[1]) - self.beta*(1 + r3)*self.MUC(c[2])
        res[0] = self.MUC(c[0]) - self.beta*(1 + r2)*self.MUC(c[1])
        return res

    def eulererror3(self, b2, b1, Kvec):
        bvec = np.array([b1,b2])
        c = self.get_c(bvec, Kvec)
        res = np.ones((2))
        r2 = self.get_r(Kvec[1])
        r3 = self.get_r(Kvec[2])
        res = self.MUC(c[1]) - self.beta*(1 + r3)*self.MUC(c[2])
        return res

    def eulererror2(self, bvec):
        #Wrapper around Euler Error for SS
        Kvec = np.ones((3))
        Kvec= Kvec*(bvec[0] + bvec[1])
        return self.eulererror(bvec, Kvec)

    def ss(self, b_init):
        #Solves SS and stores SS attributes
        ans = opt.root(self.eulererror2, b_init)
        self.bss = ans.x
        Kvec = np.ones((3))*sum(ans.x)
        self.rss = self.get_r(sum(ans.x))
        self.kss = self.bss.sum()
        self.wss = self.get_w(sum(ans.x))
        self.css = self.get_c(self.bss, Kvec)
        print("\033[4mSteady State\033[0m\nSecond/Third Period Saving:\t" + str(self.bss) + \
              "\nConsumption:\t" + str(self.css) + \
              "\nWages:\t" + str(self.wss) + \
              "\nRental Rate:\t" + str(self.rss))

    def policymulti(self, bguess, Kvec):
        #Policy Function given K
        b_init = bguess
        bres = opt.root(self.eulererror, b_init, args=(Kvec))
        return bres.x

    def policy2per(self, b1, b2guess, Kvec):
        b1 = b1
        b = b2guess
        bres = opt.root(self.eulererror3, b, args=(b1, Kvec))
        return bres.x

    def perturb(self, bvec, chi = 0.5, epsilon = 1e-12, T = 100, maxiter = 100):
        # Gives transition to the steady state from some given endowments
        bres = np.ones((T+2,2)) #Initialize savings path
        bres[0,0] = bvec[0]
        bres[0,1] = bvec[1]
        # Here, because of the overlapping grids and the need for
        #K1, K2, K3 to precdict household savings, we initialize some savings
        #at the steady state values
        bres[T,0] = self.bss[0]
        bres[T,1] = self.bss[1]
        bres[T+1,0] = self.bss[0]
        bres[T+1,1] = self.bss[1]
        bres[T-1,0] = self.bss[0]
        kinit = bvec[0] + bvec[1]
        kvec = np.linspace(kinit,self.kss, T+2)
        it = 0
        error = 100
        bguess = self.bss

        while error > epsilon and it < maxiter:
            #Solve the time path iteration
            tempk = kvec[0:3]
            bt2 = bres[0,0]
            bres[1,1] = self.policy2per(bt2,bguess[1],tempk)
            for t in range(0,T-2):
                tempk = kvec[t:t+3]
                bres[t+1,0] = self.policymulti(bguess, tempk)[0]
                bres[t+2,1] = self.policymulti(bguess, tempk)[1]
            knew = bres.sum(axis=1)
            error = np.linalg.norm(knew - kvec)
            kvec = chi* kvec + (1- chi)*knew
            print("Iteration number: " + str(it) + " Error: " +str(error))
            it += 1

        return bres
