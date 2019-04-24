class TimeProfile(object):
	# Time profile for a function, chunk of code, etc.
	def __init__(self, name, description=None):
		self.name = name
		self.description = description
		self.history = [] # list of (start_time, end_time) tuples
		self.mean = 0.0 # mean duration

	def __str__(self):
		return '{0}: mean={1}, # iters={2}'.format(self.name, self.mean,
			self.num_iters)

	@property
	def num_iters(self):
		# number of iterations of code
		return len(self.history)

	def update(self, start_time, end_time):
		# Update the time profile with the observation of start_time and end_time.
		self.mean = ((self.mean * self.num_iters + end_time - start_time) / 
					(self.num_iters + 1))
		self.history.append((start_time, end_time))

time_profiles = {}

def time_profiles_to_dict():
	return {name: tp.history for name, tp in time_profiles.items()}

maximizer_time_profile = TimeProfile('maximizer')
time_profiles['maximizer'] = maximizer_time_profile

control_loop_time_profile = TimeProfile('control_loop')
time_profiles['control_loop'] = control_loop_time_profile

outer_loop_time_profile = TimeProfile('outer_loop')
time_profiles['outer_loop'] = outer_loop_time_profile

inner_loop_time_profile = TimeProfile('inner_loop')
time_profiles['inner_loop'] = inner_loop_time_profile

maximize_inner_time_profile = TimeProfile('maximize_inner')
time_profiles['maximize_inner'] = maximize_inner_time_profile

func2_time_profile = TimeProfile('func2')
time_profiles['func2'] = func2_time_profile

car_control_new_plan_time_profile = TimeProfile('car_control_new_plan',
	'Time between when ith and (i+1)th plans become available to car.control.')
time_profiles['car_control_new_plan'] = car_control_new_plan_time_profile

value_function_time_profile = TimeProfile('value_function')
time_profiles['value_function'] = value_function_time_profile

update_corners_time_profile = TimeProfile('update_corners')
time_profiles['update_corners'] = update_corners_time_profile

simulator_time_profile = TimeProfile('simulator')
time_profiles['simulator'] = simulator_time_profile

asynchronous_planner_time_profile = TimeProfile('asynchronous_planner')
time_profiles['asynchronous_planner'] = asynchronous_planner_time_profile

asynchronous_controller_time_profile = TimeProfile('asynchronous_controller')
time_profiles['asynchronous_controller'] = asynchronous_controller_time_profile

animation_loop_time_profile = TimeProfile('animation_loop')
time_profiles['animation_loop'] = animation_loop_time_profile

# predicted duration of inner loop plus func2 of NestedMaximizer/HierarchicalMaximizer
# used in in opt_timeup.py to determine if there's time for another inner loop
predicted_inner_loop_func2_duration = 0.0



# hierarchical_maximizer_avg_duration = 0.0
# num_hierarchical_maximizer_loops = 0
# logfile = 'scrap/logs/asynchronous_test.json'
# num_planner_iters = 0 # number of iterations of control loop
# planner_iter_time_cma = 0.0 # cumulative running average (CMA) of time per planner iteration
# planner_iter_time_cma_history = []
# control_loop_times = []
# outer_loop_times = []
# inner_loop_times = []
# maximize_inner_times = []
# func2_times = []
# control_loop_durations = []
# outer_loop_durations = []
# inner_loop_durations = []
# maximize_inner_durations = []
# func2_durations = []
# value_function_times = []
# value_function_durations = []
# update_corners_times = []
# update_corners_durations = []
# simulator_times = []
# asynchronous_planner_times = []
# asynchronous_controller_times = []
# animation_loop_times = []