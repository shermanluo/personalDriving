import itertools
import pdb
import time

import numpy as np
import numpy.linalg as nl
import theano as th
import theano.tensor as tt
import theano.tensor.slinalg as ts
import scipy.optimize
import scipy.io

import config
import constants
import opt_timeup
import time_profile
import utils
from utils import shape, jacobian, hessian, grad

class Maximizer(object):
    def __init__(self, f, vs, g={}, pre=None, gen=None, method='bfgs', eps=1, iters=100000, debug=False, inf_ignore=np.inf):
        self.inf_ignore = inf_ignore
        self.debug = debug
        self.iters = iters
        self.eps = eps
        self.method = method
        def one_gen():
            yield
        self.gen = gen
        if self.gen is None:
            self.gen = one_gen
        self.pre = pre
        self.f = f
        self.vs = vs
        self.sz = [shape(v)[0] for v in self.vs]
        for i in range(1,len(self.sz)):
            self.sz[i] += self.sz[i-1]
        self.sz = [(0 if i==0 else self.sz[i-1], self.sz[i]) for i in range(len(self.sz))]
        if isinstance(g, dict):
            self.df = tt.concatenate([g[v] if v in g else grad(f, v) for v in self.vs])
        else:
            self.df = g
        self.new_vs = [tt.vector() for v in self.vs]
        self.func = th.function(self.new_vs, [-self.f, -self.df], givens=zip(self.vs, self.new_vs))
        def f_and_df(x0):
            if self.debug:
                print x0
            s = None
            N = 0
            for _ in self.gen():
                if self.pre:
                    for v, (a, b) in zip(self.vs, self.sz):
                        v.set_value(x0[a:b])
                    self.pre()
                res = self.func(*[x0[a:b] for a, b in self.sz])
                if np.isnan(res[0]).any() or np.isnan(res[1]).any() or (np.abs(res[0])>self.inf_ignore).any() or (np.abs(res[1])>self.inf_ignore).any():
                    continue
                if s is None:
                    s = res
                    N = 1
                else:
                    s[0] += res[0]
                    s[1] += res[1]
                    N += 1
            s[0]/=N
            s[1]/=N
            return s
        self.f_and_df = f_and_df
    def argmax(self, vals={}, bounds={}):
        if not isinstance(bounds, dict):
            bounds = {v: bounds for v in self.vs}
        B = []
        for v, (a, b) in zip(self.vs, self.sz):
            if v in bounds:
                B += bounds[v]
            else:
                B += [(None, None)]*(b-a)
        x0 = np.hstack([np.asarray(vals[v]) if v in vals else v.get_value() for v in self.vs])
        if self.method=='bfgs':
            opt = scipy.optimize.fmin_l_bfgs_b(self.f_and_df, x0=x0, bounds=B)[0]
        elif self.method=='gd':
            opt = x0
            for _ in range(self.iters):
                opt -= self.f_and_df(opt)[1]*self.eps
        else:
            opt = scipy.optimize.minimize(self.f_and_df, x0=x0, method=self.method, jac=True).x
        return opt
    def maximize(self, *args, **vargs):
        return self.argmax(*args, **vargs)        

class OneIterationNestedMaximizer(object):
    def __init__(self, r_h, traj_h, r_r, traj_r):
        """
        Arguments:
            - r_h: the human tactical reward.
            - traj_h: the human trajectory.
            - r_r: the robot tactical reward.
            - traj_r: the robot trajectory.
        """
        # self.r_h = r_h
        # self.r_r = r_r
        self.traj_h = traj_h
        self.traj_r = traj_r
        self.plan_h = traj_h.u_th # human plan (controls)
        self.plan_r = traj_r.u_th # robot plan (controls)
        self.human_optimizer = Maximizer(r_h, self.plan_h)
        self.robot_optimizer = Maximizer(r_r, self.plan_r)

    def maximize(self, other_vals={}, other_bounds={}, vals={}, bounds={}):
        # Assume human is other and robot is this
        # Find the optimal human plan
        opt_plan_h = self.human_optimizer.maximize(vals=other_vals, bounds=other_bounds)

        # Set the robot's belief of the human plan to the predicted/planned
        # human plan
        for v, (a, b) in zip(self.plan_h, self.traj_h.control_indices):
            v.set_value(opt_plan_h[a:b])

        # Find the optimal robot plan
        return self.robot_optimizer.maximize(vals=vals, bounds=bounds)


# class SimpleMaximizer(object):
#     # Just simple maximization of the reward ignoring any interaction with other agents.
#     # This is for example used for the sucessor of a truck, the predecessor's control is treated as fixed.
#     # The whole code is taken from NestedMaximizer.
#     def __init__(self, f1, vs1, use_timeup=True):
#         self.f1 = f1
#         self.vs1 = vs1
#         self.sz1 = [shape(v)[0] for v in self.vs1]
#         for i in range(1, len(self.sz1)):
#             self.sz1[i] += self.sz1[i-1]
#         self.sz1 = [(0 if i==0 else self.sz1[i-1], self.sz1[i]) for i in range(len(self.sz1))]
#         if use_timeup:
#             self.timeup = config.OPT_TIMEOUT
#         else:
#             self.timeup = float('inf')
#         self.df1 = grad(self.f1, vs1)
#         self.new_vs1 = [tt.vector() for v in self.vs1]
#         self.func1 = th.function(self.new_vs1, [-self.f1, -self.df1], givens=zip(self.vs1, self.new_vs1))
#         def f1_and_df1(x0):
#             return self.func1(*[x0[a:b] for a, b in self.sz1])
#         self.f1_and_df1 = f1_and_df1
#     def maximize(self, bounds={}):
#         t0 = time.time()
#         if not isinstance(bounds, dict):
#             bounds = {v: bounds for v in self.vs1}
#         B = []
#         for v, (a, b) in zip(self.vs1, self.sz1):
#             if v in bounds:
#                 B += bounds[v]
#             else:
#                 B += [(None, None)]*(b-a)
#         x0 = np.hstack([v.get_value() for v in self.vs1])
#         opt = opt_timeup.fmin_l_bfgs_b_timeup(self.f1_and_df1, x0=x0, bounds=B,
#                                               t0=t0, timeup=self.timeup)
#         opt = opt[0]
#         for v, (a, b) in zip(self.vs1, self.sz1):
#             v.set_value(opt[a:b])


class NestedMaximizer(object):
    def __init__(self, r_h, traj_h, r_r, traj_r, use_timeup=True, 
            use_second_order=False, update_with_curr_plan_fn=None,
            init_plan_scheme='prev_opt',
            # num_optimizations_r=1, get_init_plan_r_fn=None,
            # num_optimizations_h=1, get_init_plan_h_fn=None,
            init_grads=True):
        """
        Arguments:
            - r_h: the human tactical reward.
            - traj_h: the human trajectory.
            - r_r: the robot tactical reward.
            - traj_r: the robot trajectory.
            - update_with_curr_plan_fn: function to update any necessary information
                based on the current plan. This is only necessary for the 
                HierarchicalMaximizer, not the NestedMaximizer.
            - init_plan_scheme: string specifying the plan initialization scheme.
            - num_optimizations_r: number of times to optimize the robot reward (the
                best result of these optimizations will be chosen).
            - get_init_plan_r_fn: function to return a function that initializes 
                the robot's plan for optimization, based on the current optimization
                iteration.
            - num_optimizations_h: number of times to optimize the human reward (the
                best result of these optimizations will be chosen).
            - get_init_plan_h_fn: function to return a function that initializes 
                the human's plan for optimization, based on the current optimization
                iteration.
            - init_grads: if True, initialize the gradients. This argument can be 
                set to False if another function is meant to initialize the gradients.
        """

        # ---------------------------------------------------------------------------------------------------
        # Basics.

        self.r_h = r_h
        self.r_r = r_r
        self.traj_h = traj_h
        self.traj_r = traj_r
        self.plan_h = traj_h.u_th # human plan (controls)
        self.plan_r = traj_r.u_th # robot plan (controls)
        # (start, end) indices for each control in the plan when it's represented
        # as a flattened array. Ex: [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
        self.control_indices_h = traj_h.control_indices
        self.control_indices_r = traj_r.control_indices
        # maximum time for optimization
        if use_timeup:
            self.timeup = config.OPT_TIMEOUT
        else:
            self.timeup = float('inf')
        self.use_second_order = use_second_order
        if update_with_curr_plan_fn is None: # no functionality necessary here
            update_with_curr_plan_fn = lambda: None
        self.update_with_curr_plan_fn = update_with_curr_plan_fn
        
        # self.num_optimizations_r = num_optimizations_r
        # if get_init_plan_r_fn is None:
        #     self.get_init_plan_r_fn = self.get_init_plan_r_fn_default
        # else:
        #     self.get_init_plan_r_fn = get_init_plan_r_fn
        # self.num_optimizations_h = num_optimizations_h
        # if get_init_plan_h_fn is None:
        #     self.get_init_plan_h_fn = self.get_init_plan_h_fn_default
        # else:
        #     self.get_init_plan_h_fn = get_init_plan_h_fn
        self.create_get_init_plans_fn(init_plan_scheme)

        self.maximizer_inner_iters = 0 # number of iterations of maximizer_inner

        if init_grads: # initialize the gradients
            self.init_grads()

    def create_get_init_plans_fn(self, init_plan_scheme):
        """Create the functions that return the plan initialization functions
        for the robot and the human, depending on the optimization iteration.
        Also set the number of optimization loops for the robot and human.
        Arguments:
            - init_plan_scheme: string specifying the plan initialization scheme.
        """
        assert init_plan_scheme in constants.INIT_PLAN_SCHEMES_OPTIONS
        self.get_init_plan_r_fn = eval('self.get_init_plan_r_fn_' + init_plan_scheme)
        self.get_init_plan_h_fn = eval('self.get_init_plan_h_fn_' + init_plan_scheme)
        self.num_optimizations_r = constants.INIT_PLAN_SCHEME_TO_NUM_OPTS_R[init_plan_scheme]
        self.num_optimizations_h = constants.INIT_PLAN_SCHEME_TO_NUM_OPTS_H[init_plan_scheme]

    def get_init_plan_r_fn_maintain_speed_lsr_and_prev_opt(self, iter):
        # TODO: comment this
        v = self.traj_r.x0[3]
        acc = constants.FRICTION * v**2
        init_plan_r_fn_list = [
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][0], acc] for _ in range(self.traj_r.horizon)),
            lambda: np.hstack([0., acc] for _ in range(self.traj_r.horizon)),
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][1], acc] for _ in range(self.traj_r.horizon)),
            lambda: np.hstack([v.get_value() for v in self.plan_r[:-1]] + [self.traj_r.default_control])
            ]
        return init_plan_r_fn_list[iter]

    def get_init_plan_h_fn_maintain_speed_lsr_and_prev_opt(self, iter):
        # TODO: comment this
        v = self.traj_h.x0[3]
        acc = constants.FRICTION * v**2
        init_plan_h_fn_list = [
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][0], acc] for _ in range(self.traj_h.horizon)),
            lambda: np.hstack([0., acc] for _ in range(self.traj_h.horizon)),
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][1], acc] for _ in range(self.traj_h.horizon)),
            lambda: np.hstack([v.get_value() for v in self.plan_h[:-1]] + [self.traj_h.default_control])
            ]
        return init_plan_h_fn_list[iter]

    def get_init_plan_r_fn_maintain_speed_lsr(self, iter):
        # TODO: comment this
        v = self.traj_r.x0[3]
        acc = constants.FRICTION * v**2
        init_plan_r_fn_list = [
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][0], acc] for _ in range(self.traj_r.horizon)),
            lambda: np.hstack([0., acc] for _ in range(self.traj_r.horizon)),
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][1], acc] for _ in range(self.traj_r.horizon))
            ]
        return init_plan_r_fn_list[iter]

    def get_init_plan_h_fn_maintain_speed_lsr(self, iter):
        # TODO: comment this
        v = self.traj_h.x0[3]
        acc = constants.FRICTION * v**2
        init_plan_h_fn_list = [
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][0], acc] for _ in range(self.traj_h.horizon)),
            lambda: np.hstack([0., acc] for _ in range(self.traj_h.horizon)),
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][1], acc] for _ in range(self.traj_h.horizon))
            ]
        return init_plan_h_fn_list[iter]

    def get_init_plan_r_fn_lsr(self, iter):
        # TODO: comment this
        init_plan_r_fn_list = [
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][0], 0.] for _ in range(self.traj_r.horizon)),
            lambda: np.hstack([0., 0.] for _ in range(self.traj_r.horizon)),
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][1], 0.] for _ in range(self.traj_r.horizon))
            ]
        return init_plan_r_fn_list[iter]

    def get_init_plan_h_fn_lsr(self, iter):
        # TODO: comment this
        init_plan_h_fn_list = [
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][0], 0.] for _ in range(self.traj_h.horizon)),
            lambda: np.hstack([0., 0.] for _ in range(self.traj_h.horizon)),
            lambda: np.hstack([constants.CAR_CONTROL_BOUNDS[0][1], 0.] for _ in range(self.traj_h.horizon))
            ]
        return init_plan_h_fn_list[iter]

    def get_init_plan_r_fn_max_speed_prev_steer(self, iter):
        # TODO: comment this
        return lambda: np.hstack([[v.get_value()[0], constants.CAR_CONTROL_BOUNDS[1][1]] for v in self.plan_r[:-1]] + [self.traj_r.default_control[0], constants.CAR_CONTROL_BOUNDS[1][1]])

    def get_init_plan_h_fn_max_speed_prev_steer(self, iter):
        # TODO: comment this
        return lambda: np.hstack([[v.get_value()[0], constants.CAR_CONTROL_BOUNDS[1][1]] for v in self.plan_h[:-1]] + [self.traj_h.default_control[0], constants.CAR_CONTROL_BOUNDS[1][1]])

    def get_init_plan_r_fn_maintain_speed_prev_steer(self, iter):
        # TODO: comment this
        v = self.traj_r.x0[3]
        acc = constants.FRICTION * v**2
        return lambda: np.hstack([[v.get_value()[0], acc] for v in self.plan_r[:-1]] + [self.traj_r.default_control[0], acc])

    def get_init_plan_h_fn_maintain_speed_prev_steer(self, iter):
        # TODO: comment this
        v = self.traj_h.x0[3]
        acc = constants.FRICTION * v**2
        return lambda: np.hstack([[v.get_value()[0], acc] for v in self.plan_h[:-1]] + [self.traj_h.default_control[0], acc])

    def get_init_plan_r_fn_prev_opt(self, iter):
        # TODO: comment this
        """Initialize the robot plan using the default way."""
        return lambda: np.hstack([v.get_value() for v in self.plan_r[:-1]] + [self.traj_r.default_control])

    def get_init_plan_h_fn_prev_opt(self, iter):
        # TODO: comment this
        """Initialize the human's plan using the default way."""
        return lambda: np.hstack([v.get_value() for v in self.plan_h[:-1]] + [self.traj_h.default_control])


    def init_grads(self):
        """Initialize the gradients based on the rewards.
        Precondition: the rewards (self.r_h and self.r_r) have already been 
        initialized.
        """
        # gradient of human reward wrt human controls
        self.dr_h = grad(self.r_h, self.plan_h)
        # negative human reward and its derivative
        self.func1 = th.function([], [-self.r_h, -self.dr_h])
        def r_h_and_dr_h(plan_h_0):
            """Evaluate negative human reward and its derivative.
            - plan_h_0: initial value for human plan."""
            start_time = time.time()
            # set plan_h to the given (initial) plan_h_0
            for v, (a, b) in zip(self.plan_h, self.control_indices_h):
                v.set_value(plan_h_0[a:b])
            # do any necessary updates based on the current plan
            # (this is necessary for the HierarchicalMaximizer, not the Nested Maximizer)
            self.update_with_curr_plan_fn()
            func1_val = self.func1() # negative human reward and its derivative
            end_time = time.time()
            time_profile.inner_loop_time_profile.update(start_time, end_time)
            return func1_val
        self.r_h_and_dr_h = r_h_and_dr_h

        # ------------------------------------------------------------------------------------------
        # Robot's reward and its derivative.

        # ------------------------------------------------------------------------------------------
        if self.use_second_order:
            # OPTION 1: Full derivative computation with Hessian inversion. 
            # SLOW, DEPRECATED
            # jacobian of (d human reward / d robot actions) w.r.t. human actions
            J = jacobian(grad(self.r_h, self.plan_r), self.plan_h)
            # hessian of human reward w.r.t. human actions
            H = hessian(self.r_h, self.plan_h)
            # d robot reward / d human actions
            g = grad(self.r_r, self.plan_h)
            # Below is the most time-consuming step (the solve(H,g))
            self.dr_r = -tt.dot(J, ts.solve(H, g))+grad(self.r_r, self.plan_r)
        # ------------------------------------------------------------------------------------------
        else:
            # OPTION 2: Partial derivative computation. FAST
            # (Only direct effect of robot action given current human action)
            # Below is the simplified derivative that neglects the second-order 
            # effect through human (and therefore avoids the heavy Hessian 
            # inversion)
            self.dr_r = grad(self.r_r, self.plan_r)
        # ------------------------------------------------------------------------------------------

        # negative robot reward and its derivative
        self.func2 = th.function([], [-self.r_r, -self.dr_r])
        def r_r_and_dr_r(plan_r_0):
            """Get optimal human response, and return negative robot reward 
            and its derivative.
            - plan_r_0: initial value for robot plan."""
            # set self.plan_r to the given (initial) plan_r_0
            for v, (a, b) in zip(self.plan_r, self.control_indices_r):
                v.set_value(plan_r_0[a:b])
            self.maximize_inner() # get optimal human response
            start_time = time.time()
            func2_val = self.func2() # negative robot reward and its derivative
            end_time = time.time()
            time_profile.func2_time_profile.update(start_time, end_time)
            return func2_val
        self.r_r_and_dr_r = r_r_and_dr_r

    def maximize_inner(self, bounds={}, maxiter=config.NESTEDMAX_MAXITER_INNER):
        """Get optimal human response (controls).
        Arguments:
        - bounds: control bounds for the human.
        - maxiter: maximum number of iterations.
        """
        start_time = time.time()
        
        bounds = constants.HIERARCHICAL_HUMAN_CONTROL_BOUNDS
        if not isinstance(bounds, dict): # convert bounds to dictionary
            bounds = {v: bounds for v in self.plan_h}
        B = [] # list of bounds for each control in the plan
        for v, (a, b) in zip(self.plan_h, self.control_indices_h):
            if v in bounds:
                B += bounds[v]
            else:
                B += [(None, None)]*(b-a)
        
        
        # TODO: can we replace the .get_value() approach with using the numpy
        # version because at this point the Theano and numpy plans are the same?
        # plan_h_0 = np.hstack(self.traj_h.u) # initial robot plan (numpy version)
        if self.maximizer_inner_iters == 0:
            # initialize the robot's plan using the defined plan initialization scheme
            plan_h_0 = self.init_plan_h()
        else:
            # initialize human plan to previous optimal value
            plan_h_0 = np.hstack([v.get_value() for v in self.plan_h])
        
        # optimal human response, value, etc.
        opt_h = scipy.optimize.fmin_l_bfgs_b(self.r_h_and_dr_h, x0=plan_h_0, 
                bounds=B)
        opt_plan_h = opt_h[0] # optimal human response

        for v, (a, b) in zip(self.plan_h, self.control_indices_h):
            v.set_value(opt_plan_h[a:b])

        # do any necessary updates based on the current plan
        # (this is necessary for the HierarchicalMaximizer, not the Nested Maximizer)
        self.update_with_curr_plan_fn()
        
        # increment the counter for the number of iterations of maximizer_inner
        self.maximizer_inner_iters += 1
        end_time = time.time()
        time_profile.maximize_inner_time_profile.update(start_time, end_time)
        return opt_h

    def maximize(self, bounds={}, bounds_inner={}, 
                maxiter_inner=config.NESTEDMAX_MAXITER_INNER):
        # Get optimal robot plan (controls) and human response using nested
        # optimization.
        start_time = time.time()
        if not isinstance(bounds, dict): # convert bounds to dictionary
            bounds = {v: bounds for v in self.plan_r}
        B = [] # list of bounds for each control in the plan
        for v, (a, b) in zip(self.plan_r, self.control_indices_r):
            if v in bounds:
                B += bounds[v]
            else:
                B += [(None, None)]*(b-a)
        

        opt_r_list = [] # list of optimization results
        for i in range(self.num_optimizations_r):
            # TODO: can we replace the .get_value() approach with using the numpy
            # version because at this point the Theano and numpy plans are the same?
            # plan_r_0 = np.hstack(self.traj_r.u) # initial robot plan (numpy version)
            plan_r_0 = self.get_init_plan_r_fn(i)() # initialize the robot's plan
            # plan_r_0 = np.hstack([v.get_value() for v in self.plan_r])
            for j in range(self.num_optimizations_h):
                
                # debugging
                # print('robot optimization iter:', i)
                # print('human optimization iter:', j)

                # reset number of maximizer_inner iterations
                self.maximizer_inner_iters = 0
                # get the human's plan initialization function
                self.init_plan_h = self.get_init_plan_h_fn(j)
                # optimal robot control, value, etc.
                opt_r = opt_timeup.fmin_l_bfgs_b_timeup(self.r_r_and_dr_r, 
                    x0=plan_r_0, bounds=B, t0=start_time, timeup=self.timeup)
                opt_r_list.append(opt_r)
                # opt_plan_r = opt_r[0] # optimal robot control

        # get the best plan based on its value
        best_opt_r = min(opt_r_list, key=lambda opt: opt[1])
        opt_plan_r = best_opt_r[0] # optimal robot control
        
        # debugging
        # print('opt_r_list:', opt_r_list)
        # print('best_opt_r:', best_opt_r)

        # TODO: remove?
        for v, (a, b) in zip(self.plan_r, self.control_indices_r):
            v.set_value(opt_plan_r[a:b])

        # optimal human response, value, etc. to optimal robot control
        opt_h = self.maximize_inner(bounds=bounds_inner, maxiter=maxiter_inner)

        # time profile of HierarchicalMaximizer
        maximize_end_time = time.time()
        time_profile.maximizer_time_profile.update(start_time, maximize_end_time)
        return opt_r, opt_h


class HierarchicalMaximizer(NestedMaximizer):
    # The following class maximizes the hierarchical game between the robot (leader)
    # and the human (follower). The tactic reward is given analytically as inputs
    # while the terminal rewards given as the value functions of the strategic level
    # is loaded into the class as grids. To get the value from the value functions,
    # grid interpltion is used (see code below for details).
    def __init__(self, r_h, traj_h, r_r, traj_r, mat_name, n, 
        proj, traj_truck=None, use_timeup=True, use_second_order=False,
        init_plan_scheme='prev_opt',
        disc_grid=None, step_grid=None, vH_grid=None, vR_grid=None):
        """
        Arguments
        - r_h: the human tactical reward.
        - traj_h: the human trajectory.
        - r_r: the robot tactical reward.
        - traj_r: the robot trajectory.
        - mat_name: the matlab file with the value function grids.
        - n: the number of dimensions of the strategic level.
        - proj: function specifying the projection from the tactical level to the strategic level.
        - traj_truck: the truck trajectory. If None, the truck is not used in the
            strategic value.
        """

        # ---------------------------------------------------------------------------------------------------
        # Basics.

        NestedMaximizer.__init__(self, r_h, traj_h, r_r, traj_r, 
            use_timeup=use_timeup, 
            use_second_order=use_second_order, 
            update_with_curr_plan_fn=self.update_corners,
            init_plan_scheme=init_plan_scheme,
            init_grads=False)

        self.n = n # dimension of strategic state
        self.x_tact_h = traj_h.x_th[-1] # final human tactical state
        self.x_tact_r = traj_r.x_th[-1] # final robot tactical state
        if traj_truck is not None:
            self.x_tact_truck = traj_truck.x_th[-1]

        # ---------------------------------------------------------------------------------------------------
        # Shared varables.

        # Grid interpolation is done with the grid corners of the current grid 
        # cell the state is in. These grid corners are shared variables which 
        # are updated as the state is updated. Since the grid step lengths 
        # are given, only the lower corners (self.cell_corners below) are needed 
        # as shared variables.
        self.cell_corners = th.shared(np.zeros(self.n)) # corners of each box in grid
        # corners for human value function
        self.vH_corners = th.shared(np.zeros([2 for i in range(n)]))
        # corners for robot value function
        self.vR_corners = th.shared(np.zeros([2 for i in range(n)]))

        # ---------------------------------------------------------------------------------------------------
        # Load grid data.
        if (disc_grid is None or step_grid is None or vH_grid is None or 
                    vR_grid is None):
            self.disc_grid, self.step_grid, self.vH_grid, self.vR_grid = (
                utils.load_grid_data(mat_name, n=self.n))
        else:
            self.disc_grid, self.step_grid, self.vH_grid, self.vR_grid = (
                disc_grid, step_grid, vH_grid, vR_grid)

        # ---------------------------------------------------------------------------------------------------
        # Value functions.

        # strategic state (project using Theano)
        if traj_truck is not None:
            self.x_strat = proj(self.x_tact_r, self.x_tact_h, self.x_tact_truck)
        else:
            self.x_strat = proj(self.x_tact_r, self.x_tact_h)
        self.x_strat_func = th.function([], self.x_strat)

        def value_function(value_corners):
            return HierarchicalMaximizer.value_function_fn(self.x_strat, 
                self.cell_corners, value_corners, self.step_grid, self.n)

        self.vR = value_function(self.vR_corners) # robot value function
        self.vH = value_function(self.vH_corners) # human value function

        # ---------------------------------------------------------------------------------------------------
        # Human's reward and its derivative.

        # add strategic value function
        self.r_h += config.STRATEGIC_VALUE_SCALE * self.vH

        # ------------------------------------------------------------------------------------------
        # Robot's reward and its derivative.

        # add strategic value function
        self.r_r += config.STRATEGIC_VALUE_SCALE * self.vR

        # initialize the gradients
        NestedMaximizer.init_grads(self)

    @staticmethod
    def value_function_fn(x_strat, cell_corners, value_corners, step_grid, n):
        # Strategic value function computed using multilinear grid 
        # interpolation.
        start_time = time.time()
        sumterms = []
        volume = step_grid.prod()
        for i in itertools.product(range(2), repeat=n):
            partial_volume = [((-1)**(i[j]+1) * 
                                (x_strat[j] - cell_corners[j]) +
                                (1-i[j]) * step_grid[j]) for j in range(n)]
            partial_volume = np.asarray(partial_volume).prod() # convert to array to use prod.
            sumterm = value_corners[i]*partial_volume/volume
            sumterms.append(sumterm)
        sum_val = sum(sumterms)
        end_time = time.time()
        time_profile.value_function_time_profile.update(start_time, end_time)
        return sum_val

    def update_corners(self):
        # Update the corner values of the strategic cell grid by determining
        # which grid cell the current strategic state belongs to.
        cell_corners, vR_corners, vH_corners = (HierarchicalMaximizer
            .update_corners_fn(self.x_strat_func(), self.n, 
                self.disc_grid, self.vH_grid, self.vR_grid))
        self.cell_corners.set_value(cell_corners)
        self.vR_corners.set_value(vR_corners)
        self.vH_corners.set_value(vH_corners)

    @staticmethod
    def update_corners_fn(x_strat, n, disc_grid, vH_grid, vR_grid):
        # Update the corner values of the strategic cell grid by determining
        # which grid cell the current strategic state belongs to.
        start_time = time.time()
        # outside (length n) has outside[i] True if the value of the strategi state
        # at that index is outside the strategic domain. Then either project back
        # onto the strategic grid, or set the value function = 0 
        # (i.e. just consider tactical reward)
        outside = []
        inds = []
        cell_corners_new = []
        for i in range(n):
            if x_strat[i] < disc_grid[i][0]:
                ind = 0
                # only set value=0 if not projecting onto grid
                outside.append(True)
            elif x_strat[i] > disc_grid[i][-1]:
                ind = len(disc_grid[i]) - 1 # was - 2
                # only set value=0 if not projecting onto grid
                outside.append(True)
            else:
                ind = np.where(disc_grid[i] <= x_strat[i])[0][-1]
                outside.append(False) # inside the strategid domain
            inds.append(ind)
            cell_corners_new.append(disc_grid[i][ind])

        # debugging
        # if outside:
        #     print 'OUTSIDE grid interpolation!'
        # else:
        #     print 'INSIDE grid interpolation'

        cell_corners_new = np.array(cell_corners_new)
        # self.cell_corners.set_value(cell_corners_new)
        vH_corners_new = np.zeros([2 for i in range(n)])
        vR_corners_new = np.zeros([2 for i in range(n)])
        if not any(outside) or config.PROJECT_ONTO_STRAT_GRID:
            # iterate through unit vectors representing the corners of the grid
            # with dimension n
            for i in itertools.product(range(2), repeat=n):
                # gp_ind = tuple([sum(pair) for pair in zip(inds, list(i))]) # tuple to just be compatible with below.
                gp_ind = [] # list of indices of the grid cell's corners
                for j, (ind, direction, dimension) in enumerate(zip(inds, list(i), vH_grid.shape)):
                    # ind: index of grid cell "smaller" than the strategic state
                    # direction: vector specifying the grid cell corner
                    # dimension: length of the grid in this dimension
                    if outside[j]:
                        # if this state variable of the strategic state is outside
                        # of the strategic grid, project it back onto the grid
                        # by setting its index to be either 0 or dimension - 1
                        # (this is set above)
                        gp_ind.append(ind)
                    else:
                        # clip to dimension - 1 to avoid index out of bounds error
                        gp_ind.append(min(ind + direction, dimension - 1))
                gp_ind = tuple(gp_ind) # tuple to use for indexing into value grids
                try:
                    vH_corners_new[i] = vH_grid[gp_ind]
                    vR_corners_new[i] = vR_grid[gp_ind]
                except Exception as e:
                    print e
                    pdb.set_trace()
        # self.vH_corners.set_value(vH_corners_new)
        # self.vR_corners.set_value(vR_corners_new)
        end_time = time.time()
        time_profile.update_corners_time_profile.update(start_time, end_time)
        return cell_corners_new, vR_corners_new, vH_corners_new


class PredictReactMaximizer(NestedMaximizer):
    def init_grads(self):
        """Initialize the gradients based on the rewards.
        Precondition: the rewards (self.r_h and self.r_r) have already been 
        initialized.
        """
        # gradient of human reward wrt human controls
        self.dr_h = grad(self.r_h, self.plan_h)
        # negative human reward and its derivative
        self.func1 = th.function([], [-self.r_h, -self.dr_h])
        def r_h_and_dr_h(plan_h_0):
            """Evaluate negative human reward and its derivative.
            - plan_h_0: initial value for human plan."""
            start_time = time.time()
            # set plan_h to the given (initial) plan_h_0
            for v, (a, b) in zip(self.plan_h, self.control_indices_h):
                v.set_value(plan_h_0[a:b])
            # do any necessary updates based on the current plan
            # (this is necessary when using a strategic value)
            self.update_with_curr_plan_fn()
            func1_val = self.func1() # negative human reward and its derivative
            end_time = time.time()
            time_profile.inner_loop_time_profile.update(start_time, end_time)
            return func1_val
        self.r_h_and_dr_h = r_h_and_dr_h

        # ------------------------------------------------------------------------------------------
        # Robot's reward and its derivative.

        # ------------------------------------------------------------------------------------------
        if self.use_second_order:
            # OPTION 1: Full derivative computation with Hessian inversion. 
            # SLOW, DEPRECATED
            # jacobian of (d human reward / d robot actions) w.r.t. human actions
            J = jacobian(grad(self.r_h, self.plan_r), self.plan_h)
            # hessian of human reward w.r.t. human actions
            H = hessian(self.r_h, self.plan_h)
            # d robot reward / d human actions
            g = grad(self.r_r, self.plan_h)
            # Below is the most time-consuming step (the solve(H,g))
            self.dr_r = -tt.dot(J, ts.solve(H, g))+grad(self.r_r, self.plan_r)
        # ------------------------------------------------------------------------------------------
        else:
            # OPTION 2: Partial derivative computation. FAST
            # (Only direct effect of robot action given current human action)
            # Below is the simplified derivative that neglects the second-order 
            # effect through human (and therefore avoids the heavy Hessian 
            # inversion)
            self.dr_r = grad(self.r_r, self.plan_r)
        # ------------------------------------------------------------------------------------------

        # negative robot reward and its derivative
        self.func2 = th.function([], [-self.r_r, -self.dr_r])
        def r_r_and_dr_r(plan_r_0):
            """Get optimal human response, and return negative robot reward 
            and its derivative.
            - plan_r_0: initial value for robot plan."""
            start_time = time.time()
            # set self.plan_r to the given (initial) plan_r_0
            for v, (a, b) in zip(self.plan_r, self.control_indices_r):
                v.set_value(plan_r_0[a:b])
            # do any necessary updates based on the current plan
            # (this is necessary when using a strategic value)
            self.update_with_curr_plan_fn()
            func2_val = self.func2() # negative robot reward and its derivative
            end_time = time.time()
            time_profile.func2_time_profile.update(start_time, end_time)
            return func2_val
        self.r_r_and_dr_r = r_r_and_dr_r

    def maximize(self, bounds={}):
        """Optimize the robot's and human's plans with respect to their rewards
        using the predict-then-react scheme:
        1) "Predict" the human's plan by optimizing the human's plan w.r.t. its
            reward.
        2) Optimize the robot's plan w.r.t. its reward by treating the human as
            a moving obstacle following the "predicted" human plan.
        """
        # Get optimal robot plan (controls) and human response using nested
        # optimization.
        # start_time = time.time()
        # bounds_list = [robot_bounds, human_bounds]
        # plan_list = [self.plan_r, self.plan_h]
        # control_indices_list = [self.control_indices_r, self.control_indices_h]
        # opt_bounds_list = [] # bounds to pass into optimization
        # for i, (bounds, plan, control_indices) in enumerate(zip(
        #                         bounds_list, plan_list, control_indices_list)):
        #     if not isinstance(bounds, dict): # convert bounds to dictionary
        #         bounds = {v: bounds for v in plan}
        #     B = [] # list of bounds for each control in the plan
        #     for v, (a, b) in zip(plan, control_indices):
        #         if v in bounds:
        #             B += bounds[v]
        #         else:
        #             B += [(None, None)]*(b-a)
        #     opt_bounds_list.append(B)
        # opt_robot_bounds, opt_human_bounds = opt_bounds_list
        
        start_time = time.time()
        if not isinstance(bounds, dict): # convert bounds to dictionary
            bounds = {v: bounds for v in self.plan_r}
        B = [] # list of bounds for each control in the plan
        for v, (a, b) in zip(self.plan_r, self.control_indices_r):
            if v in bounds:
                B += bounds[v]
            else:
                B += [(None, None)]*(b-a)
        
        opt_robot_bounds = B
        opt_human_bounds = B

        opt_r_list = [] # list of robot optimization results
        opt_h_list = [] # list of human optimization results
        for i in range(self.num_optimizations_r):
            # TODO: can we replace the .get_value() approach with using the numpy
            # version because at this point the Theano and numpy plans are the same?
            # plan_r_0 = np.hstack(self.traj_r.u) # initial robot plan (numpy version)
            plan_r_0 = self.get_init_plan_r_fn(i)() # initialize the robot's plan
            # plan_r_0 = np.hstack([v.get_value() for v in self.plan_r])
            for j in range(self.num_optimizations_h):
                
                # debugging
                # print('robot optimization iter:', i)
                # print('human optimization iter:', j)

                # get the human's plan initialization function
                plan_h_0 = self.get_init_plan_h_fn(j)()

                # optimal human control, value, etc.
                opt_h = opt_timeup.fmin_l_bfgs_b_timeup(self.r_h_and_dr_h, 
                    x0=plan_h_0, bounds=opt_human_bounds, t0=start_time, timeup=self.timeup)
                opt_h_list.append(opt_h)
                opt_plan_h = opt_h[0] # optimal human control

                # Set the robot's belief of the human plan to the predicted/planned
                # human plan
                for v, (a, b) in zip(self.plan_h, self.control_indices_h):
                    v.set_value(opt_plan_h[a:b])

                # optimal robot control, value, etc.
                opt_r = opt_timeup.fmin_l_bfgs_b_timeup(self.r_r_and_dr_r, 
                    x0=plan_r_0, bounds=opt_robot_bounds, t0=start_time, timeup=self.timeup)
                opt_r_list.append(opt_r)

        # get the best plan based on its value
        opt_r_vals = [opt[1] for opt in opt_r_list] # list of values for robot
        best_opt_r_idx = np.argmin(opt_r_vals)
        opt_r = opt_r_list[best_opt_r_idx]
        opt_plan_r = opt_r[0] # optimal robot control
        
        opt_h = opt_h_list[best_opt_r_idx]
        opt_plan_h = opt_h[0] # human control corresponding to optimal robot control
        
        # debugging
        # print('opt_r_list:', opt_r_list)
        # print('opt_r:', opt_r)

        # Set optimal plans in Theano
        for v, (a, b) in zip(self.plan_r, self.control_indices_r):
            v.set_value(opt_plan_r[a:b])
        for v, (a, b) in zip(self.plan_h, self.control_indices_h):
            v.set_value(opt_plan_h[a:b])

        # time profile of HierarchicalMaximizer
        maximize_end_time = time.time()
        time_profile.maximizer_time_profile.update(start_time, maximize_end_time)
        return opt_r, opt_h

# TODO: make this more modular so there isn't so much copied code
class PredictReactHierarchicalMaximizer(PredictReactMaximizer):
    def __init__(self, r_h, traj_h, r_r, traj_r, mat_name, n, 
        proj, traj_truck=None, use_timeup=True, use_second_order=False,
        init_plan_scheme='prev_opt',
        disc_grid=None, step_grid=None, vH_grid=None, vR_grid=None):
        """
        Arguments
        - r_h: the human tactical reward.
        - traj_h: the human trajectory.
        - r_r: the robot tactical reward.
        - traj_r: the robot trajectory.
        - mat_name: the matlab file with the value function grids.
        - n: the number of dimensions of the strategic level.
        - proj: function specifying the projection from the tactical level to the strategic level.
        - traj_truck: the truck trajectory. If None, the truck is not used in the
            strategic value.
        """

        # ---------------------------------------------------------------------------------------------------
        # Basics.

        PredictReactMaximizer.__init__(self, r_h, traj_h, r_r, traj_r, 
            use_timeup=use_timeup, 
            use_second_order=use_second_order, 
            update_with_curr_plan_fn=self.update_corners,
            init_plan_scheme=init_plan_scheme,
            init_grads=False)

        self.n = n # dimension of strategic state
        self.x_tact_h = traj_h.x_th[-1] # final human tactical state
        self.x_tact_r = traj_r.x_th[-1] # final robot tactical state
        if traj_truck is not None:
            self.x_tact_truck = traj_truck.x_th[-1]

        # ---------------------------------------------------------------------------------------------------
        # Shared varables.

        # Grid interpolation is done with the grid corners of the current grid 
        # cell the state is in. These grid corners are shared variables which 
        # are updated as the state is updated. Since the grid step lengths 
        # are given, only the lower corners (self.cell_corners below) are needed 
        # as shared variables.
        self.cell_corners = th.shared(np.zeros(self.n)) # corners of each box in grid
        # corners for human value function
        self.vH_corners = th.shared(np.zeros([2 for i in range(n)]))
        # corners for robot value function
        self.vR_corners = th.shared(np.zeros([2 for i in range(n)]))

        # ---------------------------------------------------------------------------------------------------
        # Load grid data.
        if (disc_grid is None or step_grid is None or vH_grid is None or 
                    vR_grid is None):
            self.disc_grid, self.step_grid, self.vH_grid, self.vR_grid = (
                utils.load_grid_data(mat_name, n=self.n))
        else:
            self.disc_grid, self.step_grid, self.vH_grid, self.vR_grid = (
                disc_grid, step_grid, vH_grid, vR_grid)

        # ---------------------------------------------------------------------------------------------------
        # Value functions.

        # strategic state (project using Theano)
        if traj_truck is not None:
            self.x_strat = proj(self.x_tact_r, self.x_tact_h, self.x_tact_truck)
        else:
            self.x_strat = proj(self.x_tact_r, self.x_tact_h)
        self.x_strat_func = th.function([], self.x_strat)

        def value_function(value_corners):
            return HierarchicalMaximizer.value_function_fn(self.x_strat, 
                self.cell_corners, value_corners, self.step_grid, self.n)

        self.vR = value_function(self.vR_corners) # robot value function
        self.vH = value_function(self.vH_corners) # human value function

        # ---------------------------------------------------------------------------------------------------
        # Human's reward and its derivative.

        # add strategic value function
        self.r_h += config.STRATEGIC_VALUE_SCALE * self.vH

        # ------------------------------------------------------------------------------------------
        # Robot's reward and its derivative.

        # add strategic value function
        self.r_r += config.STRATEGIC_VALUE_SCALE * self.vR

        # initialize the gradients
        PredictReactMaximizer.init_grads(self)

    @staticmethod
    def value_function_fn(x_strat, cell_corners, value_corners, step_grid, n):
        # Strategic value function computed using multilinear grid 
        # interpolation.
        start_time = time.time()
        sumterms = []
        volume = step_grid.prod()
        for i in itertools.product(range(2), repeat=n):
            partial_volume = [((-1)**(i[j]+1) * 
                                (x_strat[j] - cell_corners[j]) +
                                (1-i[j]) * step_grid[j]) for j in range(n)]
            partial_volume = np.asarray(partial_volume).prod() # convert to array to use prod.
            sumterm = value_corners[i]*partial_volume/volume
            sumterms.append(sumterm)
        sum_val = sum(sumterms)
        end_time = time.time()
        time_profile.value_function_time_profile.update(start_time, end_time)
        return sum_val

    def update_corners(self):
        # Update the corner values of the strategic cell grid by determining
        # which grid cell the current strategic state belongs to.
        cell_corners, vR_corners, vH_corners = (HierarchicalMaximizer
            .update_corners_fn(self.x_strat_func(), self.n, 
                self.disc_grid, self.vH_grid, self.vR_grid))
        self.cell_corners.set_value(cell_corners)
        self.vR_corners.set_value(vR_corners)
        self.vH_corners.set_value(vH_corners)

    @staticmethod
    def update_corners_fn(x_strat, n, disc_grid, vH_grid, vR_grid):
        # Update the corner values of the strategic cell grid by determining
        # which grid cell the current strategic state belongs to.
        start_time = time.time()
        # outside (length n) has outside[i] True if the value of the strategi state
        # at that index is outside the strategic domain. Then either project back
        # onto the strategic grid, or set the value function = 0 
        # (i.e. just consider tactical reward)
        outside = []
        inds = []
        cell_corners_new = []
        for i in range(n):
            if x_strat[i] < disc_grid[i][0]:
                ind = 0
                # only set value=0 if not projecting onto grid
                outside.append(True)
            elif x_strat[i] > disc_grid[i][-1]:
                ind = len(disc_grid[i]) - 1 # was - 2
                # only set value=0 if not projecting onto grid
                outside.append(True)
            else:
                ind = np.where(disc_grid[i] <= x_strat[i])[0][-1]
                outside.append(False) # inside the strategid domain
            inds.append(ind)
            cell_corners_new.append(disc_grid[i][ind])

        # debugging
        # if outside:
        #     print 'OUTSIDE grid interpolation!'
        # else:
        #     print 'INSIDE grid interpolation'

        cell_corners_new = np.array(cell_corners_new)
        # self.cell_corners.set_value(cell_corners_new)
        vH_corners_new = np.zeros([2 for i in range(n)])
        vR_corners_new = np.zeros([2 for i in range(n)])
        if not any(outside) or config.PROJECT_ONTO_STRAT_GRID:
            # iterate through unit vectors representing the corners of the grid
            # with dimension n
            for i in itertools.product(range(2), repeat=n):
                # gp_ind = tuple([sum(pair) for pair in zip(inds, list(i))]) # tuple to just be compatible with below.
                gp_ind = [] # list of indices of the grid cell's corners
                for j, (ind, direction, dimension) in enumerate(zip(inds, list(i), vH_grid.shape)):
                    # ind: index of grid cell "smaller" than the strategic state
                    # direction: vector specifying the grid cell corner
                    # dimension: length of the grid in this dimension
                    if outside[j]:
                        # if this state variable of the strategic state is outside
                        # of the strategic grid, project it back onto the grid
                        # by setting its index to be either 0 or dimension - 1
                        # (this is set above)
                        gp_ind.append(ind)
                    else:
                        # clip to dimension - 1 to avoid index out of bounds error
                        gp_ind.append(min(ind + direction, dimension - 1))
                gp_ind = tuple(gp_ind) # tuple to use for indexing into value grids
                try:
                    vH_corners_new[i] = vH_grid[gp_ind]
                    vR_corners_new[i] = vR_grid[gp_ind]
                except Exception as e:
                    print e
                    pdb.set_trace()
        # self.vH_corners.set_value(vH_corners_new)
        # self.vR_corners.set_value(vR_corners_new)
        end_time = time.time()
        time_profile.update_corners_time_profile.update(start_time, end_time)
        return cell_corners_new, vR_corners_new, vH_corners_new

# Old HierarchicalMaximizer: duplicated a lot of code from the NestedMaximizer
# class HierarchicalMaximizer(object):
#     # The following class maximizes the hierarchical game between the robot (leader)
#     # and the human (follower). The tactic reward is given analytically as inputs
#     # while the terminal rewards given as the value functions of the strategic level
#     # is loaded into the class as grids. To get the value from the value functions,
#     # grid interpltion is used (see code below for details).
#     def __init__(self, r_h, traj_h, r_r, traj_r, mat_name, n, 
#         proj, use_timeup=True, use_second_order=False,
#         disc_grid=None, step_grid=None, vH_grid=None, vR_grid=None):
#         # The input parameters are:
#         #     - r_h: the human tactical reward.
#         #     - traj_h: the human trajectory.
#         #     - r_r: the robot tactical reward.
#         #     - traj_r: the robot trajectory.
#         #     - mat_name: the matlab file with the value function grids.
#         #     - n: the number of dimensions of the strategic level.
#         #     - proj: function specifying the projection from the tactical level to the strategic level.

#         # ---------------------------------------------------------------------------------------------------
#         # Basics.

#         self.n = n # dimension of strategic state
#         self.r_h = r_h
#         self.r_r = r_r
#         self.x_tact_h = traj_h.x_th[-1] # final human tactical state
#         self.x_tact_r = traj_r.x_th[-1] # final robot tactical state
#         self.plan_h = traj_h.u_th # human plan (controls)
#         self.plan_r = traj_r.u_th # robot plan (controls)
#         # (start, end) indices for each control in the plan when it's represented
#         # as a flattened array. Ex: [(0, 2), (2, 4), (4, 6), (6, 8), (8, 10)]
#         self.control_indices_h = traj_h.control_indices
#         self.control_indices_r = traj_r.control_indices
#         # maximum time for optimization
#         if use_timeup:
#             self.timeup = config.OPT_TIMEOUT
#         else:
#             self.timeup = float('inf')

#         # ---------------------------------------------------------------------------------------------------
#         # Shared varables.

#         # Grid interpolation is done with the grid corners of the current grid 
#         # cell the state is in. These grid corners are shared variables which 
#         # are updated as the state is updated. Since the grid step lengths 
#         # are given, only the lower corners (self.cell_corners below) are needed 
#         # as shared variables.
#         self.cell_corners = th.shared(np.zeros(self.n)) # corners of each box in grid
#         # corners for human value function
#         self.vH_corners = th.shared(np.zeros([2 for i in range(n)]))
#         # corners for robot value function
#         self.vR_corners = th.shared(np.zeros([2 for i in range(n)]))

#         # ---------------------------------------------------------------------------------------------------
#         # Load grid data.
#         if (disc_grid is None or step_grid is None or vH_grid is None or 
#                     vR_grid is None):
#             self.disc_grid, self.step_grid, self.vH_grid, self.vR_grid = (
#                 utils.load_grid_data(mat_name, n=self.n))
#         else:
#             self.disc_grid, self.step_grid, self.vH_grid, self.vR_grid = (
#                 disc_grid, step_grid, vH_grid, vR_grid)

#         # ---------------------------------------------------------------------------------------------------
#         # Value functions.

#         # strategic state (project using Theano)
#         self.x_strat = proj(self.x_tact_r, self.x_tact_h)
#         self.x_strat_func = th.function([], self.x_strat)

#         def value_function(value_corners):
#             return HierarchicalMaximizer.value_function_fn(self.x_strat, 
#                 self.cell_corners, value_corners, self.step_grid, self.n)

#         self.vR = value_function(self.vR_corners) # robot value function
#         self.vH = value_function(self.vH_corners) # human value function

#         # ---------------------------------------------------------------------------------------------------
#         # Human's reward and its derivative.

#         # add strategic value function
#         self.r_h += config.STRATEGIC_VALUE_SCALE * self.vH

#         # gradient of human reward wrt human controls
#         self.dr_h = grad(self.r_h, self.plan_h)
#         # negative human reward and its derivative
#         self.func1 = th.function([], [-self.r_h, -self.dr_h])
#         def r_h_and_dr_h(plan_h_0):
#             """Evaluate negative human reward and its derivative.
#             - plan_h_0: initial value for human plan."""
#             start_time = time.time()
#             # set plan_h to the given (initial) plan_h_0
#             for v, (a, b) in zip(self.plan_h, self.control_indices_h):
#                 v.set_value(plan_h_0[a:b])
#             # update strategic value corners according to current grid cell
#             self.update_corners()
#             func1_val = self.func1() # negative human reward and its derivative
#             end_time = time.time()
#             time_profile.inner_loop_time_profile.update(start_time, end_time)
#             return func1_val
#         self.r_h_and_dr_h = r_h_and_dr_h

#         # ------------------------------------------------------------------------------------------
#         # Robot's reward and its derivative.

#         # add strategic value function
#         self.r_r += config.STRATEGIC_VALUE_SCALE * self.vR

#         # ------------------------------------------------------------------------------------------
#         if use_second_order:
#             # OPTION 1: Full derivative computation with Hessian inversion. 
#             # SLOW, DEPRECATED
#             # jacobian of (d human reward / d robot actions) w.r.t. human actions
#             J = jacobian(grad(self.r_h, self.plan_r), self.plan_h)
#             # hessian of human reward w.r.t. human actions
#             H = hessian(self.r_h, self.plan_h)
#             # d robot reward / d human actions
#             g = grad(self.r_r, self.plan_h)
#             # Below is the most time-consuming step (the solve(H,g))
#             self.dr_r = -tt.dot(J, ts.solve(H, g))+grad(self.r_r, self.plan_r)
#         # ------------------------------------------------------------------------------------------
#         else:
#             # OPTION 2: Partial derivative computation. FAST
#             # (Only direct effect of robot action given current human action)
#             # Below is the simplified derivative that neglects the second-order 
#             # effect through human (and therefore avoids the heavy Hessian 
#             # inversion)
#             self.dr_r = grad(self.r_r, self.plan_r)
#         # ------------------------------------------------------------------------------------------

#         # negative robot reward and its derivative
#         self.func2 = th.function([], [-self.r_r, -self.dr_r])
#         def r_r_and_dr_r(plan_r_0):
#             """Get optimal human response, and return negative robot reward 
#             and its derivative.
#             - plan_r_0: initial value for robot plan."""
#             # set self.plan_r to the given (initial) plan_r_0
#             for v, (a, b) in zip(self.plan_r, self.control_indices_r):
#                 v.set_value(plan_r_0[a:b])
#             self.maximize_inner() # get optimal human response
#             start_time = time.time()
#             func2_val = self.func2() # negative robot reward and its derivative
#             end_time = time.time()
#             time_profile.func2_time_profile.update(start_time, end_time)
#             return func2_val
#         self.r_r_and_dr_r = r_r_and_dr_r

#     @staticmethod
#     def value_function_fn(x_strat, cell_corners, value_corners, step_grid, n):
#         # Strategic value function computed using multilinear grid 
#         # interpolation.
#         start_time = time.time()
#         sumterms = []
#         volume = step_grid.prod()
#         for i in itertools.product(range(2), repeat=n):
#             partial_volume = [((-1)**(i[j]+1) * 
#                                 (x_strat[j] - cell_corners[j]) +
#                                 (1-i[j]) * step_grid[j]) for j in range(n)]
#             partial_volume = np.asarray(partial_volume).prod() # convert to array to use prod.
#             sumterm = value_corners[i]*partial_volume/volume
#             sumterms.append(sumterm)
#         sum_val = sum(sumterms)
#         end_time = time.time()
#         time_profile.value_function_time_profile.update(start_time, end_time)
#         return sum_val

#     def update_corners(self):
#         # Update the corner values of the strategic cell grid by determining
#         # which grid cell the current strategic state belongs to.
#         cell_corners, vR_corners, vH_corners = (HierarchicalMaximizer
#             .update_corners_fn(self.x_strat_func(), self.n, 
#                 self.disc_grid, self.vH_grid, self.vR_grid))
#         self.cell_corners.set_value(cell_corners)
#         self.vR_corners.set_value(vR_corners)
#         self.vH_corners.set_value(vH_corners)

#     @staticmethod
#     def update_corners_fn(x_strat, n, disc_grid, vH_grid, vR_grid):
#         # Update the corner values of the strategic cell grid by determining
#         # which grid cell the current strategic state belongs to.
#         start_time = time.time()
#         # outside is True if outside the strategic domain. Then value function = 0 
#         # (i.e. just consider tactical reward)
#         outside = False
#         inds = []
#         cell_corners_new = []
#         for i in range(n):
#             if disc_grid[i][0] > x_strat[i]:
#                 ind = 0
#                 outside = True
#             elif disc_grid[i][-1] < x_strat[i]:
#                 ind = len(disc_grid[i])-2
#                 outside = True
#             else:
#                 ind = np.where(disc_grid[i] <= x_strat[i])[0][-1]
#             inds.append(ind)
#             cell_corners_new.append(disc_grid[i][ind])

#         # debugging
#         # if outside:
#         #     print 'OUTSIDE grid interpolation!'
#         # else:
#         #     print 'INSIDE grid interpolation'

#         cell_corners_new = np.array(cell_corners_new)
#         # self.cell_corners.set_value(cell_corners_new)
#         vH_corners_new = np.zeros([2 for i in range(n)])
#         vR_corners_new = np.zeros([2 for i in range(n)])
#         if not outside:
#             # iterate through unit vectors representing the corners of the grid
#             # with dimension n
#             for i in itertools.product(range(2), repeat=n):
#                 # gp_ind = tuple([sum(pair) for pair in zip(inds, list(i))]) # tuple to just be compatible with below.
#                 gp_ind = [] # list of indices of the grid cell's corners
#                 for ind, direction, dimension in zip(inds, list(i), vH_grid.shape):
#                     # ind: index of grid cell "smaller" than the strategic state
#                     # direction: vector specifying the grid cell corner
#                     # dimension: length of the grid in this dimension
#                     # clip to dimension - 1 to avoid index out of bounds error
#                     gp_ind.append(min(ind + direction, dimension - 1))
#                 gp_ind = tuple(gp_ind) # tuple to use for indexing into value grids
#                 try:
#                     vH_corners_new[i] = vH_grid[gp_ind]
#                     vR_corners_new[i] = vR_grid[gp_ind]
#                 except Exception as e:
#                     print e
#                     pdb.set_trace()
#         # self.vH_corners.set_value(vH_corners_new)
#         # self.vR_corners.set_value(vR_corners_new)
#         end_time = time.time()
#         time_profile.update_corners_time_profile.update(start_time, end_time)
#         return cell_corners_new, vR_corners_new, vH_corners_new

#     def maximize_inner(self, bounds={}, maxiter=config.NESTEDMAX_MAXITER_INNER):
#         """Get optimal human response (controls).
#         Arguments:
#         - bounds: control bounds for the human.
#         - maxiter: maximum number of iterations.
#         """
#         start_time = time.time()
#         # initialize human plan to previous optimal value
#         plan_h_0 = np.hstack([v.get_value() for v in self.plan_h])
#         bounds = constants.HIERARCHICAL_HUMAN_CONTROL_BOUNDS
#         if not isinstance(bounds, dict): # convert bounds to dictionary
#             bounds = {v: bounds for v in self.plan_h}
#         B = [] # list of bounds for each control in the plan
#         for v, (a, b) in zip(self.plan_h, self.control_indices_h):
#             if v in bounds:
#                 B += bounds[v]
#             else:
#                 B += [(None, None)]*(b-a)
#         # optimal human response, value, etc.
#         opt_h = scipy.optimize.fmin_l_bfgs_b(self.r_h_and_dr_h, x0=plan_h_0, 
#                 bounds=B)
#         opt_plan_h = opt_h[0] # optimal human response
#         for v, (a, b) in zip(self.plan_h, self.control_indices_h):
#             v.set_value(opt_plan_h[a:b])
#         # update strategic value corners according to current grid cell
#         self.update_corners()
#         end_time = time.time()
#         time_profile.maximize_inner_time_profile.update(start_time, end_time)
#         return opt_h

#     def maximize(self, bounds={}, bounds_inner={}, 
#                 maxiter_inner=config.NESTEDMAX_MAXITER_INNER):
#         # Get optimal robot plan (controls) and human response using nested
#         # optimization.
#         start_time = time.time()
#         if not isinstance(bounds, dict): # convert bounds to dictionary
#             bounds = {v: bounds for v in self.plan_r}
#         B = [] # list of bounds for each control in the plan
#         for v, (a, b) in zip(self.plan_r, self.control_indices_r):
#             if v in bounds:
#                 B += bounds[v]
#             else:
#                 B += [(None, None)]*(b-a)
#         # TODO: can we replace the .get_value() approach with using the numpy
#         # version because at this point the Theano and numpy plans are the same?
#         # plan_r_0 = np.hstack(self.traj_r.u) # initial robot plan (numpy version)
#         plan_r_0 = np.hstack([v.get_value() for v in self.plan_r])
        
#         # optimal robot control, value, etc.
#         opt_r = opt_timeup.fmin_l_bfgs_b_timeup(self.r_r_and_dr_r, 
#             x0=plan_r_0, bounds=B, t0=start_time, timeup=self.timeup)
#         opt_plan_r = opt_r[0] # optimal robot control

#         # TODO: remove?
#         for v, (a, b) in zip(self.plan_r, self.control_indices_r):
#             v.set_value(opt_plan_r[a:b])

#         # time profile of HierarchicalMaximizer
#         maximize_end_time = time.time()
#         time_profile.maximizer_time_profile.update(start_time, maximize_end_time)
        
#         # optimal human response, value, etc. to optimal robot control
#         opt_h = self.maximize_inner(bounds=bounds_inner, maxiter=maxiter_inner)
#         return opt_r, opt_h

