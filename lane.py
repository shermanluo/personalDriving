import numpy as np
import theano as th
import theano.tensor as tt

import constants
import feature

class Lane(object): pass

class StraightLane(Lane):
    def __init__(self, p, q, w):
        self.p = np.asarray(p) # start vector of lane
        self.q = np.asarray(q) # end vector of lane
        self.w = w # width
        # direction of road (unit norm)
        self.m = (self.q-self.p)/np.linalg.norm(self.q-self.p)
        # orthogonal to direction of road (unit norm)
        self.n = np.asarray([-self.m[1], self.m[0]])
    
    def shifted(self, m):
        return StraightLane(self.p+self.n*self.w*m, self.q+self.n*self.w*m, self.w)
    
    def crosstrack(self, x):
        # cross-track error: distance to centerline of lane 
        return (x[0]-self.p[0])*self.n[0]+(x[1]-self.p[1])*self.n[1]
    
    def crosstrack_squared(self, x):
        # squared cross-track error: distance to centerline of lane squared
        return self.crosstrack(x)**2
    
    def gaussian(self, fw, stdev=constants.LANE_REWARD_STDEV_r):
        @feature.feature
        def f(t, x, u):
            #try:
            return fw.exp(-self.crosstrack_squared(x) / (2 * stdev**2))
            #except Exception as e:
                #import pdb
                #pdb.set_trace(f)

        return f


class Fence(StraightLane):
    def __init__(self, p, q, w, side, ref_cost=0.1, ref_fraction=0.3): # original ref_fraction=0.4
        super(Fence, self).__init__(p, q, w)
        self.side = side # +1 if fence is on the right, -1 if on the left
        # cost=ref_cost when vehicle is ref_fraction*w away from the fence
        self.ref_cost = ref_cost
        self.ref_fraction = ref_fraction
        # scale for sigmoid cost to enforce ref_cost at ref_fraction
        self.scale = np.log(1.0/self.ref_cost-1)/(self.ref_fraction*self.w)
    def shifted(self, m):
        new_p = self.p+self.n*self.w*m
        new_q = self.q+self.n*self.w*m
        return Fence(new_p, new_q, self.w, self.side, self.ref_cost, self.ref_fraction)
    def sigmoid(self, fw):
        @feature.feature
        def f(t, x, u):
            return -1.0 / (1.0 + fw.exp(-1.0 * self.side * self.scale * 
                self.crosstrack(x)))
        return f


if __name__ == '__main__':
    lane = StraightLane([0., -1.], [0., 1.], 0.1)
    x = tt.vector()
    lane.feature()(0, x, 0)
