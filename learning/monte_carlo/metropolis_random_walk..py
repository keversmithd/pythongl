# Dustin Kever-SMith and Richard G Bailey
# 2020-07-01
#Simulates cheesburger density
import numpy as np
import pandas as pd
import os
# should be fixed with a graph like model this doesn't make any sense.
class metropolis_hastings_gaussian:

    def __init__(self):

        # define dimensionality of the problem
        self.number_of_states = 4
        self.state_names = {0: "bun", 1: "cheese", 2: "patty", 3: "lettuce"}

        # N is the number of steps to take
        self.number_steps = 10
        # epsilon is the tuning paramter which sets the variance in the dimensions
        self.constant_variance = 0.1
        self.covariance = np.full(self.number_of_states, self.constant_variance)
        
        return
    
    def proposal_distribution(self, current_state, proposed_state = None):
        # some kind of space, or context or graph etc, and we would traverse our options and return a vector with respect of the current
        if(proposed_state != None):
            return np.random.multivariate_normal(proposed_state, self.constant_variance*np.eye(self.number_of_states))
        
        return np.random.multivariate_normal(current_state, self.constant_variance*np.eye(self.number_of_states))
        # graph or markov chain for finite state space

    def target_distribution(self, current_state, proposed_state = None):

        if(proposed_state != None):
            return np.random.multivariate_normal(proposed_state*current_state, self.constant_variance*np.eye(self.number_of_states))
        
        return np.random.multivariate_normal(current_state, self.constant_variance*np.eye(self.number_of_states))

    def simulate_multi(self):

        # inital state
        state_index = np.random.randint(0,self.number_of_states-1)
        # set the inital state_vector
        state = np.zeros(self.number_of_states)

        # currently high probability state
        state[state_index] = 1

        #previous state
        previous_state_index = -1
        previous_state = np.zeros(self.number_of_states)
        
        for i in range(0,self.number_steps):
            print(state_index)
            # propose a distribution
            proposed_distribution = self.proposal_distribution(state)
            # calculate the acceptance ratio
            acceptance_ratio = (self.target_distribution(proposed_distribution)/self.target_distribution(state)) * (self.proposal_distribution(proposed_distribution)/self.proposal_distribution(state))

            highest_probability = 0
            highest_state = 0
            highest_state_index = 0

            for j in range(0,self.number_of_states):
                if(acceptance_ratio[j] > highest_probability):
                    previous_state_index = state_index
                    previous_state = state

                    highest_probability = acceptance_ratio[j]
                    highest_state = acceptance_ratio
                    highest_state_index = j
            # accept or reject the proposed distribution
            if(highest_probability >= 1):
                previous_state_index = state_index
                previous_state = state
                    
                state = highest_state
                state_index = highest_state_index
            else:
                if(np.random.rand() < highest_probability):
                    previous_state_index = state_index
                    previous_state = state
                    state = highest_state
                    state_index = highest_state_index
                elif(previous_state_index != -1):
                    state = previous_state
                    state_index = previous_state_index

        return

# generating a class like this have to think about a problem first.
class metropolis_langevin:

    def __init__(self):

        # express the simulation steps defined as time for mechanics purposes
        self.simulation_steps = 10

        # express the time domain of the problem
        self.time_domain = [0, 1]
        self.domain_length = self.time_domain[1]-self.time_domain[0]

        # express the minute step length 
        self.step_length = self.domain_length / self.simulation_steps

        # define the dimensionality of the problem
        self.number_of_states = 10

        # set up the current state vector as the inital boundary condition
        self.current_state = np.full(self.number_of_states, 0)

        # set of the covariance matrix
        self.covariance = np.eye(self.number_of_states)
        self.inv_cov = np.linalg.inv(self.covariance)

        # prior mean information
        self.mean = np.full(self.number_of_states, 0)


        return
    
    # discrete or continue probability density function (guassian etc)
    # p(current_state)
    def prior_distribution(self, current_state):
        # belief or assumption before assuming the data

        d = self.number_of_states
        a = ((2*np.pi)**(d/2))*np.sqrt((np.linalg.det(self.covariance)))
        b = -(1/2)*np.transpose((current_state - self.mean))*self.inv_cov*(current_state-self.mean)
        return (1/a)*np.exp(b)
    
    # discrete or continue probability density function
    # p(current_state | proposed )
    # use same type as prior_distribution | either guassian etc, mesh
    # exp{f(x)} liklihood
    def likelihood(self, proposed):
        d = self.number_of_states
        a = ((2*np.pi)**(d/2))*np.sqrt((np.linalg.det(self.covariance)))
        b = -(1/2)*np.transpose((proposed - self.mean))*self.inv_cov*(proposed-self.mean)
        return (1/a)*np.exp(b)

    def unormalized_target_distribution(self,current_state):
        return self.prior_distribution(current_state) * self.likelihood(current_state)

    def grad_log_liklihood():

        return 1

    def log_unnormalized_target_gradient(self, current_state):
        # Compute the gradient of the log unnormalized target distribution
        # This involves computing the gradient of the log prior distribution and the log likelihood
        # Since the log unnormalized target distribution is the sum of the log prior and log likelihood,
        # the gradient of the log unnormalized target distribution is the sum of the gradients of the log prior and log likelihood.

        # Gradient of the log prior distribution
        grad_log_prior = -np.dot(self.inv_cov, current_state - self.mean)

        # Gradient of the log likelihood
        # Here, you need to compute the derivative of the log likelihood function with respect to the state variables.
        # The form of the gradient will depend on the specific likelihood function you are using.
        # For example, if you are using a Gaussian likelihood, the gradient would depend on the difference between
        # the proposed state and the mean, and the covariance matrix.
        # You'll need to implement this part based on the specific likelihood function you have.

        # Combine the gradients of the log prior and log likelihood
        grad_log_target = grad_log_prior + self.grad_log_likelihood

        return grad_log_target
        
    def unormalized_target_distribution(self,current_state):
        # target distribution
        np.exp(-self.f(current_state))

        return
    
    def simulate(self):

        for i in range(0, self.simulation_steps):
            t = self.step_length*i
            self.current_state = self.current_state + ((self.step_length**2)/2)*self.log_unnormalized_target_gradient(self.current_state) + self.step_length*self.brownian_motion(i)
    
    def brownian_motion(self, t):
        return np.random.normal(0, np.eye(self.number_of_states))
    
