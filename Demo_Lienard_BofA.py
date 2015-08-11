# import time
import numpy as np

from VISolver.Domains.Lienard import Lienard

# from VISolver.Solvers.Euler_LEGS import Euler_LEGS
from VISolver.Solvers.HeunEuler_LEGS import HeunEuler_LEGS
# from VISolver.Solvers.AdamsBashforthEuler_LEGS import ABEuler_LEGS
# from VISolver.Solvers.CashKarp_LEGS import CashKarp_LEGS

from VISolver.Solver import Solve
from VISolver.Options import (
    DescentOptions, Miscellaneous, Reporting, Termination, Initialization)
from VISolver.Log import PrintSimStats

from VISolver.Utilities import ListONP2NP, aug_grid, MCLE_BofA_ID_par

from matplotlib import pyplot as plt
from IPython import embed


def Demo():

    #__CLOUD_SERVICES__##################################################

    # Define Network and Domain
    Domain = Lienard()

    # Set Method
    # Method = Euler_LEGS(Domain=Domain)
    Method = HeunEuler_LEGS(Domain=Domain,Delta0=1e-5)
    # Method = ABEuler_LEGS(Domain=Domain,Delta0=1e-4)
    # Method = CashKarp_LEGS(Domain=Domain,Delta0=1e-6)

    # Set Options
    Init = Initialization(Step=1e-5)
    Term = Termination(MaxIter=1e5)
    Repo = Reporting()
    Misc = Miscellaneous()
    Options = DescentOptions(Init,Term,Repo,Misc)
    args = (Method,Domain,Options)
    sim = Solve

    # Print Stats
    PrintSimStats(Domain,Method,Options)

    # grid = [np.array([-2.5,2.5,51])]*2
    grid = [np.array([-2.5,2.5,167])]*2
    grid = ListONP2NP(grid)
    grid = aug_grid(grid)
    Dinv = np.diag(1./grid[:,3])

    results = MCLE_BofA_ID_par(sim,args,grid,nodes=25,limit=40,AVG=.01,
                               eta_1=1.2,eta_2=.95,eps=1.,
                               L=50,q=2,r=1.1,Dinv=Dinv)
    ref, data, p, i, avg = results

    for sample in data[hash(str(ref[0]))]:
        plt.plot([sample[0][0]],[sample[0][1]],'*r')
        plt.plot([sample[1][0]],[sample[1][1]],'ob')
    ax = plt.gca()
    ax.set_xlim([-3,3])
    ax.set_ylim([-3,3])
    plt.savefig('bndry_pts.png',format='png')

    embed()

if __name__ == '__main__':
    Demo()
