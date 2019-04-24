# Elis: Maybe this is a bit too much, but it is convenient.
import pyglet

class Notice(object):
    def __init__(self, name = None, info_func = None, info = None):
        self.name = name 
        self.info_func = info_func # check info function.
        self.info = info # last updated info.
    def reset(self):
        pass

class Truck_Maniac(Notice): # Alert when maniac comes.
    def __init__(self, *args, **vargs):
        Notice.__init__(self, *args, **vargs)
        self.name = 'maniac'
        self.have_played = False
        self.beep = pyglet.media.load("beep_new.mp3", streaming=False)
    def reset(self):
		self.have_played = False

class Truck_Exit(Notice): # Alert when off-ramp comes.
    def __init__(self, *args, **vargs):
        Notice.__init__(self, *args, **vargs)
        self.name = 'exit'
        self.have_played = False
        self.beep = pyglet.media.load("beep_new.mp3", streaming=False)
    def reset(self):
        self.have_played = False

class Quit(Notice): # Quit the simulation when done. Simulation is done when info is 1 or -1.
    def __init__(self, *args, **vargs):
        Notice.__init__(self, *args, **vargs)
        self.name = 'quit'
    def reset(self):
        self.info = 0

#class Quit_Exit(Notice): # Quit the simulation when done. Simulation is done when info is 1 or -1.
#    def __init__(self, *args, **vargs):
#        Notice.__init__(self, *args, **vargs)
#        self.name = 'quit'
#        self.exit_begins = 5000. # Will change when car passes truck gap.
#        self..W = 5.
#        self..U = 30. # Was W=8 and U=40
#        self.exit_ends = exit_begins+W
#    def reset(self):
#        self.info = 0
#        self.exit_begins = 5000. # Will change when car passes truck gap.
#        self..W = 5.
#        self..U = 30. # Was W=8 and U=40
#        self.exit_ends = exit_begins+W










