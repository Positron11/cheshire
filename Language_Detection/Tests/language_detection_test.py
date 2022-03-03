import sys, os
sys.path.append('../')
from Cheshire.Language_Detection.language_detection import language_score

# get tests lists
positive_tests = [os.path.join("Language_Detection/Tests/Positive/", filename) for filename in os.listdir("Language_Detection/Tests/Positive/")]
ciphertext_tests = [os.path.join("Language_Detection/Tests/Negative/Ciphertext/", filename) for filename in os.listdir("Language_Detection/Tests/Negative/Ciphertext/")]
transliteration_tests = [os.path.join("Language_Detection/Tests/Negative/Transliteration/", filename) for filename in os.listdir("Language_Detection/Tests/Negative/Transliteration/")]

# for 2-grams and n-grams
for n in range(2,5,2):
	# open relevant wordwise n-gram dataset
	dataset = open(f"Language_Detection/Datasets/{n}grams.txt", "r")

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

	# close dataset
	dataset.close()