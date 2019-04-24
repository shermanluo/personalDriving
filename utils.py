from collections import namedtuple
import pdb

import theano as th
import theano.tensor as tt
import theano.tensor.slinalg as ts
import scipy.optimize
import scipy.io
import numpy as np
import numpy.linalg as nl
import time
import itertools

import opt_timeup
import constants
import time_profile

# Sample in interaction history: (time, state, plan, tactical reward)
Sample = namedtuple('Sample', ['t', 's', 'plan', 'r'])
# Sample in interaction history for any car that computes a plan for the human 
# and does not have a strategic value(e.g. NestedCar): 
# (time, state, plan, predicted plan for human car, tactical reward)
NestedCarSample = namedtuple('Sample', ['t', 's', 'plan', 'plan_h', 'tact_r'])
# Sample in interaction history for HierarchicalCar: 
# (time, state, plan, predicted plan for human car, tactical reward, strategic value)
HierarchicalCarSample = namedtuple('Sample', ['t', 's', 'plan', 'plan_h', 'tact_r', 'strat_val'])

def extract(var):
    return th.function([], var, mode=th.compile.Mode(linker='py'))()

def shape(var):
    return extract(var.shape)

def th_vector(n):
    return th.shared(np.zeros(n))

def th_vector_from_value(value):
    return th.shared(value)

def th_matrix(n, m, value=None):
    return th.shared(np.zeros((n, m)))

def th_matrix_from_value(value):
    return th.shared(value)

def grad(f, x, constants=[]):
    ret = th.gradient.grad(f, x, consider_constant=constants, disconnected_inputs='warn')
    if isinstance(ret, list):
        ret = tt.concatenate(ret)
    return ret

def jacobian(f, x, constants=[]):
    sz = shape(f)
    return tt.stacklists([grad(f[i], x) for i in range(sz)])
    ret = th.gradient.jacobian(f, x, consider_constant=constants)
    if isinstance(ret, list):
        ret = tt.concatenate(ret, axis=1)
    return ret

def hessian(f, x, constants=[]):
    return jacobian(grad(f, x, constants=constants), x, constants=constants)

def sigmoid(x, a, c, fw):
    """Sigmoid function with scale parameter a and horizontal shift c, evaluated
    at point x using the framework fw (numpy or theano.tensor).
    """
    return 1. / (1. + fw.exp(-1. * a * (x - c)))

def interpolate_state(t, t1, t2, x1, x2):
    # Return interpolated state at time t between states x1 and x2, 
    # which occur at times t1 and t2 (respectively)
    if t1 == t2:
        return x1
    fraction = (t - t1) / (t2 - t1)
    return (1.0 - fraction) * x1 + fraction * x2

def state_dict_to_list(state_dict):
    x = state_dict['x']
    y = state_dict['y']
    orientation = state_dict['orientation']
    speed = state_dict['speed']
    return [x, y, orientation, speed]

def state_list_to_dict(state_list, time):
    return {'x': state_list[0], 'y': state_list[1], 
    'orientation': state_list[2], 'speed': state_list[3], 'time': time}

def viz_to_opends_control(steer_viz, gas_viz):
    # Convert from visualization controls to OpenDS controls.
    steer_opends = steer_viz * constants.K_STEER # multiply by scaling factor for opends
    if gas_viz < 0:
        brake_opends = gas_viz * constants.K_BRAKE # multiply by brake scaling factor for opends
        gas_opends = 0.0
    else:
        brake_opends = 0.0
        gas_opends = gas_viz * constants.K_ACCELERATION # multiply by scaling factor for opends
    return steer_opends, gas_opends, brake_opends

def load_grid_data(mat_name, n):
    # Load grid data.
    mat = scipy.io.loadmat(mat_name)
    disc_grid = [mat['sgvs'+str(i+1)][0] for i in range(n)]
    step_grid = mat['dx'][0]
    vH_grid = mat['vH'] # the grid of the human value function.
    vR_grid = mat['vR'] # the grid of the robot value function.

    # Replacing -inf and nan values with zero. These values happens outside the domain of the the 
    # strategic level. They are here replaced with zero here to employ the tactic control which
    # (hopefully) guide the car back to the strategic domain.
    vH_grid[vH_grid == -np.inf]=0
    vH_grid[vH_grid == np.nan]=0
    vR_grid[vR_grid == -np.inf]=0
    vR_grid[vR_grid == np.nan]=0

    return disc_grid, step_grid, vH_grid, vR_grid

def tact_to_strat_proj_3d(x_r, x_h):
    """Project the given robot and human tactical states to the 3D strategic state.

    The 3D strategic state is defined as [x_r, y_rel, v_rel], where
    - x_r: robot x-coordinate
    - y_rel: relative y-coordinate of the robot with respect to the y coordinate
        of the human
    - v_rel: the relative y-velocity of the robot with respect to the y-velocity 
        of the human (x-velocity neglected)
    """
    return ([
        x_r[0],
        x_r[1]-x_h[1],
        x_r[3]-x_h[3]
    ])

# def tact_to_strat_proj_3d_np(x_r, x_h):
#     """Project the given robot and human tactical states to the 3D strategic 
#     state using numpy.

#     The 3D strategic state is defined as [x_r, y_rel, v_rel], where
#     - x_r: robot x-coordinate
#     - y_rel: relative y-coordinate of the robot with respect to the y coordinate
#         of the human
#     - v_rel: the relative y-velocity of the robot with respect to the y-velocity 
#         of the human (x-velocity neglected)
#     """
#     return np.array([
#         x_r[0],
#         x_r[1]-x_h[1],
#         x_r[3]-x_h[3]
#     ])

def tact_to_strat_proj_4d(x_r, x_h):
    """Project the given robot and human tactical states to the 4D strategic state.

    The 4D strategic state is defined as [x_r, x_h, y_rel, v_rel], where
    - x_r: robot x-coordinate
    - x_h: human x-coordinate
    - y_rel: relative y-coordinate of the robot with respect to the y coordinate
        of the human
    - v_rel: the relative y-velocity of the robot with respect to the y-velocity 
        of the human (x-velocity neglected)
    """
    return ([
        x_r[0],
        x_h[0],
        x_r[1]-x_h[1],
        x_r[3]-x_h[3]
    ])

# def tact_to_strat_proj_4d_np(x_r, x_h):
#     """Project the given robot and human tactical states to the 4D strategic 
#     state using numpy.

#     The 4D strategic state is defined as [x_r, x_h, y_rel, v_rel], where
#     - x_r: robot x-coordinate
#     - x_h: human x-coordinate
#     - y_rel: relative y-coordinate of the robot with respect to the y coordinate
#         of the human
#     - v_rel: the relative y-velocity of the robot with respect to the y-velocity 
#         of the human (x-velocity neglected)
#     """
#     return np.array([
#         x_r[0],
#         x_h[0],
#         x_r[1]-x_h[1],
#         x_r[3]-x_h[3]
#     ])

def tact_to_strat_proj_truck_cut_in_5d(x_r, x_h, x_t):
    """Project the given robot, human, and truck tactical states to the 5D strategic
    state corresponding to the truck cut-in scenario.

    Arguments:
    - x_r: robot state
    - x_h: human state
    - x_t: truck state

    The strategic state is
        x = [xR, yR_rel, vR, yH_rel, vH]
    where
        - xR: the x-coordinate of the robot.
        - yR_rel: the relative y-coordinate of the robot with respect to the
          y-coordinate of the truck.
        - vR: the absolute y-velocity of the robot.
        - yH_rel: the relative y-coordinate of the human with respect to the
          y-coordinate of the truck.
        - vH: the absolute y-velocity of the human.
    """
    return ([
        x_r[0],
        x_r[1] - x_t[1],
        x_r[3],
        x_h[1] - x_t[1],
        x_h[3]
    ])

def tact_to_strat_proj_truck_cut_in_6d(x_r, x_h, x_t):
    """Project the given robot, human, and truck tactical states to the 5D strategic
    state corresponding to the truck cut-in scenario.

    Arguments:
    - x_r: robot state
    - x_h: human state
    - x_t: truck state

    The state is
        x = [xR, yR_rel, vR, xH, yH_rel, vH]
    where
        - xR: the x-coordinate of the robot.
        - yR_rel: the relative y-coordinate of the robot with respect to the
          y-coordinate of the truck.
        - vR: the absolute y-velocity of the robot.
        - xH: the x-coordinate of the human.
        - yH_rel: the relative y-coordinate of the human with respect to the
          y-coordinate of the truck.
        - vH: the absolute y-velocity of the human.
    """
    return ([
        x_r[0],
        x_r[1] - x_t[1],
        x_r[3],
        x_h[0],
        x_h[1] - x_t[1],
        x_h[3]
    ])

def strategic_reward_heatmap_coord(min_strat_state, max_strat_state, strat_dim,
        x_r=None, x_h=None, x_truck_func=None, project_onto_grid=True):
    """Given the minimum strategic state, maximum strategic state, and tactical 
    state x_r (x_h), give the minimum and maximum bounding coordinates (x, y) 
    for the strategic value of the other car (in custom vis units).

    - Note: Only one of the tactical states should be given as an argument.
    - Note: The human is assumed to be in the left lane, which dictates its 
        x position.

    Arguments:
    - min_strat_state: minimum value of the strategic state for eahch dimension
    - max_strat_state: maximum value of the strategic state for eahch dimension
    - x_r: robot tactical state that was projected to get x_strat
    - x_h: human tactical state that was projected to get x_strat
    """
    # XOR: only one of the states should be given
    assert((x_r is None and x_h is not None) or
        (x_r is not None and x_h is None))
    assert(strat_dim == 3 or strat_dim == 4 or strat_dim == 5 or strat_dim == 6)
    if project_onto_grid:
        return None # heatmap coordinates set by visualizer

    if x_r is not None: # return human strategic reward bounding coordinates
        if strat_dim == 3:
            min_coord = [-constants.LANE_WIDTH_VIS/2.0, x_r[1] - max_strat_state[1]]
            max_coord = [constants.LANE_WIDTH_VIS/2.0, x_r[1] - min_strat_state[1]]
        elif strat_dim == 4:
            min_coord = [min_strat_state[0], x_r[1] - max_strat_state[2]]
            max_coord = [max_strat_state[0], x_r[1] - min_strat_state[2]]
        elif strat_dim == 5:
            assert x_truck_func is not None
            x_truck = x_truck_func()
            min_coord = [-constants.LANE_WIDTH_VIS/2.0, x_truck[1] + min_strat_state[3]]
            max_coord = [constants.LANE_WIDTH_VIS/2.0, x_truck[1] + max_strat_state[3]]
        elif strat_dim == 6:
            assert x_truck_func is not None
            x_truck = x_truck_func()
            # min_coord = [-constants.LANE_WIDTH_VIS/2.0, x_truck[1] + min_strat_state[4]]
            # max_coord = [constants.LANE_WIDTH_VIS/2.0, x_truck[1] + max_strat_state[4]]
            min_coord = [min_strat_state[0], x_truck[1] + min_strat_state[4]]
            max_coord = [max_strat_state[0], x_truck[1] + max_strat_state[4]]
    else: # return robot strategic reward bounding coordinates
        if strat_dim == 3:
            # TODO: temporary fix to += 0.2 to avoid strategic value from looking
            # weird at the top and bottom bands. Fix this.
            min_coord = [min_strat_state[0], x_h[1] + min_strat_state[1] + 0.2]
            max_coord = [max_strat_state[0], x_h[1] + max_strat_state[1] - 0.2]
        elif strat_dim == 4:
            # TODO: temporary fix to += 0.2 to avoid strategic value from looking
            # weird at the top and bottom bands. Fix this.
            min_coord = [min_strat_state[0], x_h[1] + min_strat_state[2] + 0.2]
            max_coord = [max_strat_state[0], x_h[1] + max_strat_state[2] - 0.2]
        elif strat_dim == 5:
            assert x_truck_func is not None
            x_truck = x_truck_func()
            min_coord = [min_strat_state[0], x_truck[1] + min_strat_state[1]]
            max_coord = [max_strat_state[0], x_truck[1] + max_strat_state[1]]
        elif strat_dim == 6:
            assert x_truck_func is not None
            x_truck = x_truck_func()
            min_coord = [min_strat_state[0], x_truck[1] + min_strat_state[1]]
            max_coord = [max_strat_state[0], x_truck[1] + max_strat_state[1]]
    return min_coord, max_coord



# def update_corners(xNs, disc_grid, step_grid, value_grid, n=3):
#     # Updates the corner values by looking at which grid cell we are in.
#     #  - xNs: strategic state, which we get by projecting the human and robot tactical states.
#     start_time = time.time()
#     outside = 0 # is 1 if outside the strategic domain. Then value function = 0 (i.e. just consider tactic).

#     inds = []
#     gp = []
#     for i in range(n):
#         if disc_grid[i][0] > xNs[i]:
#             ind = 0
#             outside = 1
#         elif disc_grid[i][-1] < xNs[i]:
#             ind = len(disc_grid[i])-2
#             outside = 1
#         else:
#             ind = np.where(disc_grid[i] <= xNs[i])[0][-1]
#         inds.append(ind)
#         gp.append(disc_grid[i][ind])

#     # debugging #
#     # if outside == 1:
#     #     print('OBS: Now outside grid interpolation!')
#     # debugging #

#     cell_corners = np.array(gp)
#     value_corners = np.zeros([2 for i in range(n)])
#     if outside == 0:
#         for i in itertools.product(range(2), repeat=n):
#             gp_ind = tuple([sum(pair) for pair in zip(inds, list(i))]) # tuple to just be compatible with below.
#             value_corners[i] = value_grid[gp_ind]
#     end_time = time.time()
#     time_profile.update_corners_time_profile.update(start_time, end_time)
#     return cell_corners, value_corners

