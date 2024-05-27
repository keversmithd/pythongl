import numpy as np
import math
class bayesian_quad:
    def __init__(self):
        self.prior_belief = 0
        self.time_frame = [0,20]

        self.dimension = 3

        self.X = np.array(3)
        pass

    def f(x):
        return x[0]+x[1]+x[2]
    
    def mean(self):
        # how likely we are to observe certain function values 
        # our prior belief about the output of the function
        return self.prior_belief

    
    def distribution(self, x):
        lam = self.mean()/(self.time_frame[1]-self.time_frame[0])

        return math.e**(-lam)*(lam**x/math.factorial(x))
    
    def likelihood_dist(self, x,x_new):
    
        x_trans = math.e**(-1/2*x**(self.mean()))/4*math.pi @ self.covariance(x,x_new)

    def likelihood(self, new_X, old_value):
        # based on the sampling the function as certain points
        self.f(new_X) 

        return
    
    def posterior(self, X_new):
        # Compute the covariance matrix between the observed points and the new points
        K = self.covariance(self.X, self.X)
        K_s = self.covariance(self.X, X_new)
        K_ss = self.covariance(X_new, X_new)

        K_inv = np.linalg.inv(K)

        # Compute the posterior mean and covariance
        mu_s = self.mean(X_new) + K_s.T.dot(K_inv).dot(self.y - self.mean(self.X))
        cov_s = K_ss - K_s.T.dot(K_inv).dot(K_s)

        return mu_s, cov_s

    def covariance(self, x, y):
        # measures the euclidian distance between points, appplies square exponetial to it
        # Hyperparameters for the covariance function
        sigma_f = 1.0  # Signal variance
        l = 1.0  # Length scale

        sqdist = np.sum(x**2, 1).reshape(-1, 1) + np.sum(y**2, 1) - 2 * np.dot(x, y.T)
        return sigma_f**2 * np.exp(-0.5 / l**2 * sqdist)
        
    def estimate(self, X_new):
        # the expected value of the function
        # integrate the function by integrating the probability mass function
        # provide level of uncertainty
        mu_s, cov_s = self.posterior(X_new)
        return mu_s, np.diag(cov_s)
    

    def update(self, new_X, new_y):
        # update the prior belief based on the observed function values
        self.likelihood(new_X,new_y)
        return
    
    def prior(self,x):
        mean = self.mean()
        cov = self.covariance(x,x)
        return mean,cov
        
        