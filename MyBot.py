#!/usr/bin/env python
from ants import *

# define a class with a do_turn method
# the Ants.run method will parse and update bot input
# it will also run the do_turn method for us
class MyBot:
	closest_unseens = []
	furthest_unseens = []
	food_locs = []

	def __init__(self):
		pass
    
	def do_setup(self, ants):
		pass
	
	def update_cartography(self, ants):
		#changed food_locs
		for food_loc in self.food_locs:
			food_row, food_col = food_loc
			if ants.map[food_row][food_col] != FOOD:
				self.food_locs.remove(food_loc)

		#new food locs
		for food_loc in ants.food():
			if food_loc not in self.food_locs:
				self.food_locs.append(food_loc)
    
	def do_turn(self, ants):
		orders = {}
		targets = {}
		ant_dist = []
		
		#update map
		self.update_cartography(ants)

		#occupy so no order ever goes here
		for hill_loc in ants.my_hills():
			targets[hill_loc] = hill_loc

		def do_move_direction(loc, direction):
			new_loc = ants.destination(loc, direction)
			if (ants.unoccupied(new_loc) and ants.passable(new_loc) and 
				not new_loc in targets.values()):
				return new_loc
			else:
				return False
	
		def do_move_location(ant_loc, dst_loc):
			for direction in ants.direction(ant_loc, dst_loc):
				new_loc = do_move_direction(ant_loc, direction)
				if new_loc:
					return (new_loc, direction)
				return (False, False)

		#gather food
		for food_loc in self.food_locs:
			for ant_loc in ants.my_ants():
				if ants.time_remaining() < 10:
					return

				dist = ants.distance(ant_loc, food_loc)
				ant_dist.append((dist, ant_loc, food_loc))				
			
		ant_dist.sort()
		for dist, ant_loc, food_loc in ant_dist:
			if (not food_loc in targets.values() and not ant_loc in orders):
				new_loc, direction = do_move_location(ant_loc, food_loc)
				if direction:
					orders[ant_loc] = direction
					targets[ant_loc] = new_loc
					ants.issue_order((ant_loc, direction))

		#explore (scout)
		

		#explore (terrain)
		
				
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
