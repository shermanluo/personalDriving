import copy
import json
import os
import pdb
import pickle
import random
import sys
import threading

import pyglet
from pyglet.window import key
import pyglet.gl as gl
import pyglet.graphics as graphics
import numpy as np
import theano as th
import theano.tensor as tt
import matplotlib.cm
import text_input
import time

import config
import constants
from car import Car
import feature
import time_profile
import topic_program
import utils



class Visualizer(threading.Thread): # inherits from thread to properly access shared variable of the external simulation state
    def __init__(self, world, dt=constants.DT, fullscreen=False, manual=False,
            name='unnamed', iters=float('inf'), magnify=1., 
            save_interaction_data=False, save_interaction_data_dir=None, 
            save_frames=False, frame_dir=None,
            heatmap_show=False, heatmap_name=None, plan_show=False,
            heat_val_show=False):
        """
        Arguments:
        - save_interaction_data: if True, save the interaction data
        - save_interaction_data_dir: directory inside of the interaction
            data directory to which to save the interaction data.
        - save_frames: If True, save the frames of the interaction in save_interaction_data_dir.
        - heat_val_show: if True, display the value of the heat at the current
            mouse location.
        """
        threading.Thread.__init__(self)
        self.world = world
        self.dt = dt
        self.manual = manual
        self.name = name
        self.iters = iters
        self.magnify = magnify
        self.autoquit = True
        self.frame = None
        self.subframes = None
        self.camera_center = None
        # if (save_interaction_data_filename is not None and 
        #         save_interaction_data_filename[-7:] != '.pickle'):
        #     save_interaction_data_filename += '.pickle'
        if save_interaction_data_dir is not None:
            if save_interaction_data_dir[-1] != '/':
                save_interaction_data_dir += '/'
        else:
            save_interaction_data_dir = '{0}{1}-{2}/'.format(
                    constants.INTERACTION_DATA_DIR, self.name, int(time.time()))
        self.save_interaction_data_dir = save_interaction_data_dir
        # filename to save the save the interaction data to (set during saving process)
        self.save_interaction_data_filename = None
        # TODO: remove commented out code
        # if frame_dir is not None:
        #     if frame_dir[-1] != '/':
        #         frame_dir += '/'
        #     if not os.path.exists(frame_dir):
        #         os.makedirs(frame_dir)
        # self.frame_dir = frame_dir
        self.save_frames = save_frames
        # Directory to which to save frames
        if frame_dir is not None:
            if frame_dir[-1] != '/':
                frame_dir += '/'
        else:
            frame_dir = self.save_interaction_data_dir + 'frames/'
        self.frame_dir = frame_dir 
        if self.save_frames and not os.path.exists(self.frame_dir):
            os.makedirs(self.frame_dir)
        self.world.objects = []
        
        # Pyglet
        self.event_loop = pyglet.app.EventLoop()
        self.window = pyglet.window.Window(600, 600, fullscreen=fullscreen, caption=name)
        self.grass = pyglet.resource.texture(constants.IMAGE_DIR + 'grass.png')
        self.window.on_draw = self.on_draw
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.window.on_key_press = self.on_key_press
        self.window.on_key_release = self.on_key_release
        self.window.on_mouse_motion = self.on_mouse_motion
        self.joystick = None
        if self.manual:
            self.manual_window = text_input.Window()

        self.anim_x = {}
        self.prev_x = {}
        self.feed_u = None
        self.feed_x = None
        self.prev_t = None
        self.main_car = None
        self.plan_show = plan_show
        # gist_rainbow works well with 0.75 multiplier
        self.cm = matplotlib.cm.gist_rainbow # jet, nipy_spectral, gist_rainbow
        self.logging = False
        # reward heatmap
        self.heat = None
        self.heatmap = None
        self.heatmap_show = heatmap_show
        self.heatmap_name = heatmap_name
        self.heatmap_valid = False # if True, current heatmap is valid and shouldn't be recomputed
        self.min_heatmap_val = None
        self.max_heatmap_val = None
        self.heatmap_min_max_coords = None # (min, max) coordinates (x, y) for reward heatmap
        # if True, heatmap scale is fixed and not rescaled according to the 
        # specific values of the current heatmap
        self.fixed_heatmap_scale = False
        self.heat_val_show = heat_val_show

        # User controls
        self.steer_user = 0.0
        self.gas_user = 0.0
        self.brake_user = 0.0

        # Text labels
        self.label_speed_r = pyglet.text.Label(
            '',
            font_name='Times New Roman',
            font_size=24,
            x=30, y=self.window.height-20,
            anchor_x='left', anchor_y='top',
        )
        self.label_speed_h = pyglet.text.Label(
            '',
            font_name='Times New Roman',
            font_size=24,
            x=30, y=self.window.height-530,
            anchor_x='left', anchor_y='top'
        )
        self.label_heat = pyglet.text.Label(
            '',
            font_name='Times New Roman',
            font_size=16,
            x=30, y=self.window.height/2,
            anchor_x='left', anchor_y='top'
        )

        # Object and car images/sprites
        def centered_image(filename):
            img = pyglet.resource.image(filename)
            img.anchor_x = img.width/2.
            img.anchor_y = img.height/2.
            return img
        def car_sprite(color, scale=0.15/600.):
            sprite = pyglet.sprite.Sprite(centered_image(constants.IMAGE_DIR + 
                'car-{}.png'.format(color)), subpixel=True)
            sprite.scale = scale
            return sprite
        def object_sprite(name, scale=0.15/600.):
            sprite = pyglet.sprite.Sprite(centered_image(constants.IMAGE_DIR + 
                '{}.png'.format(name)), subpixel=True)
            sprite.scale = scale
            return sprite
        self.sprites = {c: car_sprite(c) for c in 
            ['red', 'yellow', 'purple', 'white', 'orange', 'gray', 'cyan', 'blue', 'truck']}
        #self.obj_sprites = {c: object_sprite(c) for c in ['cone', 'firetruck','arrow']}
        self.obj_sprites = {c: object_sprite(c) for c in 
            ['cone', 'firetruck','arrow1','arrow2','arrow3','arrow4','arrow5',
            'rarrow1','rarrow2','rarrow3','rarrow4','rarrow5']}
    
    ################################################################################################
    # Event handling
    ################################################################################################

    def on_mouse_motion(self, x, y, dx, dy):
        center_x, center_y = self.center() # center of visualization
        # scale = 0.15/600.
        scale = (0.13 / 2) / 20 # TODO: this is an approximation, find the exact scaling
        vis_x = (x-self.window.width/2) * scale
        vis_y = (y-self.window.height/2) * scale
        if self.heat is not None:
            self.label_heat.text = 'heat: {0}'.format(
                self.heat(np.array([center_x + vis_x, center_y + vis_y])))

    def on_key_release(self, symbol, modifiers):
        """Handle key release events."""
        if not self.keys[key.UP] and not self.keys[key.DOWN]:
            self.gas_user = 0.0
        if not self.keys[key.LEFT] and not self.keys[key.RIGHT]:
            self.steer_user = 0.0

    def heatmap_r_tact(self):
        """Set heatmap to robot's tactical value."""
        robot_car = self.world.main_robot_car
        self.set_heat(robot_car.reward.reward_np, fw=np, car=robot_car)
        # No min/max coordinates because tactical reward is defined everywhere
        self.heatmap_min_max_coords = None
        # No min/max strategic value because it's not applicable
        self.min_heatmap_val, self.max_heatmap_val = None, None

    def heatmap_h_tact(self):
        """Set heatmap to human's tactical value."""
        human_car = self.world.main_human_car
        self.set_heat(human_car.reward.reward_np, fw=np, car=human_car)
        # No min/max coordinates because tactical reward is defined everywhere
        self.heatmap_min_max_coords = None
        # No min/max strategic value because it's not applicable
        self.min_heatmap_val, self.max_heatmap_val = None, None

    def heatmap_r_strat(self):
        """Set heatmap to robot's strategic value."""
        robot_car = self.world.main_robot_car
        self.set_heat(robot_car.strat_val.value_r_np, fw=np, 
            car=robot_car)
        # Compute min and max coordinates of the bounding box for
        # the robot's strategic value.
        x_truck_func = None
        if hasattr(robot_car, 'truck'):
            x_truck_func = lambda: robot_car.truck.traj.x0
        self.heatmap_min_max_coords = (lambda: 
            utils.strategic_reward_heatmap_coord(
                robot_car.strat_val.min_state, 
                robot_car.strat_val.max_state,
                strat_dim=config.STRAT_DIM, 
                x_h=robot_car.human.traj.x0,
                x_truck_func=x_truck_func,
                project_onto_grid=config.PROJECT_ONTO_STRAT_GRID))
        # Set min/max strategic values
        self.min_heatmap_val = config.MIN_STRAT_VAL
        self.max_heatmap_val = config.MAX_STRAT_VAL

    def heatmap_h_strat(self):
        """Set heatmap to human's strategic value."""
        human_car = self.world.main_human_car
        robot_car = self.world.main_robot_car
        self.set_heat(human_car.strat_val.value_h_np, fw=np, 
            car=human_car)
        # Compute min and max coordinates of the bounding box for
        # the human's strategic value.
        x_truck_func = None
        if hasattr(human_car, 'truck'):
            x_truck_func = lambda: human_car.truck.traj.x0
        self.heatmap_min_max_coords = (lambda: 
            utils.strategic_reward_heatmap_coord(
                human_car.strat_val.min_state, 
                human_car.strat_val.max_state, 
                strat_dim=config.STRAT_DIM,
                x_r=robot_car.traj.x0,
                x_truck_func=x_truck_func,
                project_onto_grid=config.PROJECT_ONTO_STRAT_GRID))
        # Set min/max strategic values
        self.min_heatmap_val = config.MIN_STRAT_VAL
        self.max_heatmap_val = config.MAX_STRAT_VAL

    def on_key_press(self, symbol, modifiers):
        """Handle key press events."""
        # User controls
        if self.keys[key.UP] and not self.keys[key.DOWN]:
            self.gas_user = constants.CAR_CONTROL_BOUNDS[1][1]
        if self.keys[key.DOWN] and not self.keys[key.UP]:
            self.gas_user = constants.CAR_CONTROL_BOUNDS[1][0]
        if self.keys[key.LEFT] and not self.keys[key.RIGHT]:
            self.steer_user = constants.CAR_CONTROL_BOUNDS[0][1]
        if self.keys[key.RIGHT] and not self.keys[key.LEFT]:
            self.steer_user = constants.CAR_CONTROL_BOUNDS[0][0]
        if symbol == key.ESCAPE: # quit
            if self.save_interaction_data:
                self.save_interaction_data() # save interaction data before quitting
            self.event_loop.exit()
        if symbol == key.P: # take screenshot
            pyglet.image.get_buffer_manager().get_color_buffer().save(
                constants.SCREENSHOT_DIR + self.name + '-%.2f.png'%time.time())
        if symbol == key.SPACE: # pause/unpase
            topic_program.paused = not topic_program.paused
        # show/hide reward heatmap
        if (symbol == key.H or symbol == key.J or
                symbol == key.B or symbol == key.N):
            topic_program.paused = True # pause movement
            self.heatmap_valid = False # current heatmap (if any) is now invalid
            robot_car = self.world.main_robot_car
            human_car = self.world.main_human_car

            if symbol == key.H: # robot tactical reward
                self.heatmap_r_tact()
                reward_name = 'robot tactical reward'
            elif symbol == key.J: # robot strategic value
                if hasattr(robot_car, 'strat_val'):
                    self.heatmap_r_strat()
                    reward_name = '{0} * robot strategic value'.format(
                        robot_car.strat_val.scale)
                else:
                    print '{0} does not have a strategic value'.format(
                        robot_car.name)
                    return
            elif human_car is None:
                # User wants to display human reward but the human car is either 
                # ambiguous or undefined
                return 
            elif symbol == key.B: # human tactical reward
                self.heatmap_h_tact()
                reward_name = 'human tactical reward'
            elif symbol == key.N: # human strategic value
                if hasattr(human_car, 'strat_val'):
                    self.heatmap_h_strat()
                    reward_name = '{0} * human strategic value'.format(
                        human_car.strat_val.scale)
                else:
                    print '{0} does not have a strategic value'.format(
                        human_car.name)
                    return
            if self.heatmap_show:
                print 'hiding heatmap'
            else:
                print 'showing heatmap of ' + reward_name
            self.heatmap_show = not self.heatmap_show
        if symbol == key.K:
            # change whether reward heatmap is according to a fixed or dynamic scale
            self.fixed_heatmap_scale = not self.fixed_heatmap_scale
            self.heatmap_valid = False
        if symbol == key.L: # time profile logging
            filename = '{0}/{1}-{2}.json'.format(
                    constants.TIME_PROFILE_DIR, self.name, int(time.time()))
            print 'Saving time profile data to {0}'.format(filename)
            log = time_profile.time_profiles_to_dict()
            with open(filename, 'w') as f:
                json.dump(log, f)
        if symbol == key.S: # save interaction data
            topic_program.paused = True
            self.save_interaction_data()
        if symbol == key.V:
            if self.world.user_controlled_car is not None:
                x0 = self.world.user_controlled_car.traj.x0
                new_x0 = [x0[0], x0[1], np.pi / 2.0, x0[3]]
                self.world.user_controlled_car.traj.x0 = new_x0
                self.world.user_controlled_car.traj.x0_th = new_x0
        if symbol == key.R: # reset cars to initial positions
            self.reset()
        if symbol == key.X: # show/unshow predicted initial states
            print 'show/unshow predicted initial states'
            self.x0_pred_show = not self.x0_pred_show
        if symbol == key.Z: # show/unshow car plan
            print 'show/unshow plan'
            self.plan_show = not self.plan_show

    def on_draw(self):
        self.window.clear()
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        self.camera()
        gl.glEnable(self.grass.target)
        gl.glEnable(gl.GL_BLEND)
        gl.glBindTexture(self.grass.target, self.grass.id)
        W = 10000.
        graphics.draw(4, gl.GL_QUADS,
            ('v2f', (-W, -W, W, -W, W, W, -W, W)),
            ('t2f', (0., 0., W*5., 0., W*5., W*5., 0., W*5.))
        )
        gl.glDisable(self.grass.target)
        for lane in self.world.lanes:
            self.draw_lane_surface(lane)
        for lane in self.world.lanes:
            self.draw_lane_lines(lane)
        for obj in self.world.objects:
            self.draw_object(obj)
        for note in self.world.notices: # Elis: added.
            self.draw_notice(note)
        if self.heat is not None:
            self.draw_heatmap()
        for car in self.world.cars:
            # this draws the car at its current actual position (according to
            # the control loop) and doesn't take its animation position (in
            # self.anim_x[car]) into account.
            self.draw_car(car.traj.x0, car.color)
            # self.draw_car(self.anim_x[car], car.color)
        self.draw_car_plans() # display plans generated by the main robot car
        gl.glPopMatrix()
        self.draw_labels()
        # Save current frame
        if self.save_frames and not topic_program.paused:
            pyglet.image.get_buffer_manager().get_color_buffer().save(
                '{0}{1}.png'.format(
                    self.frame_dir, 
                    int(self.world.simulator.time / self.world.simulator.dt)))

    ################################################################################################
    # Camera/visualization orientation
    ################################################################################################

    def center(self):
        """Return the center of the visualization."""
        try:
            if self.main_car is None:
                return np.asarray([0., 0.])
            elif self.camera_center is not None: # (x, y) coordinates of camera center
                return np.asarray(self.camera_center[0:2])
            else: # (x, y) coordinates of main car's position
                # return [0., self.anim_x[self.main_car][1]]
                return [0., self.main_car.traj.x0[1]] # using car's actual position
        except Exception as e:
            print e
            pdb.set_trace()
    
    def center_road(self):
        """Return the x coordinates of the center of the road."""
        left_x = constants.LEFT_LANE_CENTER - constants.LANE_WIDTH_VIS / 2.0
        right_x = left_x + len(self.world.lanes) * constants.LANE_WIDTH_VIS
        return (left_x + right_x) / 2.0

    def camera(self):
        o = self.center()
        a1 = o[0]-1./self.magnify
        a2 = o[0]+1./self.magnify
        a3 = o[1]-1./self.magnify
        a4 = o[1]+1./self.magnify
        gl.glOrtho(a1, a2, a3, a4, -1., 1.)
    

    def set_heat(self, reward, fw, car=None):
        # reward: the reward function
        # car: the car corresponding to the reward function. Used to get its 
        # current heading and velocity. If car is None, visualize the reward for
        # 0 heading and 0 velocity.
        assert(fw == np or fw == tt)
        if fw == np:
            if car is not None:
                def val(state):
                    x_car, y_car, heading_car, vel_car = car.traj.x0
                    # maintain same heading and velocity in a different x, y location
                    x = np.array([state[0], state[1], heading_car, vel_car])
                    # maintain same control
                    u = car.traj.u[0]
                    return reward(0, x, u) # (t, x, u)
            else:
                def val(state):
                    x = np.array([state[0], state[1], 0., 0.])
                    u = np.zeros(constants.CONTROL_DIM)
                    return reward(0, x, u) # (t, x, u)
        elif fw == tt:
            x = utils.th_vector(constants.STATE_DIM)
            u = utils.th_vector(constants.CONTROL_DIM)
            reward_func = th.function([], reward(0, x, u))  # (t, x, u)
            if car is not None:
                def val(state):
                    x_car, y_car, heading_car, vel_car = car.traj.x0
                    # maintain same heading and velocity in a different x, y location
                    x.set_value(np.array([state[0], state[1], heading_car, vel_car]))
                    # maintain same control
                    u.set_value(np.array(car.traj.u[0]))
                    return reward_func()
            else:
                def val(state):
                    # maintain same heading and velocity in a different x, y location
                    x.set_value(np.array([state[0], state[1], 0.0, 0.0]))
                    return reward_func()
        self.heat = val

    ################################################################################################
    # Loops
    ################################################################################################

    def animation_loop(self, _):
        start_time = time.time()
        t = self.world.simulator.time
        alpha = min((t - self.prev_t) / self.dt, 1.) # Elis: Temporary solution for just taking the computation steps. Replace 0<--1.
        for car in self.world.cars:
            # self.anim_x[car] = ((1 - alpha) * np.array(self.prev_x[car]) + 
            #                 alpha*np.array(car.traj.x0))
            self.prev_x[car] = copy.copy(self.anim_x[car]) # set previous animation x for car
            self.anim_x[car] = np.array(car.traj.x0)
        end_time = time.time()
        time_profile.animation_loop_time_profile.update(start_time, end_time)

    def control_loop(self, _=None):
        # Pause conditions
        if constants.PAUSE_EVERY_N is not None and constants.PAUSE_EVERY_N > 0 and len(self.history_u[0])%constants.PAUSE_EVERY_N==0:
            topic_program.paused = True
        if topic_program.paused:
            return

        # Quit conditions
        if ((self.iters is not None and self.world.simulator.time / self.dt > self.iters) or # number of iterations
            # length of input controls
            (self.world.simulator.feed_u is not None and len(self.world.cars[0].history) >= len(self.world.simulator.feed_u[0])) or
            # no more interaction data available
            (self.world.simulator.interaction_data is not None and int(self.world.simulator.time / self.world.simulator.dt) >= len(self.world.simulator.interaction_data[0]))):
            print 'Quit condition met.'
            if self.autoquit:
                if self.save_interaction_data:
                    self.save_interaction_data() # save interaction data before quitting
                print 'Quitting.'
                self.event_loop.exit()
                sys.exit()
            return False

        self.heatmap_valid = False # heatmap no longer valid due to car movement

        # User controls
        if self.joystick:
            # steering sign: + (steer right) -> - (yaw clockwise)
            self.steer_user = -self.joystick.x * constants.K_STEER_USER
            self.gas_user = (1.0 - self.joystick.y) / 2.0 * constants.K_GAS_USER
            self.brake_user = (1.0 - self.joystick.rz) / 2.0 * constants.K_BRAKE_USER
        if self.world.user_controlled_car is not None:
            self.world.user_controlled_car.set_control(
                [self.steer_user, self.gas_user - self.brake_user])

        for note in self.world.notices: # show notices
            note.info = note.info_func()
        
        self.world.simulator.simulate() # get new plans for cars and apply them to move the cars

        return True
    
    def output_loop(self, _):
        if topic_program.paused:
            return
        if self.frame % self.subframes == 0:
            self.control_loop()
        alpha = float(self.frame % self.subframes) / float(self.subframes)
        for car in self.world.cars:
            self.anim_x[car] = ((1-alpha) * np.array(self.prev_x[car]) + 
                            alpha*np.array(car.traj.x0))
        self.frame += 1

    def manual_animation_loop(self, _):
        state_changed = False
        for car, widget_group in zip(self.world.cars, self.manual_window.widget_groups):
            try:
                state = np.array([float(widget.document.text) for widget in widget_group])
                car.traj.x0 = np.array([state[0] * constants.METERS_TO_VIS,
                                    state[1] * constants.METERS_TO_VIS,
                                    state[2], state[3] * constants.METERS_TO_VIS])
                if any(car.traj.x0 != self.prev_x[car]):
                    state_changed = True
                    self.heatmap_valid = False # heatmap no longer valid due to movement
                self.anim_x[car] = self.prev_x[car] = car.traj.x0
            except Exception as e:
                print e
                car.traj.x0 = self.prev_x[car]
        for car in self.world.cars:
            car.update_other_traj()
        if state_changed:
            for car in self.world.cars:
                print '{0}: {1}'.format(car.name, car.traj.x0)

    ################################################################################################
    # Drawing
    ################################################################################################

    def draw_lane_surface(self, lane):
        gl.glColor3f(0.4, 0.4, 0.4)
        W = 1000
        graphics.draw(4, gl.GL_QUAD_STRIP, ('v2f',
            np.hstack([lane.p-lane.m*W-0.5*lane.w*lane.n, lane.p-lane.m*W+0.5*lane.w*lane.n,
                       lane.q+lane.m*W-0.5*lane.w*lane.n, lane.q+lane.m*W+0.5*lane.w*lane.n])
        ))

    def draw_lane_lines(self, lane):
        gl.glColor3f(1., 1., 1.)
        W = 1000
        graphics.draw(4, gl.GL_LINES, ('v2f',
            np.hstack([lane.p-lane.m*W-0.5*lane.w*lane.n, lane.p+lane.m*W-0.5*lane.w*lane.n,
                       lane.p-lane.m*W+0.5*lane.w*lane.n, lane.p+lane.m*W+0.5*lane.w*lane.n])
        ))

    def draw_car(self, x, color='yellow', opacity=255):
        sprite = self.sprites[color]
        sprite.x, sprite.y = x[0], x[1]
        sprite.rotation = -x[2]*180./np.pi
        sprite.opacity = opacity
        sprite.draw()

    def draw_car_plans(self):
        """Display plans generated by the main robot car."""
        if self.plan_show and self.world.main_robot_car is not None:
            # draw robot car's plan
            r_car = self.world.main_robot_car
            if config.ASYNCHRONOUS:
                plan_r = r_car.remove_plan_past(r_car.plan)
                traj_r = [e[1] for e in plan_r]
                plan_pred_h = r_car.remove_plan_past(r_car.pred_h)
                traj_h_pred = [e[1] for e in humaplan_pred_hn_pred]
            else:
                traj_r = r_car.traj.x
                try:
                    traj_h_pred = r_car.traj_h.x
                except Exception as e:
                    print e
                    pdb.set_trace()
            for i, (x_r, x_h_pred) in enumerate(zip(traj_r, traj_h_pred)):
                opacity_t = 100*(len(traj_r)-i)/len(traj_r)
                self.draw_car(x_r, r_car.color, opacity=opacity_t)
                self.draw_car(x_h_pred, r_car.human.color, opacity=opacity_t)

    def draw_labels(self):
        """Populate and draw the text labels."""
        robot_car = self.world.main_robot_car
        if robot_car is not None:
            self.label_speed_r.text = ('R:%.1f km/h' % 
                (robot_car.traj.x0[3]/constants.METERS_TO_VIS*3.6))
            self.label_speed_r.draw()
        human_car = self.world.main_human_car
        if human_car is not None:
            self.label_speed_h.text = ('H:%.1f km/h' % 
                (human_car.traj.x0[3]/constants.METERS_TO_VIS*3.6))
            self.label_speed_h.draw()
        if self.heat_val_show:
            self.label_heat.draw()

    def draw_object(self, obj):
        sprite = self.obj_sprites[obj.name]
        sprite.x, sprite.y = obj.x[0], obj.x[1]
        sprite.rotation = obj.x[2] if len(obj.x)>=3 else 0.
        sprite.draw()

    def draw_heatmap(self):
        """Draw reward defined by self.heat as a heatmap."""
        if not self.heatmap_show:
            return
        if not self.heatmap_valid:
            center_x = self.center_road() # x coordinate of center of road
            center_vis = self.center() # center of visualization
            # heatmap center is (center of road, y coordinate of main car)
            center_heatmap = [center_x, center_vis[1]]
            # proportion of width and height to draw heatmap around the center
            if config.FULL_HEATMAP:
                w_h = [1.0, 1.0]
            else:
                w_h = [0.25, 1.0]
            # Min and max coordinates of the heatmap that define the largest area
            # that could be visible.
            visible_heatmap_min_coord = center_heatmap - np.asarray(w_h) / self.magnify
            visible_heatmap_max_coord = center_heatmap + np.asarray(w_h) / self.magnify
                
            # Set the min and max coordinates of the heatmap
            if self.heatmap_min_max_coords is None or self.heatmap_min_max_coords() is None:
                self.heatmap_min_coord = visible_heatmap_min_coord
                self.heatmap_max_coord = visible_heatmap_max_coord
            else:
                self.heatmap_min_coord, self.heatmap_max_coord = self.heatmap_min_max_coords()
                # Only draw the heatmap on the visible parts of the screen
                self.heatmap_min_coord = np.maximum(self.heatmap_min_coord, 
                        visible_heatmap_min_coord)
                self.heatmap_max_coord = np.minimum(self.heatmap_max_coord, 
                        visible_heatmap_max_coord)
            
            size = config.HEATMAP_SIZE
            min_coord = self.heatmap_min_coord
            max_coord = self.heatmap_max_coord

            print 'heatmap min coord: {0}'.format(min_coord)
            print 'heatmap max coord: {0}'.format(max_coord)

            vals = np.zeros(size)
            for i, x in enumerate(np.linspace(min_coord[0]+1e-6, max_coord[0]-1e-6, size[0])):
                for j, y in enumerate(np.linspace(min_coord[1]+1e-6, max_coord[1]-1e-6, size[1])):
                    # try:
                    vals[j, i] = self.heat(np.asarray([x, y]))
                    # except Exception as e:
                    #     print e
                    #     pdb.set_trace()
            # Set min and max values if showing the strategic value heatmap
            # using either fixed values or dynamic values based on the visible heatmap
            # print('self.min_heatmap_val:', self.min_heatmap_val)
            # print('self.max_heatmap_val:', self.max_heatmap_val)

            if self.min_heatmap_val is None or not self.fixed_heatmap_scale:
                min_val = np.min(vals)
            else:
                min_val = self.min_heatmap_val
            if self.max_heatmap_val is None or not self.fixed_heatmap_scale:
                max_val = np.max(vals)
            else:
                max_val = self.max_heatmap_val

            # scale and translate the values to make the heatmap most useful
            # 1 - vals to reverse the heatmap colors to make red==bad and blue==good
            vals = ((vals-min_val) / (max_val-min_val))
            vals *= 0.75
            # vals = 1 - vals
            vals = self.cm(vals)
            vals[:,:,3] = 0.7 # opacity
            vals = (vals * 255.).astype('uint8').flatten() # convert to RGBA
            vals = (gl.GLubyte * vals.size) (*vals)
            img = pyglet.image.ImageData(size[0], size[1], 'RGBA', vals, 
                pitch=size[1]*4)
            self.heatmap = img.get_texture()
            self.heatmap_valid = True
        gl.glClearColor(1., 1., 1., 1.)
        gl.glEnable(self.heatmap.target)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        # gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_SRC_ALPHA)
        gl.glBindTexture(self.heatmap.target, self.heatmap.id)
        gl.glEnable(gl.GL_BLEND)
        min_coord = self.heatmap_min_coord
        max_coord = self.heatmap_max_coord
        graphics.draw(4, gl.GL_QUADS,
            ('v2f', (min_coord[0], min_coord[1], max_coord[0], min_coord[1], 
                     max_coord[0], max_coord[1], min_coord[0], max_coord[1])),
            ('t2f', (0., 0., 1., 0., 1., 1., 0., 1.)),
            #('t2f', (0., 0., size[0], 0., size[0], size[1], 0., size[1]))
        )
        gl.glDisable(self.heatmap.target)

    def draw_notice(self, notice): # Elis: Function added to just have an arrow when car is coming.
        #if notice.condition: # then notice condition is fulfilled, so notify.
        if notice.name == 'maniac':
            if notice.info is not False and notice.info < 5 and notice.info > 0: # old: notice.info <= 5 and notice.info >= 0:
                #if notice.have_played is False:
                #    notice.beep.play()
                #    notice.have_played = True
                sprite = self.obj_sprites['arrow%d'%np.ceil(notice.info)]
                sprite.x, sprite.y = -0.13, self.center()[1]+0.85
                sprite.rotation = 0
                sprite.draw()
        elif notice.name == 'exit':
            exit_begins = notice.exit_begins
            W = notice.W
            U = notice.U
            gl.glColor3f(0.4, 0.4, 0.4)
            graphics.draw(4, gl.GL_QUAD_STRIP, ('v2f',
                np.hstack([(0.13/2,exit_begins+W), (0.13/2,exit_begins),
                           (1,exit_begins+U+W), (1,exit_begins+U)])
            ))
            gl.glColor3f(1, 1, 1)
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+W), (1,exit_begins+U+W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins), (1,exit_begins+U)])
            ))
            # dashed lines (neater way to do this?)
            gl.glColor3f(0.4, 0.4, 0.4)
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins), (0.13/2,exit_begins+W)]) # overwrite the usual white road lines.
            ))
            gl.glColor3f(1, 1, 1)
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins), (0.13/2,exit_begins+0.05*W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+0.1*W), (0.13/2,exit_begins+0.15*W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+0.2*W), (0.13/2,exit_begins+0.25*W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+0.3*W), (0.13/2,exit_begins+0.35*W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+0.4*W), (0.13/2,exit_begins+0.45*W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+0.5*W), (0.13/2,exit_begins+0.55*W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+0.6*W), (0.13/2,exit_begins+0.65*W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+0.7*W), (0.13/2,exit_begins+0.75*W)])
            ))
            graphics.draw(2, gl.GL_LINES, ('v2f',
            np.hstack([(0.13/2,exit_begins+0.8*W), (0.13/2,exit_begins+W)])
            ))
            if notice.info is not False and notice.info < 5 and notice.info > 0: # Here for exit.
                #if notice.have_played is False:
                #    notice.beep.play()
                #    notice.have_played = True
                sprite = self.obj_sprites['rarrow%d'%np.ceil(notice.info)]
                sprite.x, sprite.y = 0.13+0.13/4, self.center()[1]+0.85
                sprite.roation = 0
                sprite.draw()
        elif notice.name == 'quit':
            if notice.info == 1 or notice.info == -1: # the done.
                topic_program.paused = True
                initcond = notice.current_init_order[0]
                while True:
                    input_text = raw_input('Write your subject ID and trial number: ')
                    input_text = input_text.split()
                    if (len(input_text) == 2 and 
                            input_text[0] in notice.subject_list and 
                            input_text[1] in notice.trial_list):
                        save = True
                        if input_text[1] == notice.trial_list[-1]:
                            # last trial so take next order for next subject.
                            # rotate list of orders for next subject.
                            notice.init_orders = notice.init_orders[1:] + notice.init_orders[:1]
                            # get the first order for next subject (copies it to
                            # preserve the orginal one in case something goes wrong).
                            notice.current_init_order = copy.copy(notice.init_orders[0])
                        else:
                            # rotate the current order for next trial.
                            notice.current_init_order = (notice.current_init_order[1:]
                                + notice.current_init_order[:1])
                        break
                    elif len(input_text) == 1 and input_text[0] == 'dismiss':
                        # completely ignore this trial and continue.
                        save = False
                        break
                    elif len(input_text) == 1 and input_text[0] == 'skip':
                        # jump to next order without saving.
                        save = False
                        notice.init_orders = notice.init_orders[1:] + notice.init_orders[:1]
                        notice.current_init_order = copy.copy(notice.init_orders[0])
                        break
                    elif len(input_text) == 1 and input_text[0] == 'reset':
                        # reset to same original order (in case something went wrong).
                        save = False
                        notice.current_init_order = copy.copy(notice.init_orders[0])
                        break
                    elif len(input_text) == 1 and input_text[0] == 'RESET':
                        # Reset the total list of orders and make current order the first.
                        save = False
                        notice.init_orders = copy.copy(notice.original_init_order)
                        notice.current_init_order = copy.copy(notice.init_orders[0])
                        break
                    else:
                        print('Wrong input format.')
                        print('Example of correct input formats:')
                        print('kth1 2')
                        print('ucb2 3')
                        print('Try again...')
                # if save:
                #     save_name = notice.scenario+'-initcond'+str(initcond)+'-'+input_text[0]+'-'+input_text[1]
                #     with open('data/'+input_text[0]+'/%s-%d.pickle'%(save_name, int(time.time())), 'w') as f:
                #         pickle.dump((topic_world.history, notice.info), f)
                self.reset()

    def analyze_strat_val_loop(self, _):
        human_car = self.world.main_human_car
        robot_car = self.world.main_robot_car
        # iterate through relative velocity
        r_vrel_linspace = np.linspace(self.world.main_robot_car.strat_val.min_state[3],
            self.world.main_robot_car.strat_val.max_state[3], 50)
        for v_rel in r_vrel_linspace:
            x0_r = robot_car.traj.x0
            x0_r = [x0_r[0], x0_r[1], x0_r[2], v_rel]
            robot_car.traj.x0 = x0_r
            human_car.traj_r.x0 = x0_r
            time.sleep(0.1)
            pyglet.image.get_buffer_manager().get_color_buffer().save(
                self.analyze_strat_val_outdir + '{0}-vrel_{1}.png'.format(self.name, v_rel))
        
    def save_interaction_data(self):
        """Save interaction data."""
        # construct and save interaction data
        if not os.path.exists(self.save_interaction_data_dir):
            os.makedirs(self.save_interaction_data_dir)
        self.save_interaction_data_filename = self.save_interaction_data_dir + 'interaction_data.pickle'
        print 'Saving interaction data to {0}'.format(self.save_interaction_data_filename)
        data = []
        for car in self.world.cars:
            data.append([list(s) for s in car.history])
        with open(self.save_interaction_data_filename, 'w') as outfile:
            pickle.dump(data, outfile)
        # construct and save configuration of this scenario
        self.config_filename = self.save_interaction_data_dir + 'config.pickle'
        config = self.world.get_config()
        with open(self.config_filename, 'w') as config_file:
            pickle.dump(config, config_file)
        print 'Saving configuration of this scenario to {0}'.format(self.config_filename)
        print 'Finished saving interaction history.'

    def reset(self):
        for car in self.world.cars:
            car.reset()
        for note in self.world.notices: # Elis: added.
            note.reset()
        self.prev_t = self.world.simulator.time
        for car in self.world.cars:
            self.prev_x[car] = car.traj.x0
            self.anim_x[car] = car.traj.x0
        topic_program.paused = False

    def run(self, filename=None):
        self.reset()
        if filename is not None:
            with open(filename) as f:
                self.feed_u, self.feed_x = pickle.load(f)
        # if self.output is None:
        if self.manual:
            pyglet.clock.schedule_interval(self.manual_animation_loop, 0.4)
        else:
            # pyglet.clock.schedule_interval(self.animation_loop, 
            #     constants.ANIMATION_DT)
            pyglet.clock.schedule_interval(self.control_loop, self.dt)
        # else:
        #     self.subframes = 6
        #     self.frame = 0
        #     self.autoquit = True
        #     pyglet.clock.schedule(self.output_loop)

        # Set joysticks
        joysticks = pyglet.input.get_joysticks()
        print 'joysticks: ', joysticks
        if joysticks and len(joysticks) >= 1:
            self.joystick = joysticks[0]
            self.joystick.open()
        
        # Start asynchronous simulator and controller if in asynchronous mode.
        # if config.ASYNCHRONOUS:
        #     print 'Starting simulator.'
        #     self.world.simulator.start()
        #     print 'Starting controller.'
        #     self.world.controller.start()
        #     print 'Starting planners.' # start planner for the robot car.
        #     for car in self.world.cars:
        #         if not car.user_controlled:
        #             car.start_asynchronous_planner()

        # TODO: clean this up
        # Display the specified heatmap
        if self.heatmap_name is not None:
            eval('self.heatmap_{0}'.format(self.heatmap_name))()

        # robot_car = self.world.main_robot_car
        # human_car = self.world.main_human_car
        # self.set_heat(robot_car.strat_val.value_r_np, fw=np, car=robot_car)
        # self.heatmap_min_max_coords = (lambda: 
        #                 utils.strategic_reward_heatmap_coord(
        #                     robot_car.strat_val.min_state, 
        #                     robot_car.strat_val.max_state,
        #                     strat_dim=config.STRAT_DIM, 
        #                     x_h=robot_car.human.traj.x0))
        # self.set_heat(human_car.reward.strat_val_h_np, fw=np, 
        #                 car=human_car)
        # self.heatmap_show = True # show heatmap

        # self.plan_show = False # show plan

        try:
            self.event_loop.run()
        except KeyboardInterrupt:
            print "Main process interrupted. Sending kill signal to all threads."
            topic_program.kill = True

