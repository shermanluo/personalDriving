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
# Script to run an obstacle avoidance example for the TwoPlayerUnicycle4D.
#
################################################################################

import os
import numpy as np
import matplotlib.pyplot as plt

from CarSystem import TwoPlayerCarSystem
from ilq_solver import ILQSolver
from point import Point
from proximity_cost import ProximityCost
from obstacle_cost import ObstacleCost
from semiquadratic_cost import SemiquadraticCost
from quadratic_cost import QuadraticCost
from player_cost import PlayerCost
from box_constraint import BoxConstraint
from visualizer import Visualizer
from logger import Logger
import sys
import signal
from CarSystemControlCost import CarSystemControlCost
from CarSystemStateCost import CarSystemStateCost
from product_multiplayer_dynamical_system import \
    ProductMultiPlayerDynamicalSystem
import pdb

def run(x0, currentStates, currentControls, carDynamics, r_r, r_h):
    # General parameters.
    TIME_HORIZON = 2.0   # s
    TIME_RESOLUTION = 0.1 # s
    HORIZON_STEPS = int(TIME_HORIZON / TIME_RESOLUTION)
    LOG_DIRECTORY = "./logs/world_highway/"

    # Create dynamics.
    dynamics = TwoPlayerCarSystem(carDynamics, T=TIME_RESOLUTION)
    # Choose an initial state and control laws.
    x0 = np.array(
               [[0.0],
                [0.0],
                [0.0],
                [0.0],
                [0.0],
                [0.0],
                [0.0],
                [0.0]])
    mult = 0.0
    P1s = [mult * np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])] * HORIZON_STEPS
    P2s = [np.zeros((dynamics._u_dims[1], dynamics._x_dim))] * HORIZON_STEPS
    alpha1s = [np.zeros((dynamics._u_dims[0], 1))] * HORIZON_STEPS
    alpha2s = [np.zeros((dynamics._u_dims[1], 1))] * HORIZON_STEPS


    stateCost_r = CarSystemStateCost(r_r)
    stateCost_h = CarSystemStateCost(r_h)
    controlCost_r = CarSystemControlCost(r_r)
    controlCost_h = CarSystemControlCost(r_h)


    player1_cost = PlayerCost()
    player1_cost.add_cost(stateCost_r, "x", 1)
    player1_cost.add_cost(controlCost_r, 0, 1)

    player2_cost = PlayerCost()
    player2_cost.add_cost(stateCost_h, "x", 1)
    player2_cost.add_cost(controlCost_h, 1, 1)

    # Visualizer.

    # Logger.
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)

    path_to_logfile = os.path.join(LOG_DIRECTORY, "CarExample.pkl")
    if len(sys.argv) > 1:
        path_to_logfile = os.path.join(LOG_DIRECTORY, sys.argv[1])

    print("Saving log file to {}...".format(path_to_logfile))
    logger = Logger(path_to_logfile)

    # Set up ILQSolver.
    solver = ILQSolver(dynamics,
                       [player1_cost, player2_cost],
                       x0,
                       [P1s, P2s],
                       [alpha1s, alpha2s],
                       0.01,
                       None,
                       logger,
                       None)

    def handle_sigint(sig, frame):
        print("SIGINT caught! Saving log data...")
        logger.dump()
        print("...done, exiting!")
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigint)
    import pdb
    #pdb.set_trace()
    solver.run()
