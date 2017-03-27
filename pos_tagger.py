import nltk
import ontology
import string
from nltk.corpus import stopwords

###########################################################################

# Get ontology
defect_dict = ontology.buildOntology()

# Tag list for pos tag checking
adj_tags = ["JJ", "JJR", "JJS"]
adv_tags = ["RB", "RBR", "RBS"]

###########################################################################

# Check if present in dictionary.
# If yes, return the list of defect words.
# Else, return 0
def check_defect_dict(word):
	
	empty_list = []
	if word in defect_dict.keys():
		return defect_dict[word]
	else:
		return empty_list

# Check how close a word is to the words in the list
# Using wordnet features here
def closeness_check(word,defect_list):

	if word in defect_list:
		return 1
	else:
		return 0

# Remove the various punctuations from the text
def remove_punc(text):
	return text.translate(None, string.punctuation)

###########################################################################

# Use POS Tagging to tag words.
# STEP 1 - Check if defect word is present. If not, return 0
# STEP 2 - If present, use closeness of adjectives (with list of adjectives to describe the defect) to decide if defect or not
def pos_tag_dd(text):

	print "\nPOS TAGGING DEFECT DETECTION\n"

	text_list = text.split()

	defect_word = ""
	defect_list = []

	# Check if any word is in defect_dictionary
	# If not, it is not a defect
	for word in text_list:
		defect_list = check_defect_dict(word)
		if defect_list:
			defect_word = word
			break

	print "Defect word found : " + defect_word
	if (defect_word == ""):
		return 0

	# Picks the adjective and prints. Doesn't work very well. Shortcomings of POS tagging
	pos_tag_list = nltk.pos_tag(nltk.word_tokenize(text))
	for word_tag in pos_tag_list:
		
		# Find all adjective related words 
		if word_tag[1] in adj_tags:
			if closeness_check(word_tag[0],defect_list) == 1:
				print "Describing word found : " + (word_tag[0])
				return 1

	return 0

############################################################################

# Naive Checking.
# STEP 1 - Remove stop words from sentence
# STEP 2 - Check if defect word is present. If not, return 0
# STEP 3 - Check closeness with adjective list for each word
def naive_dd(text):

	print "\nNAIVE DEFECT DETECTION\n"

	# Remove the stopwords
	punc_remove_text = remove_punc(text)
	stop_list = set(stopwords.words('english'))
	cleaned_text = [i for i in punc_remove_text.lower().split() if i not in stop_list]
	print "Stopword-removed list of words:"
	print cleaned_text

	defect_word = ""
	defect_list = []

	# Check if any word is in defect_dictionary
	# If not, it is not a defect
	for word in cleaned_text:
		defect_list = check_defect_dict(word)
		if defect_list:
			defect_word = word
			break

	print "Defect word found : " + defect_word
	if (defect_word == ""):
		return 0

	# Check word by word for closeness with defect_list
	for word in cleaned_text:
		if closeness_check(word,defect_list) == 1:
			print "Describing word found : " + word
			return 1

	return 0

###########################################################################

text = ""
print pos_tag_dd(text)
print naive_dd(text)