import re, unicodedata
from typing import TextIO

# n-gram heuristic function
def language_score(text_file:TextIO, ngram_length:int, ngram_type:str, frequency_dataset:TextIO, verbose:bool=False) -> float:
	# sanitize text
	sanitized_text = ''.join(c for c in unicodedata.normalize('NFD', text_file.read()) if unicodedata.category(c) != 'Mn')
	
	# strip non-alphabetic characters and extract ngrams from stripped text
	if ngram_type == "word":
		plaintext = re.sub('[^a-zA-Z ]+', '', sanitized_text).upper()
		ngrams = [word[i:i+ngram_length] for word in plaintext.split() for i in range(len(word) - (ngram_length - 1))]
	elif ngram_type == "continuous":
		plaintext = re.sub('[^a-zA-Z]+', '', sanitized_text).upper()
		ngrams = [plaintext[i:i+ngram_length] for i in range(len(plaintext) - (ngram_length - 1))]
	
	# create ngram ranked dictionary
	distinct_ngram_list = [ngram for n, ngram in enumerate(ngrams) if ngram not in ngrams[:n]]
	ngram_frequency_list = [ngrams.count(ngram) for ngram in distinct_ngram_list]
	ngram_dictionary = {distinct_ngram_list[i]:ngram_frequency_list[i] for i in range(len(distinct_ngram_list))}

	# initialize scores and counts
	language_score = 0
	ngrams_found = 0
	dataset_ngram_count = 0

	# go through each fourgram in dataset
	for line_number, line in enumerate(frequency_dataset, 1):
		# extract fourgram and frequency from line
		data = {"ngram": line.split()[0], "frequency": line.split()[1]}

		# if fourgram in text
		if data["ngram"] in ngram_dictionary.keys():
			# increment scores and counters
			language_score += line_number - ngram_dictionary[data["ngram"]]

			# increment number of ngrams found
			ngrams_found += 1

			# # verbose output
			if verbose:
				print(f"found: {data['ngram']} | ngram diff: {line_number - ngram_dictionary[data['ngram']]} | total score: {language_score}")
	
		# increment dataset ngram count
		dataset_ngram_count += 1

	# reset read pointers
	text_file.seek(0)
	frequency_dataset.seek(0)

	# add unfound ngram penalty
	language_score += (len(ngram_dictionary) - ngrams_found) * dataset_ngram_count
	
	# return final score
	return language_score / len(ngram_dictionary)