import numpy as np
class protein_node:
    
    def __init__(self):
        self.position = []
        self.neighbors = []
        self.conformational_attributes = []

class protein_graph:

    def __init__(self):
        return

# mean't to used with particles with energy    
class molecular_hamiltonian:
    def __init__(self):
        
        self.dimension = 0
        self.time_step = 0.1
        self.simulation_steps = 100
        
        self.covariance = np.eye(self.dimension)

        return

    def hamiltonian(position, auxillary_momentum):
        
        return 1/2*np.exp(position) + auxillary_momentum


    

    def leap_frog(self, auxillary_momentum, position):
        iterations = 0
        change_hamiltonian = self.hamiltonian(position-1, auxillary_momentum) + self.hamiltonian(position+1, auxillary_momentum)
        auxillary_half = auxillary_momentum + (self.time_step/2)*change_hamiltonian
        
        new_position = position + (self.time_step)*(np.linalg.inv(self.covariance))*auxillary_half


        change_hamiltonian = self.hamiltonian(new_position-1,auxillary_half) + self.hamiltonian(new_position+1,auxillary_half)
        new_auxillary = auxillary_half + (self.time_step/2)*change_hamiltonian 
        
        return new_position,new_auxillary

    def old(self):
        
        position = 0
        auxillary_momentum = 0

        for i in range(0, self.simulation_steps):
            new_position, new_auxilliary = self.leap_frog(position, auxillary_momentum)

            acceptance_ratio = np.exp(-self.hamiltonian(new_position, new_auxilliary)) \
            / np.exp(-self.hamiltonian(position, auxillary_momentum))

            if(acceptance_ratio == 1 or np.random.random() < acceptance_ratio):
                position = new_position
                auxillary_momentum = new_auxilliary
            
                

        return

    def hamiltonian_monte_carlo(self):

        position_current = np.full(self.dimension,0)

        for m in range(0, self.simulation_steps):
            auxillary_momentum_current = np.random.multivariate_normal(0, self.covariance)
            position_next, auxillary_next = self.leap_frog(auxillary_momentum_current, position_current)
            delta_ham = self.hamiltonian(position_current,auxillary_momentum_current) - self.hamiltonian(position_next,auxillary_next)
            acceptance_ratio = min(1, np.exp(delta_ham))
            # accept or reject based on the ratio.


class magnetic_hamiltonian:
    