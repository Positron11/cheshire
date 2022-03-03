from numpy import exp, random
from typing import Callable, Union

# simulated annealing algorithm
def simulated_anneal(initial_point, step_function:Callable, objective_function:Callable, annealing_schedule_function:Callable, iterations:int, transitions:int, max_non_improving_steps:int, initial_temperature:float, verbose:Union[str, Callable]=None) -> list:
	try:
		# generate an initial point
		best = initial_point
		# evaluate the initial point
		best_evaluated = objective_function(best)
		# set current point to initial point
		current, current_evaluated = best, best_evaluated

		# set current temperature
		current_temperature = initial_temperature

		# create non-improving counter
		non_improving_steps = 0

		# run the algorithm
		for i in range(iterations):
			for j in range(transitions):
				# load new point into buffer
				buffer = step_function(current)

				# evaluate buffer point
				buffer_evaluated = objective_function(buffer)

				# check if buffer better than best point...
				if buffer_evaluated < best_evaluated:
					# set best point to current buffer ppoint
					best, best_evaluated = buffer, buffer_evaluated
				else:
					non_improving_steps += 1

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
					# set step counter string
					step_counter = f"[it:{i:0{len(str(iterations))}}|tr:{j:0{len(str(transitions))}}|te:{current_temperature:.2f}]>"
					
					# print log
					if verbose == "long" or verbose == "short": # if built-in verbose
						metropolis_acceptance = f"[{random_point:1.5f} vs {metropolis:1.5f}]"
						buffer_evaluation = f"""{f'f({str(buffer)[:25]}{"..." if len(str(buffer)) > 25 else ""}) = ' if verbose == "long" else ''}{buffer_evaluated:10.2f}"""
						print(f"{step_counter} {buffer_evaluation} | CURRENT: {current_evaluated:10.2f} | BEST: {best_evaluated:10.2f} || DIFF: {diff:10.2f} | MET: {metropolis_acceptance}")
					elif callable(verbose): # if custom verbose function
						print(f"{step_counter} {current_evaluated:7.0f} | {verbose(current=current, best=best, current_evaluated=current_evaluated, best_evaluated=best_evaluated)}")

				# reset if exceeded non-improving step limit
				if non_improving_steps > max_non_improving_steps:
					non_improving_steps = 0
					current = best

			# calculate temperature for new epoch 
			current_temperature = annealing_schedule_function(current_temperature)

		# return best point and best point score
		return [best, best_evaluated]

	# if keyboard interrupt signal sent, do before exiting
	except KeyboardInterrupt:
		# return best point and best point score
		return [best, best_evaluated]