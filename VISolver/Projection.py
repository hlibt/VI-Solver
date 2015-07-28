import numpy as np

from VISolver.Utilities import MachineLimit_Exp


class Projection(object):

    def P(self):
        '''This function projects the data.'''
        raise NotImplementedError(
            'Base classes of Projection must override the P method')


class IdentityProjection(Projection):

    def P(self,Data,Step,Direc):
        return Data+Step*Direc


class RPlusProjection(Projection):

    def P(self,Data,Step,Direc):
        return np.maximum(0,Data+Step*Direc)


class EntropicProjection(Projection):

    def P(self,Data,Step,Direc):
        ProjectedData = Data*np.exp(MachineLimit_Exp(Step,Direc)*Direc)
        return ProjectedData/np.sum(ProjectedData)


class EuclideanSimplexProjection(Projection):

    #Taken from: https://gist.github.com/daien/1272551
    def P(self,Data,Step,Direc,s=1):
        assert s > 0, "Radius s must be strictly positive (%d <= 0)" % s
        Data = Data + Step*Direc
        n, = Data.shape  # will raise ValueError if Data is not 1-D
        # check if we are already on the simplex
        if Data.sum() == s and np.alltrue(Data >= 0):
            # best projection: itself!
            return Data
        # get the array of cumulative sums of a sorted (decreasing) copy of Data
        u = np.sort(Data)[::-1]
        cssd = np.cumsum(u)
        # get the number of > 0 components of the optimal solution
        rho = np.nonzero(u * np.arange(1, n+1) > (cssd - s))[0][-1]
        # compute the Lagrange multiplier associated to the simplex constraint
        theta = (cssd[rho] - s) / (rho + 1.0)
        # compute the projection by thresholding Data using theta
        w = (Data - theta).clip(min=0)
        return w


class LyapunovGSRProjection(Projection):

    def P(self,Data,Step,Direc):
        # figure out intelligent slicing later
        # this only works with euler - the other ones update Domain.Lyapunov
        # multiple times per update which is wrong
        psi = Data[2:].reshape(2,2)
        psi, R = np.linalg.qr(psi)
        Data[2:] = psi.flatten()
        return Data+Step*Direc
