from secretpy import Playfair, CryptMachine
from Language_Detection.language_detection import language_score
from Simulated_Annealing.simulated_annealing import simulated_anneal
from Playfair_Keygen.playfair_keygen import generate_key, linearize_key, shuffle_key


# construct dataset
with open(f"Language_Detection/Datasets/4grams_continuous.txt") as frequency_dataset_file:
	# initialize vars
	dataset = dict()
	rank_counter = 1
	previous_frequency = -1

	# go through each fourgram in dataset_file
	for line in frequency_dataset_file:
		# extract fourgram and assign rank
		dataset[line.split()[0]] = rank_counter
		 
		# increment rank
		if line.split()[1] != previous_frequency:
			rank_counter += 1

		# set previous frequency buffer
		previous_frequency = line.split()[1]


# create cryptmachine
encryption_key = generate_key()
machine = CryptMachine(Playfair())
machine.set_alphabet(linearize_key(encryption_key))

# encrypt plaintext file
with open("Plaintexts/plaintext_1.txt") as test_file:
	ciphertext = machine.encrypt(test_file.read())
	encrypted_score = language_score(text=ciphertext, ngram_length=4, ngram_type="continuous", frequency_dataset=dataset)


# annealing schedule function
def annealing_schedule(current_temperature):
	return (0.93 * current_temperature) + 10


# objective key evaluation function
def objective_function(key):
	# set key
	machine.set_alphabet(linearize_key(key))

	# calculate language score
	return language_score(text=machine.decrypt(ciphertext), ngram_length=4, ngram_type="continuous", frequency_dataset=dataset)


# custom verbose function
def custom_verbose_function(**kwargs):
	# get keys
	buffer_key = linearize_key(kwargs['buffer'])
	current_key = linearize_key(kwargs['current'])
	best_key = linearize_key(kwargs['best'])

	# get decrypted texts
	machine.set_alphabet(buffer_key)
	buffer_decrypted = machine.decrypt(ciphertext)
	machine.set_alphabet(current_key)
	current_decrypted = machine.decrypt(ciphertext)
	machine.set_alphabet(best_key)
	best_decrypted = machine.decrypt(ciphertext)

	# print log
	buffer_string = f"BUFFER\n======\nDecrypted: {buffer_decrypted}\n--\nKey: {''.join(buffer_key)} (Score: {kwargs['buffer_evaluated']:.0f})"
	current_string = f"CURRENT\n=======\nDecrypted: {current_decrypted}\n--\nKey: {''.join(current_key)} (Score: {kwargs['current_evaluated']:.0f})"
	best_string = f"BEST\n====\nDecrypted: {best_decrypted}\n---\nKey: {''.join(best_key)} (Score: {kwargs['best_evaluated']:.0f})"
	return f"⤵\n\n{buffer_string}\n\n{current_string}\n\n{best_string}\n\n"


# print result function
def get_result(best, encryption_key, encrypted_score, decrypted_score):
	# decrypt ciphertext with obtained key
	decryption_key = linearize_key(best)
	machine.set_alphabet(decryption_key)
	decrypted = machine.decrypt(ciphertext)
	
	# print result to stdout and file
	print(f"\n***\n\nEncryption key: {''.join(linearize_key(encryption_key))}\nDecryption key: {''.join(decryption_key)}\n\nDecrypted: {decrypted}\n\nEncrypted Score: {encrypted_score:.0f}\nDecrypted Score: {decrypted_score:.0f}")
	with open("decrypted.txt", "w") as output_file:
		print(decrypted, file=output_file)


# run simulation
try:
	# anneal
	best, decrypted_score = simulated_anneal(
		initial_point=generate_key(ciphertext), 
		objective_function=objective_function, 
		step_function=shuffle_key, 
		annealing_schedule_function=annealing_schedule, 
		iterations=100, transitions=10000,
		max_non_improving_steps=10000,
		initial_temperature=100000, 
		verbose=custom_verbose_function
	)

	get_result(best, encryption_key, encrypted_score, decrypted_score)

# if keyboard interrupt signal sent, do before exiting
except KeyboardInterrupt:
	get_result(best, encryption_key, encrypted_score, decrypted_score)