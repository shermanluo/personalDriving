import pdb
import pickle
import sys

import matplotlib.pyplot as plt
import numpy as np

import config
import constants


def load_data(filename):
    with open(filename) as infile:
        return pickle.load(infile)

### Data access functions
def get_ith_sample_elem(data, i):
    return np.array([[s[i] for s in car_hist] for car_hist in data])

def get_time(data):
    return get_ith_sample_elem(data, 0)

def get_state(data):
    return get_ith_sample_elem(data, 1)

def get_plan(data):
    return get_ith_sample_elem(data, 2)

def get_tactical_reward(data):
    return get_ith_sample_elem(data, 3)

def get_strategic_value(data):
    return get_ith_sample_elem(data, 4)

### Plotting functions
def plot(x, y, xlabel, ylabel, label, color=None, new_fig=True, 
        show=True, aspect='auto'):
    """General plotting function for a single plot on one figure."""
    if new_fig:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_aspect(aspect)
    if color is not None:
        plt.plot(x, y, label=label, color=color)
    else:
        plt.plot(x, y, label=label)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    if show:
        plt.show()

def plots(x_list, y_list, xlabel, ylabel, labels, show=True):
    """Plot multiple plots on the same figure."""
    for i, (x, y, label) in enumerate(zip(x_list, y_list, labels)):
        plot(x, y, xlabel, ylabel, label, new_fig=(i==0), show=False)
    if show:
        plt.show()


# Plot states
def plot_time_vs_state_ith_elem(data, i, ylabel, car_names=['robot', 'human']):
    """Plot time vs. ith element of the state."""
    time = get_time(data)
    states = get_state(data)
    state_i = states[:, :, i] # ith element of the state
    plots(time, state_i, 'time (sec)', ylabel, car_names)

def plot_time_vs_x(data, car_names=['robot', 'human']):
    plot_time_vs_state_ith_elem(data, 0, 'x', car_names)

def plot_time_vs_y(data, car_names=['robot', 'human']):
    plot_time_vs_state_ith_elem(data, 1, 'y', car_names)

def plot_time_vs_angle(data, car_names=['robot', 'human']):
    plot_time_vs_state_ith_elem(data, 2, 'angle', car_names)

def plot_time_vs_velocity(data, car_names=['robot', 'human']):
    plot_time_vs_state_ith_elem(data, 3, 'velocity', car_names)

def plot_x_y(data, car_names=['robot', 'human']):
    """Plot x position vs. y position of the cars."""
    states = get_state(data)
    x = states[:, :, 0] # x position
    y = states[:, :, 1] # y position
    plots(x, y, 'x', 'y', car_names)

def plot_time_vs_state_ith_elem_rel(data, i, ylabel, car_names):
    time = get_time(data)
    states = get_state(data)
    state_i = states[:, :, i] # ith element of the state
    for j in range(1, len(state_i)):
        state_i[j] -= state_i[0] # compute relative state (to 0th state)
    rel_state_i = state_i[1:, ]
    plots(time, rel_state_i, 'time (sec)', ylabel, car_names)

def plot_time_vs_x_rel(data, car_names=['robot', 'human']):
    rel_labels = (['{0} x - {1} x'.format(car_names[i], car_names[0]) 
            for i in range(1, len(car_names))])
    plot_time_vs_state_ith_elem_rel(data, 0, 'relative x', rel_labels)

def plot_time_vs_y_rel(data, car_names=['robot', 'human']):
    rel_labels = (['{0} y - {1} y'.format(car_names[i], car_names[0]) 
            for i in range(1, len(car_names))])
    plot_time_vs_state_ith_elem_rel(data, 1, 'relative y', rel_labels)

def plot_time_vs_angle_rel(data, car_names=['robot', 'human']):
    rel_labels = (['{0} angle - {1} angle'.format(car_names[i], car_names[0]) 
            for i in range(1, len(car_names))])
    plot_time_vs_state_ith_elem_rel(data, 2, 'relative angle', rel_labels)

def plot_time_vs_velocity_rel(data, car_names=['robot', 'human']):
    rel_labels = (['{0} velocity - {1} velocity'.format(car_names[i], car_names[0]) 
            for i in range(1, len(car_names))])
    plot_time_vs_state_ith_elem_rel(data, 3, 'relative velocity', rel_labels)


# Plot rewards
def plot_tactical_reward(data, car_names=['robot', 'human']):
    time = get_time(data)
    tact_r = get_tactical_reward(data)
    plots(time, tact_r, 'time (sec)', 'tactical reward', car_names)

def plot_cum_tactical_reward(data, car_names=['robot', 'human']):
    time = get_time(data)
    tact_r = get_tactical_reward(data)
    cum_reward = np.array([np.cumsum(r) for r in tact_r])
    plots(time, cum_reward, 'time (sec)', 'cumulative tactical reward', 
        car_names)

def plot_strategic_value(data, car_name='robot'):
    time = get_time(data)[0]
    strat_val = get_strategic_value([data[0]])[0]
    plot(time, strat_val, 'time (sec)', 'strategic value', car_name)

def plot_hierarchical_reward(data, car_name='robot'):
    time = get_time(data)[0]
    tact_r = get_tactical_reward([data[0]])[0]
    strat_val = get_strategic_value([data[0]])[0]
    hierarch_r = tact_r + config.STRATEGIC_VALUE_SCALE * strat_val
    plot(time, hierarch_r, 'time (sec)', 'hierarchical reward', car_name)

def plot_all_robot_rewards(data):
    time = get_time(data)[0]
    tact_r = get_tactical_reward([data[0]])[0]
    strat_val = get_strategic_value([data[0]])[0]
    hierarch_r = tact_r + config.STRATEGIC_VALUE_SCALE * strat_val
    x_list = [time, time, time]
    y_list = [tact_r, strat_val, hierarch_r]
    labels = ['robot tactical reward', 'robot strategic value', 
        'robot hierarchical reward']
    plots(x_list, y_list, 'time (sec)', 'tactical reward', labels)
    

if __name__ == '__main__':
    filename = sys.argv[1]
    func = sys.argv[2]
    data = load_data(filename)
    globals()[func](data)
