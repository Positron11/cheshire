from typing import Callable
from numpy import exp, random

# simulated annealing algorithm
def simulated_anneal(initial_point, step_function:Callable, objective_function:Callable, annealing_schedule_function:Callable, iterations:int, initial_temperature:float, verbose:bool=False) -> list:
	# generate an initial point
	best = initial_point

	# evaluate the initial point
	best_evaluated = objective_function(best)

	# set current point to initial point
	current, current_evaluated = best, best_evaluated

	# run the algorithm
	for i in range(iterations):
		# load new point into buffer
		buffer = step_function(current)

		# evaluate buffer point
		buffer_evaluated = objective_function(buffer)

		# check if buffer better than best point...
		if buffer_evaluated < best_evaluated:
			# set best point to current buffer ppoint
			best, best_evaluated = buffer, buffer_evaluated
			
		# report progress
		if verbose:
			print(f"{i:04}> f({str(buffer)[:50]}{'...' if len(str(buffer)) > 50 else ''}) = {buffer_evaluated:10.3f} | BEST: {best_evaluated}")

		# ...otherwise find difference between buffer and current point evaluations
		diff = buffer_evaluated - current_evaluated

		# calculate temperature for current epoch 
		temperature = annealing_schedule_function(initial_temperature, i)

		# calculate metropolis acceptance criterion
		metropolis = exp(-diff / temperature)

		# check if keeping new point
		if diff < 0 or random.rand() < metropolis:
			# store the new current point
			current, current_evaluated = buffer, buffer_evaluated

	# return best point and best point score
	return [best, best_evaluated]