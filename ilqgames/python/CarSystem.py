"""
BSD 3-Clause License

Copyright (c) 2019, HJ Reachability Group
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Author(s): David Fridovich-Keil ( dfk@eecs.berkeley.edu )
"""
################################################################################
#
# 4D unicycle model with disturbance. Dynamics are as follows:
#                          \dot x     = v cos theta + u21
#                          \dot y     = v sin theta + u22
#                          \dot theta = u11
#                          \dot v     = u12
#
################################################################################

import torch
import numpy as np
import constants

from multiplayer_dynamical_system import MultiPlayerDynamicalSystem

class TwoPlayerCarSystem(MultiPlayerDynamicalSystem):
    """ 4D unicycle model with disturbances.

    dynamics is the dynamics object passed in from the CarSimulation codebase"""

    #dynamics
    def __init__(self, dynamics, T=0.1):
        super(TwoPlayerCarSystem, self).__init__(8, [2, 2], T)

    def __call__(self, x, u,
                 friction=constants.FRICTION,
                 wheelbase=constants.WHEELBASE * constants.METERS_TO_VIS):
        """
        Compute the time derivative of state for a particular state/control.
        NOTE: `x`, and all `u` should be 2D (i.e. column vectors).

        :param x: current state
        :type x: torch.Tensor or np.array
        :param u: list of current control inputs for all each player
        :type u: [torch.Tensor] or [np.array]
        :return: current time derivative of state
        :rtype: torch.Tensor or np.array
        """
        assert len(u) == self._num_players

        if isinstance(x, np.ndarray):
            x_dot = np.zeros((self._x_dim, 1))
            cos = np.cos
            sin = np.sin
            tan = np.tan
        else:
            x_dot = torch.zeros((self._x_dim, 1))
            cos = torch.cos
            sin = torch.sin
            tan = torch.tan
        #print(np.array(x_dot).shape, np.array(u).shape)
        x_dot[0, 0] = x[3, 0] * cos(x[2, 0])                       #x[3, 0] * cos(x[2, 0]) + u[1][0, 0]
        x_dot[1, 0] = x[3, 0] * sin(x[2, 0])                       #x[3, 0] * sin(x[2, 0]) + u[1][1, 0]
        x_dot[2, 0] = x[3, 0] * tan(u[0][0, 0]) / wheelbase        #u[0][0, 0]
        x_dot[3, 0] = u[0][1, 0] - friction * x[3, 0] ** 2         #u[0][1, 0]

        x_dot[4, 0] = x[7, 0] * cos(x[6, 0])  # x[3, 0] * cos(x[2, 0]) + u[1][0, 0]
        x_dot[5, 0] = x[7, 0] * sin(x[6, 0])  # x[3, 0] * sin(x[2, 0]) + u[1][1, 0]
        x_dot[6, 0] = x[7, 0] * tan(u[1][0, 0]) / wheelbase  # u[0][0, 0]
        x_dot[7, 0] = u[1][1, 0] - friction * x[7, 0] ** 2  # u[0][1, 0]
        return x_dot
