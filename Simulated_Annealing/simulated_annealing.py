from typing import Callable
from numpy import exp, random

# simulated annealing algorithm
def simulated_anneal(initial_point, step_function:Callable, objective_function:Callable, annealing_schedule_function:Callable, iterations:int, transitions:int, initial_temperature:float, verbose:str="") -> list:
	# generate an initial point
	best = initial_point
	# evaluate the initial point
	best_evaluated = objective_function(best)
	# set current point to initial point
	current, current_evaluated = best, best_evaluated

	# set current temperature
	current_temperature = initial_temperature

	# run the algorithm
	for i in range(iterations):
		# calculate temperature for current epoch 
		current_temperature = annealing_schedule_function(initial_temperature, i)

		for j in range(transitions):
			# load new point into buffer
			buffer = step_function(current)

			# evaluate buffer point
			buffer_evaluated = objective_function(buffer)

			# check if buffer better than best point...
			if buffer_evaluated < best_evaluated:
				# set best point to current buffer ppoint
				best, best_evaluated = buffer, buffer_evaluated

			# ...otherwise find difference between buffer and current point evaluations
			diff = buffer_evaluated - current_evaluated

			# calculate metropolis acceptance criterion
			metropolis = exp(-diff / current_temperature)

			# check if keeping new point
			random_point = random.rand()
			if diff < 0 or random_point < metropolis:
				# store the new current point
				current, current_evaluated = buffer, buffer_evaluated

			# report progress
			if verbose:
				metropolis_acceptance = f"[{random_point:1.5f} vs {metropolis:1.5f}]"
				step_counter = f"[it:{i:0{len(str(iterations))}}|tr:{j:0{len(str(transitions))}}|te:{current_temperature:.2f}]>"
				buffer_evaluation = f"""{f'f({str(buffer)[:25]}{"..." if len(str(buffer)) > 25 else ""}) = ' if verbose == "long" else ''}{buffer_evaluated:10.2f}"""
				print(f"{step_counter} {buffer_evaluation} | CURRENT: {current_evaluated:10.2f} | BEST: {best_evaluated:10.2f} || DIFF: {diff:10.2f} | MET: {metropolis_acceptance}")

	# return best point and best point score
	return [best, best_evaluated]