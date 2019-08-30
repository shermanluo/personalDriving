import pdb

import theano as th
import theano.tensor as tt
import numpy as np

import constants
import feature
import lane
import utils
import torch


class Trajectory(object):
    def __init__(self, x0, dyn, dt, horizon):
        self.dyn = dyn
        self.dt = dt
        self.horizon = horizon

        ### numpy state, plan, dynamics
        self.dyn_np = dyn(np, dt=dt) # numpy dynamics function
        self.x0_initial = np.array(x0) # initial state
        self._x0 = np.array(x0) # current state
        # plan (list of controls), initialized to zeros
        self._u = [np.zeros(self.dyn_np.nu) for t in range(horizon)]
        self.default_control = np.zeros(self.dyn_np.nu) # default action
        self.u_length = horizon * self.dyn_np.nu # length of self.u in 1-D
        self.x_cache = {}
        self._x = self.get_x(self._x0, self._u, self.dyn_np) # state trajectory

        ### Theano state, plan, dynamics
        self.dyn_th = dyn(tt, dt=dt) # Theano dynamics function
        self._x0_th = utils.th_vector_from_value(x0) # theano version of self.x
        # theano version of self.u
        self._u_th = [utils.th_vector(self.dyn_np.nu) for t in range(horizon)]
        # theano version of self.x
        self._x_th = self.get_x(self._x0_th, self._u_th, self.dyn_th)

        ### Torch state, plan, dynamics
        self.dyn_torch = dyn(torch, dt=dt)  # Theano dynamics function
        self._x0_torch = torch.tensor(x0, requires_grad=True)  # theano version of self.x
        # theano version of self.u
        self._u_torch = [torch.zeros(self.dyn_np.nu) for t in range(horizon)]
        # theano version of self.x
        self._x_torch = self.get_x(self._x0_torch, self._u_torch, self.dyn_torch)
        
        # Start and stop indices of each control in the plan.
        self.control_indices = [a.shape[0] for a in self._u]
        for i in range(1,len(self.control_indices)):
            self.control_indices[i] += self.control_indices[i-1]
        self.control_indices = [(0 if i==0 else self.control_indices[i-1], 
            self.control_indices[i]) for i in range(len(self.control_indices))]
        
        self.timestamp = None # timestamp of the beginning of this trajectory

    def reset(self, x0=None):
        # Reset the trajectory to the given state or to the initial state, and
        # set the plan to all zeros.
        if x0 is not None:
            self.x0 = x0
            self.x0_th = x0
        else:
            self.x0 = self.x0_initial
            self.x0_th = self.x0_initial
        self.u = np.zeros((self.horizon, self.dyn_np.nu))
        # Reset self._u_th directory because resetting to its original symbolic
        # Theano variable and not to an actual value.
        self._u_th = [utils.th_vector(self.dyn_np.nu) for t in range(self.horizon)]

    def move(self, control=None):
        # Apply the given control, or the first control in the plan if no control
        # is given, to update the current position.
        if control is None:
            control = self.u[0]
        self.x0 = self.dyn_np(self.x0, control)
        self.x0_th = self.x0

    def get_x(self, x0, u, dyn):
        # Return state trajectory produced by initial state x0, plan u, and
        # dynamics dyn.
        try: # only works for numpy because Theano variables aren't iterable
            x_cache_key = (tuple(x0), tuple([tuple(ui) for ui in u]))
            return self.x_cache[x_cache_key] # might miss
        except Exception as e:
            pass
        x = []
        for t in range(self.horizon):
            x0 = dyn(x0, u[t])
            x.append(x0)
        try: # save result in cache if possible (not possible when using Theano
             # reward)
            self.x_cache[x_cache_key] = np.array(x)
        except Exception as e:
            pass
        return np.array(x)

    def format_u(self, value):
        # Format the given value for u into the same shape as self.u
        value_flat = np.array(value).flatten() # reshape to 1-D
        # assert(len(value_flat) == self.u_length) # correct number of controls
        formatted_value = [np.zeros(self.dyn_np.nu) for t in range(self.horizon)]
        for i, (a, b) in enumerate(self.control_indices):
            formatted_value[i] = value_flat[a:b]
        return formatted_value

    ### numpy properties
    @property
    def x0(self):
        return self._x0
    @x0.setter
    def x0(self, value):
        assert(len(value) == len(self._x0))
        self._x0 = np.array(value)
    @property
    def x(self):
        return self.get_x(self.x0, self.u, self.dyn_np)
    @property
    def u(self):
        return self._u
    @u.setter
    def u(self, value):
        self._u = self.format_u(value)
    ### Theano properties
    @property
    def x0_th(self):
        return self._x0_th
    @x0_th.setter
    def x0_th(self, value):
        assert(len(value) == len(self._x0))
        self._x0_th.set_value(value)
    @property
    def x_th(self):
        return self._x_th
    @property
    def u_th(self):
        return self._u_th
    @u_th.setter
    def u_th(self, value):
        value_format = self.format_u(value)
        for i in range(len(value_format)):
            self._u_th[i].set_value(value_format[i])

    ### Torch properties
    @property
    def x0_torch(self):
        return self._x0_torch
    @x0_torch.setter
    def x0_torch(self, value):
        assert (len(value) == len(self._x0))
        self._x0_torch = torch.tensor(value)
    @property
    def x_torch(self):
        return self._x_torch

    @property
    def u_torch(self):
        return self._u_torch

    @u_torch.setter
    def u_torch(self, value):
        value_format = self.format_u(value)
        for i in range(len(value_format)):
            self._u_torch[i] = torch.tensor(value_format[i])

    def x_from_x0(self, fw):
        assert(fw == np or fw == tt or fw == torch)
        if fw == np:
            x = [self.x0]
            x.extend(self.x[:-1])
            return x
        elif fw == tt:
            x = [self.x0_th]
            x.extend(self.x_th[:-1])
            return x
        elif fw == torch:
            x = [self.x0_torch]
            x.extend(self.x_torch[:-1])
            return x


    def gaussian(self, fw, length=.07, width=.03):
        """Gaussian-shaped cost around trajectory."""
        assert(fw == np or fw == tt or fw == torch)
        # Make the reward function applied to the state trajectory
        # by calling self.x_from_x0 and using  the computational framework fw.
        # Note: self.x_from_x0 is a function instead of a value so that the 
        # current state trajectory can be used.
        @feature.feature
        def f(t, x, u):
            # Reward evaluated at time t (t=0 is the current state) when the
            # other car is at state x with plan u.
            return Trajectory.r_gaussian(self.x_from_x0(fw)[t], x, fw, 
                length=length, width=width)
        return f

    @staticmethod
    def r_gaussian(this_x0, other_x0, fw, length=.14, width=.03):
        # length=.07, width=.03):
        # Guassian reward around the point this_x0 when the other car is at 
        # state other_x.
        # Arguments:
        #  - this_x0: current state of this car
        #  - other_x0: current state of the other car
        #  - fw: computational fw
        #  - length: constant corresponding to length of car
        #  - width: constant corresponding to width of car
        assert(fw == np or fw == tt or fw == torch)
        d = (this_x0[0]-other_x0[0], this_x0[1]-other_x0[1])
        theta = this_x0[2]
        dl = fw.cos(theta)*d[0]+fw.sin(theta)*d[1]
        dw = -fw.sin(theta)*d[0]+fw.cos(theta)*d[1]
        return fw.exp(-0.5*(dl*dl/(length*length)+dw*dw/(width*width)))

    def gaussian(self, fw, length=.07, width=.03):
        """Gaussian-shaped cost around trajectory."""
        assert(fw == np or fw == tt or fw==torch)
        # Make the reward function applied to the state trajectory
        # by calling self.x_from_x0 and using  the computational framework fw.
        # Note: self.x_from_x0 is a function instead of a value so that the 
        # current state trajectory can be used.
        @feature.feature
        def f(t, x, u):
            # Reward evaluated at time t (t=0 is the current state) when the
            # other car is at state x with plan u.
            return Trajectory.r_gaussian(self.x_from_x0(fw)[t], x, fw, 
                length=length, width=width)
        return f

    def sigmoid(self, fw):
        """Sigmoid-shaped cost around trajectory."""
        assert(fw == np or fw == tt or fw == torch)
        # Make the reward function applied to the state trajectory
        # by calling self.x_from_x0 and using  the computational framework fw.
        # Note: self.x_from_x0 is a function instead of a value so that the 
        # current state trajectory can be used.
        @feature.feature
        def f(t, x, u):
            # Reward evaluated at time t (t=0 is the current state) when the
            # other car is at state x with plan u.
            return Trajectory.r_sigmoid(self.x_from_x0(fw)[t], x, fw)
        return f

    @staticmethod
    def r_sigmoid(this_x0, other_x0, fw):
        """Sigmoidal reward in x- and y-directions surrounding this car.
        This car must be heading straight in its lane (i.e. theta = pi).

        Arguments
        - this_x0: current state of this car
        - other_x0: current state of other car
        - fw: computational framework (numpy or theano.tensor)
        """
        assert(fw == np or fw == tt or fw == torch)
        dx = this_x0[0] - other_x0[0]
        dy = this_x0[1] - other_x0[1]
        theta = this_x0[2]
        # TODO: assert isclose using theano as well
        if fw == np:
            assert np.isclose(theta, np.pi / 2.) # this vehicle must be heading straight
        left = utils.sigmoid(dx, constants.TRUCK_REWARD_SCALE, -constants.TRUCK_REWARD_WIDTH, fw=fw)
        right = -1. * utils.sigmoid(dx, constants.TRUCK_REWARD_SCALE, constants.TRUCK_REWARD_WIDTH, fw=fw)
        x_sigmoid = left + right
        down = utils.sigmoid(dy, constants.TRUCK_REWARD_SCALE, -constants.TRUCK_REWARD_LENGTH, fw=fw)
        up = -1. * utils.sigmoid(dy, constants.TRUCK_REWARD_SCALE, constants.TRUCK_REWARD_LENGTH, fw=fw)
        y_sigmoid = down + up
        return x_sigmoid * y_sigmoid

    
    def not_behind(self, fw, weight):
        # Not behind (another car) penalty represeneted as sigmoids.
        assert(fw == np or fw == tt or fw == torch)
        # Make the reward function applied to the state trajectory
        # by calling self.x_from_x0 and using  the computational framework fw.
        # Note: self.x_from_x0 is a function instead of a value so that the 
        # current state trajectory can be used.
        # Define inverse operation depending on framework (Theano or otherwise)
        if fw == np:
            inv = lambda x: 1.0 / x
        elif fw == torch:
            inv = torch.reciprocal
        elif fw == tt:
            inv = tt.inv
        @feature.feature
        def f(t, x, u):
            # Reward evaluated at time t (t=0 is the current state) when the
            # other car is at state x with plan u.
            #pdb.set_trace()
            return Trajectory.r_not_behind(self.x_from_x0(fw)[t], x, weight, fw, inv)
        return f

    @staticmethod
    def r_not_behind(this_x0, other_x0, weight, fw, inv):
        # Negative sigmoid reward for being behind this car.
        # Arguments:
        #  - this_x0: state of this car
        #  - other_x0: state of other car
        #  - weight: constant multiplier
        #  - fw: computational framework
        #  - inv: inversion operation, depending on numpy or Theano
        assert(fw == np or fw == tt or fw == torch)
        x_rel = other_x0[0]-this_x0[0]
        y_rel = other_x0[1]-this_x0[1]
        term1 = inv(1+fw.exp(-constants.BEHIND_REWARD_SLOPE * (x_rel+0.13/2)))
        term2 = inv(1+fw.exp(constants.BEHIND_REWARD_SLOPE * (x_rel-0.13/2)))
        term3 = inv(1+fw.exp(constants.BEHIND_REWARD_SLOPE * y_rel))
        return weight*term1*term2*term3

    # TODO: implement x_func functionality like for gaussian and not_behind
    # HERE FOUND ERROR!!!  wa was 1/0.025 but should be 1/0.01!!! So now things should be less critical (though perhaps still present!!)
    def minkowski_sum_2d(
                    self, fw, ha = 1/0.025, wa = 1/0.01,
                    own_length=.6957, own_width=2.6*constants.METERS_TO_VIS,
                    other_length=0.148, other_width=1.9*constants.METERS_TO_VIS):
        # This minkowski sum is approximate in the sense that both vehicles 
        # are assumed to be in the y-direction (fixed theta).
        # Height is in the y-direction while width is in the x-direction.
        assert(fw == np or fw == tt or fw == torch)
        def make_f(x_func, fw):
            # Make the reward function applied to the given state trajectory
            # x_func() and the computational framework fw.
            if fw == np:
                inv = lambda x: 1.0 / x
            elif fw == tt:
                inv = tt.inv
            elif fw == torch:
                inv = torch.reciprocal
            @feature.feature
            def f(t, x, u):
                # Reward evaluated at time t (t=0 is the current state) when the
                # other car is at state x with plan u.
                #ha = 1/0.025 # The slopes of the sigmoids.
                #wa = 1/0.01
                hl = x_func(fw)[t][1]-(own_length+other_length)/2 # The shifts of the sigmoids.
                hu = x_func(fw)[t][1]+(own_length+other_length)/2
                wl = x_func(fw)[t][0]-(own_width+other_width)/2
                wu = x_func(fw)[t][0]+(own_width+other_width)/2
                term1 = inv(1+fw.exp(-ha*(x[1]-hl)))
                term2 = inv(1+fw.exp(ha*(x[1]-hu)))
                term3 = inv(1+fw.exp(-wa*(x[0]-wl)))
                term4 = inv(1+fw.exp(wa*(x[0]-wu)))
                return term1*term2*term3*term4
            return f
        return make_f(self.x_from_x0, fw)
        

    # TODO: implement x_func functionality like for gaussian and not_behind
    def minkowski_sum_1d(self, fw, h=1/0.025, own_length=.14, other_length=.14):
        # This minkowski sum assumes what minkowski_sum_2d assumes plus that the 
        # vehicles are aligned in the y-direction.
        assert(fw == np or fw == tt or fw == torch)
        def make_f(x_func, fw):
            # Make the reward function applied to the given state trajectory
            # x_func() and the computational framework fw.
            if fw == np:
                inv = lambda x: 1.0 / x
            elif fw == tt:
                inv = tt.inv
            elif fw == torch:
                inv = torch.reciprocal
            @feature.feature
            def f(t, x, u):
                # Reward evaluated at time t (t=0 is the current state) when the
                # other car is at state x with plan u.
                #ha = 1/0.025 # The slope of the sigmoids.
                hl = x_func(fw)[t][1]-(own_length+other_length)/2 # The shifts of the sigmoids.
                hu = x_func(fw)[t][1]+(own_length+other_length)/2
                term1 = inv(1+fw.exp(-ha*(x[1]-hl)))
                term2 = inv(1+fw.exp(ha*(x[1]-hu)))
                return term1*term2
            return f
        return make_f(self.x_from_x0, fw)

    
    # TODO: update this function to match format of the other functions above)
    def truck_tailing(self, fw, tailing_dist=0.6957+8.9597*constants.METERS_TO_VIS, 
        weight=1):
        @feature.feature
        def f(t, x, u):
            # Reward evaluated at time t (t=0 is the current state) when the
            # other car is at state x with plan u.
            c = self.x_th[t][1]-tailing_dist
            return weight*fw.exp(-(x[1]-c)**2/(2*0.05**2))
        return f
    
    # TODO: update this function to match format of the other functions above)
    def truck_tailing_quad(self, tailing_dist=0.6957+8.9597*constants.METERS_TO_VIS, weight=4./((7.*constants.METERS_TO_VIS)**2)): # is -4 at gap distance 16 meter. 
        @feature.feature
        def f(t, x, u):
            # Reward evaluated at time t (t=0 is the current state) when the
            # other car is at state x with plan u.
            c = self.x_th[t][1]-tailing_dist+0.018 # 0.018 is shift to get combined proxmity reward over 9 (8.9597) m.
            return -weight*(x[1]-c)**2
        return f
    
    # TODO: update this function to match format of the other functions above)
    def stay_inside_domain(self, fw, ha=1/0.025, 
                           limit_dist=12*constants.METERS_TO_VIS, weight=100):
        # Elis: added to make trucks stay inside its DSG domain.
        if fw == tt:
            inv = tt.inv
        elif fw == th:
            inv = torch.reciprocal
        else:
            inv = lambda x: 1.0 / x 
        @feature.feature
        def f(t,x,u):
            # Reward evaluated at time t (t=0 is the current state) when the
            # other car is at state x with plan u.
            c = self.x_th[t][1]-limit_dist
            return weight*inv(1+fw.exp(-ha*(x[1]-c)))
        return f
    
    def reward(self, reward, fw):
        # Function for assembling the cumulative rewards.
        #
        # Important note concerning the index of state and control:
        # The index of the state and the control are different in the sense that 
        # x[0] is not x0 but u[0] is the first applied control. That is the state 
        # index is shifted one step ahead. This "miss" is okay as long as the state
        # part and the control part in the reward above is additively separable, 
        # which is the case.
        
        # Important comment concerning the hierarchical game and the last_reward:
        # For the hierarchical game, this function assembles the tactic level with 
        # last rewards determined by last_reward. The last_reward is a replacement 
        # for the last added accumulative reward of the tactic horizon. If this was 
        # not done (i.e. last_reward=None) and the value function were added with 
        # this reward, then the end state of the tactic level (self.x_th[horizon]) 
        # would both be included in the accumulative reward of the tactic level 
        # (consider the last term in the list (*) below, and the note concerning 
        # state and control index above) AND the cost-to-go by the value function 
        # (the value functions is a function of the end state of the tactic level). 
        # ince we do not want to count the end state twice, the last_reward omit 
        # the state-dependent term from the tactic level, keeping just the control 
        # part from the tactic level. Apart from the control part, last_reward might 
        # also include the value function if possible. This is done in the platoon 
        # cenario since the the value functions is on an analytical closed form 
        # (neural network). In the car scenarios however, the value function is 
        # given via grid interpolation that needs to be updated in the optimiation 
        # process. In this case, last_reward is just the control part.

        # align self.x{_th} and self.u{_th} properly in order to compute the reward.
        # self.x{_th}[t] and self.u{_th}[t] should be the state and control applied 
        # at time t. Prepend x0 to self.x{_th}, don't use self.x{_th}[-1] for the
        # tactical reward.
        
        assert(fw == np or fw == tt or fw == torch)
        if fw == np:
            # x = self.x
            x = [self.x0]
            x.extend(self.x[:-1])
            return sum([reward(t, x[t], self.u[t]) for t in range(self.horizon)])
        elif fw == tt:
            # x = self.x_th
            x = [self.x0_th]
            x.extend(self.x_th[:-1])
            return sum([reward(t, x[t], self.u_th[t]) for t in range(self.horizon)])
        elif fw == torch:
            # x = self.x_th
            x = [self.x0_torch]
            x.extend(self.x_torch[:-1])
            return sum([reward(t, x[t], self.u_torch[t]) for t in range(self.horizon)])
        
    def cum_reward(self, reward, fw):
        # The first cumulative reward term. Note that use of the current state 
        # (x0) and the first control (u[0]) (see the important note in the 
        # reward function above.
        assert(fw == np or fw == tt or fw == torch)
        if fw == np:
            return reward(0, self.x0, self.u[0])
        elif fw == tt:
            return reward(0, self.x0_th, self.u_th[0])
        elif fw == torch:
            return reward(0, self.x0_torch, self.u_torch[0])
