import numpy as np
import theano.tensor as tt

import constants
import feature
from optimizer import HierarchicalMaximizer
import utils

class StrategicValue(object):
    def __init__(self, traj_r, traj_h, proj, mat_name, dim, scale,
        min_val, max_val, traj_truck=None):
        """
        Arguments:
        - traj_r: robot Trajectory object
        - traj_h: human Trajectory object
        - proj: Projection object specifying projection function from tactical to
            strategic state
        - mat_name: name of MATLAB file containing the strategic value.
        - dim: dimension of the strategic state.
        - scale: scalar multiplier for the strategic value
        - min_val: minimum possible strategic value (to be used for heatmap)
        - max_val: maximum possible strategic value (to be used for heatmap)
        - traj_truck: truck Trajectory object. If None, truck trajectory is not
            accounted for.
        """
        assert(dim == 3 or dim == 4 or dim == 5 or dim == 6)
        self.traj_r = traj_r
        self.traj_h = traj_h
        self.proj = proj
        self.mat_name = mat_name
        self.dim = dim
        self.scale = scale
        self.min_val = min_val
        self.max_val = max_val
        self.traj_truck = traj_truck
        self.use_truck = traj_truck is not None

        self.disc_grid, self.step_grid, self.vH_grid, self.vR_grid = (
            utils.load_grid_data(self.mat_name, self.dim))
        # Min and max values of the strategic state
        self.min_state = np.array([min(a) for a in self.disc_grid])
        self.max_state = np.array([max(a) for a in self.disc_grid])
        # robot's strategic value
        self.value_r_np = (self.scale * 
            self.get_strategic_value(constants.NAME_R, fw=np, use_truck=self.use_truck))
        self.value_r_th = (self.scale * 
            self.get_strategic_value(constants.NAME_R, fw=tt, use_truck=self.use_truck))
        # human's strategic value
        self.value_h_np = (self.scale * 
            self.get_strategic_value(constants.NAME_H, fw=np, use_truck=self.use_truck))
        self.value_h_th = (self.scale * 
            self.get_strategic_value(constants.NAME_H, fw=tt, use_truck=self.use_truck))

    def get_config(self):
        """Return JSON object describing the parameters of this strategic value."""
        return {
            'mat_name': self.mat_name,
            'dim': self.dim,
            'scale': self.scale,
            'min_state': self.min_state,
            'max_state': self.max_state
            }

    def get_strategic_value(self, car_name, fw, use_truck=False):
        """Return a feature that computes the strategic value for the robot car 
        given its tactical state.
        Arguments:
        - car_name: string specifying whether to return the robot's strategic value
            (constants.NAME_R) or the human's strategic value (constants.NAME_H)
        - fw: the computational framework to use, either numpy or theano.tensor
        - use_truck: if True, use the truck state to compute the strategic state.
            Else, only use the robot and human car states.
        """
        assert(car_name == constants.NAME_R or car_name == constants.NAME_H)
        assert(fw == np or fw == tt)
        def make_f(x_other_func, proj, car_name, use_truck=False, x_truck_func=None):
            """ 
            Arguments
            - x_other_func: function to compute the state of the other car.
                 When computing the robot's strategic value, the other car is the
                 human, and when computing the human's strategic value, the
                 other car is the robot.
            - proj: projection function from tactical states to strategic state
            - car_name: string specifying which car's strategic value to return.
                   See description in get_strategic_value.
            - x_truck_func: function to compute state of the truck.
            """
            assert (not use_truck) or (x_truck_func is not None)
            if car_name == constants.NAME_R:
                @feature.feature
                def strat_val_r(t, x_r, u_r):
                    """Compute the robot's strategic value."""
                    # t: time. Only needed to match Feature function signature
                    # x_r: robot tactical state
                    # u_r: robot control. Only needed to match Feature function signature
                    x_h = x_other_func() # human tactical state
                    if use_truck:
                        x_truck = x_truck_func()
                        x_strat = proj(x_r, x_h, x_truck)
                    else:
                        x_strat = proj(x_r, x_h) # strategic state
                    cell_corners, vR_corners, vH_corners = (HierarchicalMaximizer
                        .update_corners_fn(x_strat, self.dim, 
                            self.disc_grid, self.vH_grid, self.vR_grid))
                    # use vR_corners to compute robot's strategic value
                    return HierarchicalMaximizer.value_function_fn(
                        x_strat, cell_corners, vR_corners, self.step_grid, self.dim)
                return strat_val_r
            elif car_name == constants.NAME_H:
                @feature.feature
                def strat_val_h(t, x_h, u_h):
                    """Compute the human's strategic value."""
                    # t: time. Only needed to match Feature function signature
                    # x_h: human tactical state
                    # u_h: human control. Only needed to match Feature function signature
                    x_r = x_other_func() # robot tactical state
                    if use_truck:
                        x_truck = x_truck_func()
                        x_strat = proj(x_r, x_h, x_truck)
                    else:
                        x_strat = proj(x_r, x_h) # strategic state
                    cell_corners, vR_corners, vH_corners = (HierarchicalMaximizer
                        .update_corners_fn(x_strat, self.dim, 
                            self.disc_grid, self.vH_grid, self.vR_grid))
                    # use vH_corners to compute human's strategic value
                    return HierarchicalMaximizer.value_function_fn(
                        x_strat, cell_corners, vH_corners, self.step_grid, self.dim)
                return strat_val_h
        
        x_truck_func = None
        if fw == np:
            proj = self.proj.proj_np
            if car_name == constants.NAME_H:
                x_other_func = lambda: self.traj_r.x0 # robot numpy state
            elif car_name == constants.NAME_R:
                x_other_func = lambda: self.traj_h.x0 # human numpy state
            if use_truck:
                x_truck_func = lambda: self.traj_truck.x0 # truck numpy state
        elif fw == tt:
            proj = self.proj.proj_th
            if car_name == constants.NAME_H:
                x_other_func = lambda: self.traj_r.x0_th # robot Theano state
            elif car_name == constants.NAME_R:
                x_other_func = lambda: self.traj_h.x0_th # human Theano state
            if use_truck:
                x_truck_func = lambda: self.traj_truck.x0_th # truck Theano state
        return make_f(x_other_func, proj, car_name, use_truck=use_truck, 
                x_truck_func=x_truck_func)
