import pdb
import thread
import threading

class Planner(object):
	# Generates plans for the car.
	def __init__(self, traj, optimizer, bounds, other_bounds=None, name=None):
		"""
		traj: trajectory of the car
		optimizer: optimizer to use for generating the plan
		bounds: control bounds for this car
		other_bounds: control bounds for the other vehicle
		"""
		self.traj = traj
		self.optimizer = optimizer
		self.bounds = bounds
		self.other_bounds = other_bounds
		self.name = name

	def plan(self):
		# Generate a new plan and set it in the trajectory.
		if self.other_bounds is None:
			plan = self.optimizer.maximize(bounds=self.bounds) # 1-D
		else:
			plan = self.optimizer.maximize(
					bounds=self.bounds, other_bounds=self.other_bounds) # 1-D
		# Update optimal control in trajectory
		self.traj.u = plan # numpy plan
		self.traj.u_th = plan # Theano plan
		return self.traj.u # return plan in shape of self.traj.u

class TwoCarPlanner(object):
	# Generates plans for the car using nested optimization.
	def __init__(self, traj_r, traj_h, human, optimizer, bounds, name=None):
		# traj_r: trajectory of the robot car
		# traj_h: trajectory of the human car
		# human: the human car
		# optimizer: optimizer to use for generating the plan
		# bounds: car control bounds
		self.traj_r = traj_r
		self.traj_h = traj_h
		self.human = human
		self.optimizer = optimizer
		self.bounds = bounds
		self.name = name

	def plan(self):
		"""Generate new plans for robot and human, set them in the 
								corresponding trajectories, and return the robot plan."""
		opt_r, opt_h = self.optimizer.maximize(bounds=self.bounds) # 1-D
		plan_r, plan_h = opt_r, opt_h
		# Update optimal control in trajectories
		self.traj_r.u = plan_r # numpy robot plan
		self.traj_r.u_th = plan_r # Theano robot plan
		self.traj_h.u = plan_h # numpy human plan
		self.traj_h.u_th = plan_h # Theano human plan
		return self.traj_r.u # return plan in shape of self.traj.u

class FixedControlPlanner(object):
	"""Applies the same fixed control at each timestep."""
	def __init__(self, traj, fixed_control):
		self.traj = traj
		self.fixed_control = fixed_control
		self.fixed_plan = [self.fixed_control for i in range(self.traj.horizon)]

	def plan(self):
		self.traj.u = self.fixed_plan # numpy plan
		self.traj.u_th = self.fixed_plan # Theano plan
		return self.fixed_plan # return plan in shape of self.traj.u
