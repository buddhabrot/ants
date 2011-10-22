#!/usr/bin/env python
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
    def __init__(self):
        # define class level variables, will be remembered between turns
        pass
    
    # do_setup is run once at the start of the game
    # after the bot has received the game settings
    # the ants class is created and setup by the Ants.run method
    def do_setup(self, ants):
        # initialize data structures after learning the game settings
        pass
    
    # do turn is run once per turn
    # the ants class has the game state and is updated by the Ants.run method
    # it also has several helper methods to use
    def do_turn(self, ants):
		orders = {}
		targets = {}
		ant_dist = []
		
		#occupy so no order goes here
		for hill_loc in ants.my_hills():
			targets[hill_loc] = hill_loc

		def do_move_direction(loc, direction):
			new_loc = ants.destination(loc, direction)
			if (ants.unoccupied(new_loc) and not new_loc in targets.values()):
				return new_loc
			else:
				return False
	
		def do_move_location(ant_loc, dst_loc):
			for direction in ants.direction(ant_loc, dst_loc):
				if do_move_direction(ant_loc, direction):
					return direction
				return False

		#gather food
		for food_loc in ants.food():
			for ant_loc in ants.my_ants():
				if ants.time_remaining() < 10:
					return

				dist = ants.distance(ant_loc, food_loc)
				ant_dist.append((dist, ant_loc, food_loc))				
			
		ant_dist.sort()
		for dist, ant_loc, food_loc in ant_dist:
			if (not food_loc in targets.values() and not ant_loc in orders):
				direction = do_move_location(ant_loc, food_loc)
				if direction:
					orders[ant_loc] = direction
					targets[ant_loc] = food_loc
					ants.issue_order((ant_loc, direction))

		#explore
		
				
		#free hill
		for hill_loc in ants.my_hills():
			if hill_loc in ants.my_ants() and not hill_loc in orders:
				for direction in ('n', 's', 'e', 'w'):
					if ants.time_remaining() < 10:
						return
					new_loc = do_move_direction(hill_loc, direction)
					if new_loc:
						orders[hill_loc] = direction
						targets[hill_loc] = new_loc
						ants.issue_order((hill_loc, direction))
						break

		#if ants.time_remaining() < 10:
		#	break
            
if __name__ == '__main__':
    # psyco will speed up python a little, but is not needed
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    try:
        # if run is passed a class with a do_turn method, it will do the work
        # this is not needed, in which case you will need to write your own
        # parsing function and your own game state class
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
