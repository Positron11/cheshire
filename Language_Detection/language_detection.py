from numpy import abs
import re, unicodedata

# n-gram heuristic function
def language_score(text:str, ngram_length:int, ngram_type:str, frequency_dataset:dict, verbose:bool=False) -> float:
	# extract ngrams from text
	ngrams = extract_ngrams(text, ngram_length, ngram_type)
	
	# create ngram ranked dictionary
	ngram_frequencies = [ngrams.count(ngram) for ngram in ngrams]
	ranked_ngram_frequencies = sorted([frequency for n, frequency in enumerate(ngram_frequencies) if frequency not in ngram_frequencies[:n]], reverse=True)
	ranked_ngrams = {ngram:ranked_ngram_frequencies.index(ngrams.count(ngram)) + 1 for ngram in ngrams}

	# initialize scores and counts
	dissimilarity_score = 0
	unfound_ngrams = list()

	# get frequency dataset length
	dataset_length = len(frequency_dataset)

	# go through each fourgram in dataset
	for ngram in ngrams:
		# if fourgram in dataset
		try:
			# get rank difference
			rank_diff = frequency_dataset[ngram] - ranked_ngrams[ngram]

			# increment scores and counters
			dissimilarity_score += abs(rank_diff)

			# verbose output
			if verbose:
				print(f"found: {ngram} | ngram diff: abs({rank_diff}) | total score: {dissimilarity_score}")
		
		# if not in dataset
		except:
			unfound_ngrams.append(ngram)

	# add unfound ngram penalty and normalize score for text size
	normalized_dissimilarity_score = (dissimilarity_score + (len(unfound_ngrams) * dataset_length)) / (len(ranked_ngrams) if ranked_ngrams else 1)
	
	# verbose output
	if verbose:
		print(f'\n**\n\nUnfound: {", ".join(unfound_ngrams) if unfound_ngrams else "None"}')
		print(f"Total Dissimilarity score: {dissimilarity_score:.3f}")
		print(f"Normalized Dissimilarity score: {normalized_dissimilarity_score:.3f}")

	# return final score
	return normalized_dissimilarity_score


# ngram extractor function
def extract_ngrams(text:str, ngram_length:int, ngram_type:str) -> list:
	# sanitize text
	sanitized_text = ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

	# strip non-alphabetic characters and extract ngrams from stripped text
	if ngram_type == "word": # word-by-word ngram extraction
		stripped_text = re.sub('[^a-zA-Z ]+', '', sanitized_text).upper()
		return [word[i:i+ngram_length] for word in stripped_text.split() for i in range(len(word) - (ngram_length - 1))]
	elif ngram_type == "continuous": # continuous (between words) ngram extraction
		stripped_text = re.sub('[^a-zA-Z]+', '', sanitized_text).upper()
		return [stripped_text[i:i+ngram_length] for i in range(len(stripped_text) - (ngram_length - 1))]
	else:
		raise NgramTypeError(ngram_type)


# ngram type exception
class NgramTypeError(Exception):
    def __init__(self, ngram_type=None):
        self.ngram_type = ngram_type

    def __str__(self):
        return f"""Invalid ngram type {'"' + self.ngram_type + '"' if self.ngram_type else ''}"""