import numpy as np
import theano.tensor as tt
import torch

import constants

class Dynamics(object):
    def __init__(self, nx, nu, f, fw, dt=None):
        # nx: state dimension
        # nu: control dimension
        # f: dynamics derivative function
        # fw: computational framework (numpy or Theano)
        # dt: timestep
        assert(fw == np or fw == tt or fw == torch) # Framework must be either numpy or theano.tensor
        self.nx = nx
        self.nu = nu
        self.dt = dt
        # Set numpy or Theano version of dynamics derivative function f
        if fw == np:
            f_fw = lambda x, u: np.array(f(x, u))
        elif fw == tt:
            f_fw = lambda x, u: tt.stacklists(f(x, u))
        elif fw == torch:
            f_fw = lambda x, u: torch.stack(f(x, u))
        
        if dt is not None:
            self.f = lambda x, u: x + dt * f_fw(x, u)
        else:
            self.f = f_fw

    def __call__(self, x, u):
        return self.f(x, u)

class CarDynamicsUnicycle(Dynamics):
    """Unicycle model
    State: [x, y, heading (theta), velocity]
    """
    def __init__(self, fw, dt=0.1, ub=constants.CAR_CONTROL_BOUNDS, 
                friction=constants.FRICTION):
        def f(x, u):
            return [
                x[3]*fw.cos(x[2]),
                x[3]*fw.sin(x[2]),
                x[3]*u[0],
                u[1]-x[3]*friction
            ]

        Dynamics.__init__(self, constants.STATE_DIM, constants.CONTROL_DIM, f, 
            fw, dt)


class CarDynamics(Dynamics):
    """Bicycle model
    State: [x, y, heading (theta), velocity]
    """
    def __init__(
        self, fw, dt=0.1, ub=constants.CAR_CONTROL_BOUNDS,
        friction=constants.FRICTION, 
        wheelbase=constants.WHEELBASE*constants.METERS_TO_VIS):
        # friction for max-out at ~200km/h; old friction=0.008...
        def f(x, u):
            return [
                x[3]*fw.cos(x[2]),
                x[3]*fw.sin(x[2]),
                x[3]*fw.tan(u[0])/wheelbase,
                u[1]-friction*x[3]**2
            ]
        Dynamics.__init__(self,  constants.STATE_DIM, constants.CONTROL_DIM, f, 
            fw, dt)


# TODO: why take dt as an argument when passing in dt=None to Dynamics?
class TruckDynamics(Dynamics):
    # Truck model used for DSG setups.
    def __init__(self, fw, dt=0.1, ub=constants.TRUCK_CONTROL_BOUNDS, 
                 friction=constants.FRICTION):
        # The platoon is assumed to be lined in the positive y-direction (y due to experimental setup.)
        def f(x,u): # dynamics for one truck.
            return [
                x[0],
                (u[0]-friction*x[3]**2)*dt**2/2+x[3]*dt+x[1],
                x[2],
                (u[0]-friction*x[3]**2)*dt+x[3]
            ]
        Dynamics.__init__(self, constants.STATE_DIM, constants.TRUCK_CONTROL_DIM, 
            f, dt=None)

