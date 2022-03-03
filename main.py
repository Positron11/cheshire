from secretpy import Playfair, CryptMachine
from Language_Detection.language_detection import language_score
from Simulated_Annealing.simulated_annealing import simulated_anneal
from Playfair_Keygen.playfair_keygen import generate_key, linearize_key, shuffle_key

# open dataset and test file
dataset = open(f"Language_Detection/Datasets/4grams_continuous.txt", "r")
test_file = open("Plaintexts/plaintext_1.txt");

# create cryptmachine
key = generate_key()
machine = CryptMachine(Playfair())
machine.set_alphabet(linearize_key(key))

# encrypt plaintext file
ciphertext = machine.encrypt(test_file.read())

# annealing scedule function
def annealing_schedule(current_temperature):
	return (0.993 * current_temperature) + 0.0001

def objective_function(key):
	# set key
	machine.set_alphabet(linearize_key(key))
	
	# write decryption output to file
	with open("decrypted.txt", "w") as textfile:
		print(machine.decrypt(ciphertext), file=textfile)

	# calculate language score
	with open("decrypted.txt", "r") as textfile:
		return language_score(text_file=textfile, ngram_length=4, ngram_type="continuous", frequency_dataset=dataset)

# anneal
best, score = simulated_anneal(
	initial_point=generate_key(ciphertext), 
	objective_function=objective_function, 
	step_function=shuffle_key, 
	annealing_schedule_function=annealing_schedule, 
	iterations=500, transitions=100,
	initial_temperature=100000, 
	verbose="short"
)

# print result
machine.set_alphabet(linearize_key(best))
print(f"\n***\n\n{machine.decrypt(ciphertext)}")

# close dataset and test file
dataset.close()
test_file.close()

