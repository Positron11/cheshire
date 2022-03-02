from numpy.random import rand
from random import shuffle, randint

# random playfair cipher key generator
def generate_key(ciphertext:str=[]) -> list:
	# get alphabet list
	alphabet = [chr(c) for c in range(97,123)]

	# remove most appropriate letter
	low_frequency_letters = [letter for letter in ["z", "q", "j"] if letter not in ciphertext]
	alphabet.remove(low_frequency_letters[0] if low_frequency_letters else "q")

	# shuffle and alphabet
	shuffle(alphabet)

	# construct and return key
	return [[letter for letter in alphabet [5*i:5*i+5]] for i in range(5)]


# convert 2d key to 1d list
def linearize_key(key:list) -> list:
	return [row[i] for row in key for i in range(len(key))]


# shuffle playfair cipher key
def shuffle_key(key:list, mode:str="", shuffles:int=1) -> list:
	# for number of shuffles
	for shuffle in range(shuffles):
		# get random value between 0 and 1
		selector = rand()

		# reverse key
		if (not mode and 0.98 <= selector < 1.00) or mode == "rwk":
			key.reverse()
			for row in key:
				row.reverse()

		# flip all columns
		if (not mode and 0.96 <= selector < 0.98) or mode == "rac":
			key.reverse()

		# flip all rows
		if (not mode and 0.94 <= selector < 0.96) or mode == "rar":
			for row in key:
				row.reverse()

		# flip random column
		if (not mode and 0.92 <= selector < 0.94) or mode == "rrc":
			# get random column
			column_index = randint(0,4)

			# construct and reverse column list
			column = [row[column_index] for row in key]
			column.reverse()

			# substitute reversed column values into key
			for row in key:
				row[column_index] = column[key.index(row)]

		# flip random row
		if (not mode and 0.90 <= selector < 0.92) or mode == "rrr":
			key[randint(0,4)].reverse()

		# swap two random letters
		if (not mode and 0 <= selector < 0.90) or mode == "swp":
			# initialize index variables
			x, y, i, j = 0, 0, 0, 0

			# get random indices, make sure distinct
			while x == i and y == j:
				x, y, i, j = randint(0,4), randint(0,4), randint(0,4), randint(0,4)

			# swap values
			key[x][y], key[i][j] = key[i][j], key[x][y]
	
	return key