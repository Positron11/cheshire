import sys, os
sys.path.append('../')
from Cheshire.Language_Detection.language_detection import language_score

# get tests lists
positive_tests = [os.path.join("Language_Detection/Tests/Positive/", filename) for filename in os.listdir("Language_Detection/Tests/Positive/")]
ciphertext_tests = [os.path.join("Language_Detection/Tests/Negative/Ciphertext/", filename) for filename in os.listdir("Language_Detection/Tests/Negative/Ciphertext/")]
transliteration_tests = [os.path.join("Language_Detection/Tests/Negative/Transliteration/", filename) for filename in os.listdir("Language_Detection/Tests/Negative/Transliteration/")]

# for 2-grams and n-grams
for n in range(2,5,2):
	# construct dataset
	with open(f"Language_Detection/Datasets/4grams.txt") as frequency_dataset_file:
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

	# print header 
	print(f"\n{n}-GRAM TESTS:\n=============")

	# run tests
	for i in range(len(positive_tests)):
		# open test files
		positive_test = open(positive_tests[i])
		ciphertext_test = open(ciphertext_tests[i])
		transliteration_test = open(transliteration_tests[i])

		# run tests
		positive_test_result = language_score(positive_test, n, 'word', dataset)
		ciphertext_test_result = language_score(ciphertext_test, n, 'word', dataset)
		transliteration_test_result = language_score(transliteration_test, n, 'word', dataset)

		# print test results
		filename = positive_tests[i].split("/")[-1].split(" - ")[0]
		print(f"""{filename.split(' - ')[0]:18} || Positive: {positive_test_result:4.0f} | Ciphertext: {ciphertext_test_result:5.0f} | Transliteration: {transliteration_test_result:5.0f}""")

		# close test files
		positive_test.close()
		ciphertext_test.close()
		transliteration_test.close()