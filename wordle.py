import pandas as pd
from collections import Counter

def get_all_words(file_name):
	"""
	Read data from CSV into dataframe
	"""
	return pd.read_csv(file_name, sep='\t', names=['word','frequency'])

def word_length_filter(df, word_length):
	"""
	Create a new df with only the words of the proper length
	"""
	length_checker = lambda x: len(str(x)) == word_length
	length_mask = df['word'].apply(length_checker)
	return df[length_mask].reset_index(drop=True)

def common_words_filter(df):
	"""
	Create a new df with only the most common words of the proper length
	"""
	num_top_words = 1000
	return df.iloc[:num_top_words,:].reset_index(drop=True)

def letter_positions(words_list, word_length):
	"""
	Loop through all words and track location of letters by position using a dictionary.
	Keys = integers of each position in word_length
	Values = list of allocated letters with total length equal to number of words in words_list
	"""
	dictionary = {key: [].copy() for key in list(range(word_length))}
	
	for word in words_list:
		for loc in range(word_length):
			letter = word[loc]
			dictionary[loc].append(letter)

	return dictionary

def letter_positions_common(word_length, dict_letter_positions, num_top_letters):
	"""
	Create a dictionary of the top most common letters by position
	Keys = integers of each position in word_length
	Values = list of most common letters with total length equal to num_top_letters
	"""
	dictionary = {key: [].copy() for key in list(range(word_length))}

	for loc in range(word_length):
		letters_list = dict_letter_positions[loc]
		count = Counter(letters_list)
		most_common_letters = count.most_common(num_top_letters)
		for letter in most_common_letters:
			dictionary[loc].append(letter[0])

	return dictionary

def find_good_words(word_length, words_list, dict_letter_positions_common):
	""" 
	Create list of words where each letter by position is in the list of most common letters in that position
	"""
	good_words_list = []

	for word in words_list:
		is_good_word = True
		for loc in range(word_length):
			letter = word[loc]
			position_common_letters = dict_letter_positions_common[loc]
			if not letter in position_common_letters:
				is_good_word = False

		if is_good_word:
			good_words_list.append(word)

	return good_words_list

def find_combinations_double(word_length, good_words_list):
	"""
	From the list of good words, check every unqiue double combination (pair)
	Only return those that have fully unique letters, defined as word_length * 2
	"""
	first_word = ""
	second_word = ""
	combo_list = []

	for x in range(len(good_words_list)):

		for y in range(x + 1, len(good_words_list)):

			first_word = good_words_list[x]
			second_word = good_words_list[y]
			total_letters = len(list(set(first_word + second_word)))

			if total_letters == (word_length * 2):
				combo_list.append(tuple((first_word, second_word)))

	return combo_list

def find_combinations_triple(word_length, good_words_list):
	"""
	From the list of good words, check every unqiue triple combination
	Only return those that have fully unique letters, defined as word_length * 3
	"""
	first_word = ""
	second_word = ""
	third_word = ""
	combo_list = []

	for x in range(len(good_words_list)):

		for y in range(x + 1, len(good_words_list)):

			for z in range(y + 1, len(good_words_list)):

				first_word = good_words_list[x]
				second_word = good_words_list[y]
				third_word = good_words_list[z]
				total_letters = len(list(set(first_word + second_word + third_word)))

				if total_letters == (word_length * 3):
					combo_list.append(tuple((first_word, second_word, third_word)))

	return combo_list

def efficiency_algorithm(word_length, words_list, num_words_suggest, dict_letter_positions):
	"""
	Find combinations of words with which to start the game
	These words must have letters that match the most common letters in each letter slot
	Ideally we would only need the top few letters in each position, so we start with 3
	In reality, will likely need several more (depending on num_words_suggest), so slowly increment until combinations are found
	"""
	num_top_letters = 3
	found_combos = False
	
	while found_combos == False:

		dict_letter_positions_common = letter_positions_common(word_length, dict_letter_positions, num_top_letters)
		good_words_list = find_good_words(word_length, words_list, dict_letter_positions_common)
		
		if num_words_suggest == 2:
			combos_list = find_combinations_double(word_length, good_words_list)
		elif num_words_suggest == 3:
			combos_list = find_combinations_triple(word_length, good_words_list)
		
		if combos_list:
			for combo in combos_list:
				print(combo)
			found_combos = True
		else:
			num_top_letters += 1

def main(word_length, num_words_suggest):
	
	file_name = 'word_list.txt'
	
	# create dataframe of all English words along with their frequency
	df_words = get_all_words(file_name)

	# create a new dataframe only with the words of the correct length
	df_words_correct_length = word_length_filter(df_words, word_length)

	# create a new dataframe only with the most common words of the correct length
	df_words_correct_length_common = common_words_filter(df_words_correct_length)
	
	# convert the remaining words into a list
	words_list = df_words_correct_length_common['word'].to_list()

	# create a dictionary tracking how all the words allocate letters to each position
	dict_letter_positions = letter_positions(words_list, word_length)

	# find pairs of words based on the most common letters in each position
	efficiency_algorithm(word_length, words_list, num_words_suggest, dict_letter_positions)

if __name__ == '__main__':
	
	word_length = 5
	
	# must take a value of 2 or 3
	num_words_suggest = 2 

	if num_words_suggest not in (2,3):
		raise ValueError("Number of suggested words must be 2 or 3")

	main(word_length, num_words_suggest)