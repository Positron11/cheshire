from os import remove
from secretpy import Playfair, CryptMachine
from Language_Detection.language_detection import language_score
from Simulated_Annealing.simulated_annealing import simulated_anneal
from Playfair_Keygen.playfair_keygen import generate_key, linearize_key, shuffle_key

# open dataset
dataset = open(f"Language_Detection/Datasets/4grams.txt", "r")

# create cryptmachine
key = generate_key()
machine = CryptMachine(Playfair())
machine.set_alphabet(linearize_key(key))

# encrypt plaintext file
with open("plaintext.txt") as file:
	ciphertext = machine.encrypt(file.read())

# annealing scedule function
def annealing_schedule(temp, i):
	return temp / float(i + 1)

def objective_function(key):
	# set key
	machine.set_alphabet(linearize_key(key))
	
	# write decryption output to file
	with open("decrypted.txt", "w") as textfile:
		print(machine.decrypt(ciphertext), file=textfile)

	# calculate language score
	with open("decrypted.txt", "r") as textfile:
		return language_score(text_file=textfile, ngram_length=4, ngram_type="word", frequency_dataset=dataset)

# anneal
best, score = simulated_anneal(
	initial_point=generate_key(ciphertext), 
	objective_function=objective_function, 
	step_function=shuffle_key, 
	annealing_schedule_function=annealing_schedule, 
	iterations=10000, initial_temperature=10, 
	verbose=True
)

# print result
machine.set_alphabet(linearize_key(best))
print(f"\n***\n\n{machine.decrypt(ciphertext)}")

# close dataset
dataset.close()

