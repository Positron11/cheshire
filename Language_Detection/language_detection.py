from numpy import abs
import re, unicodedata
from typing import TextIO

# n-gram heuristic function
def language_score(text_file:TextIO, ngram_length:int, ngram_type:str, frequency_dataset:TextIO, verbose:bool=False) -> float:
	# sanitize text
	sanitized_text = ''.join(c for c in unicodedata.normalize('NFD', text_file.read()) if unicodedata.category(c) != 'Mn')

	# strip non-alphabetic characters and extract ngrams from stripped text
	if ngram_type == "word": # word-by-word ngram extraction
		stripped_text = re.sub('[^a-zA-Z ]+', '', sanitized_text).upper()
		ngrams = [word[i:i+ngram_length] for word in stripped_text.split() for i in range(len(word) - (ngram_length - 1))]
	elif ngram_type == "continuous": # continuous (between words) ngram extraction
		stripped_text = re.sub('[^a-zA-Z]+', '', sanitized_text).upper()
		ngrams = [stripped_text[i:i+ngram_length] for i in range(len(stripped_text) - (ngram_length - 1))]
	
	# create ngram ranked dictionary
	ngram_frequencies = [ngrams.count(ngram) for ngram in ngrams]
	ranked_ngram_frequencies = sorted([frequency for n, frequency in enumerate(ngram_frequencies) if frequency not in ngram_frequencies[:n]], reverse=True)
	ranked_ngrams = {ngram:ranked_ngram_frequencies.index(ngrams.count(ngram)) + 1 for ngram in ngrams}

	# initialize scores and counts
	language_score = 0
	dataset_length = 0
	ngrams_found = list()

	# go through each fourgram in dataset
	for line_number, line in enumerate(frequency_dataset, 1):
		# extract fourgram and frequency from line
		data = {"ngram": line.split()[0], "frequency": line.split()[1]}

		# if fourgram in text
		if data["ngram"] in ngrams:
			# increment scores and counters
			language_score += abs(line_number - ranked_ngrams[data["ngram"]])
			ngrams_found.append(data["ngram"])

			# verbose output
			if verbose:
				print(f"found: {data['ngram']} | ngram diff: abs({line_number - ranked_ngrams[data['ngram']]}) | total score: {language_score}")
	
		# increment dataset ngram count
		dataset_length += 1

	# reset read pointers
	text_file.seek(0)
	frequency_dataset.seek(0)

	# add unfound ngram penalty and normalize score for text size
	language_score = (language_score + ((len(ranked_ngrams) - len(ngrams_found)) * dataset_length)) / len(ranked_ngrams)
	
	# verbose output
	if verbose:
		print(f'{"="*50}\nUnfound: {", ".join([ngram for ngram in ranked_ngrams.keys() if ngram not in ngrams_found])}')
		print(f"Final score: {language_score}")

	# return final score
	return language_score