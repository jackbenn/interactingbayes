#!python
import numpy as np

#TODO
# figure out MCMC approach
#   gather all the observations
#   start at some random position
#   repeatedly:
#     consider "nearby" position
#     choose with probability given by ratio of likelihoods
#         based on the observations
#     if choosen:
#       update position
#     add 
#
#     


class Generators(object):
    def __init__(self, n_generators, relations, n=100):
        '''
        n_generators: int, number of generators
        relations: list of 2-tuples (n1, n2) stating that p1 >= p2
        n: number of levels of probability
        '''

        self.n = n
        self.n_generators = n_generators
        self.dims = (self.n,) * n_generators
        self.priors = np.ones(self.dims) # uniform priors

        # zero out possibilities for which we know one generator must be <= another
        indices = np.indices(self.dims)
        for relation in relations:
            self.priors *= indices[relation[0]] >= indices[relation[1]]
        print self.priors.sum()

        self.normalize()

    def normalize(self):
        self.priors /= self.priors.sum()
    
    def update(self, g, result):
        '''
        update priors base on generator # g producing result result
        g: int (index of generator)
        result: bool (result)
        '''
        self.priors *= self.likelihood(g, result)
        self.normalize()

        
    def likelihood(self, g, result):
        if result:
            return np.indices(self.dims)[g] / (self.n - 1.)
        else:
            return 1-(np.indices(self.dims)[g] / (self.n - 1.))

    def expectation(self, g):
        return (self.priors * self.likelihood(g, True)).sum()





