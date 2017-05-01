import nltk
import ontology, wordnet_closeness, dependency
import string
from nltk.corpus import stopwords
import sys

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
    
    return wordnet_closeness.closeness(word,defect_list) 

# Remove the various punctuations from the text
def remove_punc(text):
    return text.translate(None, string.punctuation)

def negative_present(word_list,keyword):
    text = word_list[0]
    for i in range(len(word_list)-1):
        text += " " + word_list[i+1]
    return dependency.check_neg(text,keyword)

###########################################################################

# Use POS Tagging to tag words.
# STEP 1 - Check if defect word is present. If not, return 0
# STEP 2 - If present, use closeness of adjectives (with list of adjectives to describe the defect) to decide if defect or not
def pos_tag_dd(text,isPrint,window,threshold):

    if (isPrint):
        print "\nPOS TAGGING DEFECT DETECTION\n"

    text = text.lower()
    punc_remove_text = remove_punc(text)
    text_list = punc_remove_text.split()
    pos_tag_list = nltk.pos_tag(nltk.word_tokenize(text))
    
    if (isPrint):
        print "POS tagging of text:"
        print pos_tag_list

    defect_word = ""
    defect_list = []

    # Check if any word is in defect_dictionary
    # If not, it is not a defect
    for i in range(len(text_list)):

        word = text_list[i]

        defect_list = check_defect_dict(word)
        if defect_list:
            defect_word = word

            # Local parameters
            done = 0
            lower = max(i-window,0)
            upper = min(i+window+1,len(text_list))
            
            # Checks the adjectives in the text and checks closeness with defect list
            for j in range(lower,upper):

                if j == i:
                    continue

                word_tag = pos_tag_list[j]

                # Find all adjective related words 
                if word_tag[1] in adj_tags or word_tag[1] in adv_tags:
                    closest_defect = closeness_check(word_tag[0],defect_list)
                    if closest_defect[0] > threshold:

                        # If negative sentiment present, then it should not be a defect.
                        if negative_present(text_list,word_tag[0]):
                            if (isPrint):
                                print "Defect found. But negative word also present. Negating meaning."
                            return 0
                        else:
                            if (isPrint):
                                print "Describing word found : " + (word_tag[0]) + " (matched with " + closest_defect[1] +  ") for " + defect_word + ". Score: " + str(closest_defect[0])
                            done = 1
                            break

            if done == 1:
                continue
            elif (isPrint):
                print "Component '" + defect_word + "' found. But no defect keyword corresponding to it is found. Hence not a defect."


    if (defect_word == ""):
        if (isPrint):
            print "No component found."

    return 0

############################################################################

# Naive Checking.
# STEP 1 - Remove stop words from sentence
# STEP 2 - Check if defect word is present. If not, return 0
# STEP 3 - Check closeness with adjective list for each word
def naive_dd(text,isPrint,window,threshold):

    if (isPrint):
        print "\nNAIVE DEFECT DETECTION\n"

    # Remove the stopwords
    text = text.lower()
    punc_remove_text = remove_punc(text)
    stop_list = set(stopwords.words('english'))
    # cleaned_text = [i for i in punc_remove_text.split() if i not in stop_list]
    cleaned_text =  punc_remove_text.split()

    if (isPrint):
        print "Stopword-removed list of words:"
        print cleaned_text

    defect_word = ""
    defect_list = []

    # Check if any word is in defect_dictionary
    # If not, it is not a defect
    for i in range(len(cleaned_text)):

        word = cleaned_text[i]

        defect_list = check_defect_dict(word)
        if defect_list:
            defect_word = word
            
            # Local parameters
            done = 0
            lower = max(i-window,0)
            upper = min(i+window+1,len(cleaned_text))

            # Check word by word for closeness with defect_list
            for j in range(lower,upper):

                # If component word found, then don't check with it
                if j == i:
                    continue

                word = cleaned_text[j]

                closest_defect = closeness_check(word, defect_list)
                if closest_defect[0] > threshold:
                    # If negative sentiment present, then it should not be a defect.
                    if negative_present(cleaned_text,word):
                        if (isPrint):
                            print "Defect found. But negative word also present. Negating meaning."
                        return 0
                    else:
                        if (isPrint):
                            print "Describing word found : " + word + " (matched with " + closest_defect[1] +  ") for " + defect_word + ". Score: " + str(closest_defect[0])
                        done = 1
                        break

            if done == 1:
                continue
            elif (isPrint):
                print "Component '" + defect_word + "' found. But no defect keyword corresponding to it is found. Hence not a defect."

    if (defect_word == ""):
        if (isPrint):
            print "No component found."

    return 0

###########################################################################


# Read lines from camera_reviews_corpus.txt and append the corresponding tuple into test_data
def make_corpus(corpus_file):

    test_data = []
    
    f = open(corpus_file,'r')
    for line in f:
        if line[-1] == "\n":
            test_data.append(line[:-1])
        else:
            test_data.append(line)

    f.close()
    return test_data

# Given a corpus of text, evaluate the various methods
def evaluate_corpus(corpus, printWrong, writeInFile, isOnline, threshold, window):

    if (isOnline):

        print "Online System Entered"
        print "Enter 'quit' to exit from the system"

        sentence = raw_input(">> ")
        while (sentence != "quit"):

            # Matching the sentence
            print "-------------------------------------------------------------------------------------------"

            pos_tag_annotation = pos_tag_dd(sentence,1,window,threshold)
            print "\n------------------------------------"
            naive_annotation = naive_dd(sentence,1,window,threshold)

            print "\n==========================================================================================\n\n"

            sentence = raw_input(">> ")

    else:

        dataset = make_corpus(corpus)
        # pos_tag_prediction = []
        # naive_prediction = []

        for data_point in dataset:

            sentence = data_point

            print "Sentence: " + sentence
            print "-------------------------------------------------------------------------------------------"

            pos_tag_annotation = pos_tag_dd(sentence,1,window,threshold)
            print "\n------------------------------------"
            naive_annotation = naive_dd(sentence,1,window,threshold)

            # pos_tag_prediction.append(pos_tag_annotation)
            # naive_prediction.append(naive_annotation)

            print "\n==========================================================================================\n\n"

            sys.stdin.read(1)


############################################################################

evaluate_corpus("demo_sentences.txt",0,1,1,0.15,5)
