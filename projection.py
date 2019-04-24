import numpy as np
import theano.tensor as tt

import utils

class Projection(object):
    """Defines the projection function and provides utility projection functions
    with the numpy and Theano frameworks."""
    def __init__(self, proj):
        """
        Arguments:
        - proj: projection function that projects the given robot and human 
            tactical states to the strategic state and returns it as a list.
        """
        self.proj = proj

    def proj_np(self, *args):
        return np.array(self.proj(*args))

    def proj_th(self, *args):
        return tt.stacklists(self.proj(*args))

class ProjectionStrategicValue3D(Projection):
    """Default 3D strategic value projection."""
    def __init__(self):
        Projection.__init__(self, utils.tact_to_strat_proj_3d)

class ProjectionStrategicValue4D(Projection):
    """Default 4D strategic value projection."""
    def __init__(self):
        Projection.__init__(self, utils.tact_to_strat_proj_4d)

class ProjectionTruckCutInStrategicValue5D(Projection):
    """Default strategic value projection for 5D truck cut-in scenario."""
    def __init__(self):
        Projection.__init__(self, utils.tact_to_strat_proj_truck_cut_in_5d)

class ProjectionTruckCutInStrategicValue6D(Projection):
    """Default strategic value projection for 6D truck cut-in scenario."""
    def __init__(self):
        Projection.__init__(self, utils.tact_to_strat_proj_truck_cut_in_6d)