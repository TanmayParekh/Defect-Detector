import nltk
import ontology, wordnet_closeness, dependency
import string
from nltk.corpus import stopwords


###########################################################################

# Get ontology
defect_dict = ontology.buildOntology()

# Tag list for pos tag checking
adj_tags = ["JJ", "JJR", "JJS"]
adv_tags = ["RB", "RBR", "RBS"]
not_wordlist = ["not","none"]

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
    pos_tag_list = nltk.pos_tag(nltk.word_tokenize(punc_remove_text))
    
    if (isPrint):
        print "POS tagging of text:"
        print pos_tag_list

    defect_word = ""
    defect_list = []
    defect_found = 0

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
                            defect_found = 1
                            break

            if done == 1:
                continue
            elif (isPrint):
                print "Component '" + defect_word + "' found. But no defect keyword corresponding to it is found. Hence not a defect."

    if defect_found == 1:
        return 1

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
    defect_found = 0

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
                        defect_found = 1
                        break

            if done == 1:
                continue
            elif (isPrint):
                print "Component '" + defect_word + "' found. But no defect keyword corresponding to it is found. Hence not a defect."

    if defect_found == 1:
        return 1

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
        split_line = line.split("|")
        test_tuple = (split_line[0],int(split_line[1]))
        test_data.append(test_tuple)

    f.close()
    return test_data

# Calculate the confusion matrix given true and predicted values
def make_confusion_matrix(true_label,predicted_label):

    con_matrix = [[0 for x in range(2)] for y in range(2)]
    mismatched = []

    for i in range(len(true_label)):
        if (true_label[i] == 0 and predicted_label[i] == 0):
            con_matrix[0][0] += 1
        elif (true_label[i] == 1 and predicted_label[i] == 0):
            con_matrix[1][0] += 1
            mismatched.append(i)
        elif (true_label[i] == 0 and predicted_label[i] == 1):
            con_matrix[0][1] += 1
            mismatched.append(i)
        elif (true_label[i] == 1 and predicted_label[i] == 1):
            con_matrix[1][1] += 1

    return con_matrix, mismatched

# Given a corpus of text, evaluate the various methods
def evaluate_corpus(corpus, printWrong, writeInFile, isOnline, threshold, window):

    if (isOnline):

        print "Online System Entered"
        print "Enter 'quit' to exit from the system"

        sentence = raw_input()
        while (sentence != "quit"):

            pos_tag_annotation = pos_tag_dd(sentence,0,window,threshold)
            naive_annotation = naive_dd(sentence,0,window,threshold)

            sentence = raw_input()

    else:
        dataset = make_corpus(corpus)
        pos_tag_prediction = []
        naive_prediction = []
        true_annotation = []

        for data_point in dataset:

            sentence = data_point[0]
            annotation = data_point[1]

            pos_tag_annotation = pos_tag_dd(sentence,0,window,threshold)
            naive_annotation = naive_dd(sentence,0,window,threshold)

            pos_tag_prediction.append(pos_tag_annotation)
            naive_prediction.append(naive_annotation)
            true_annotation.append(annotation)

        pos_con_matrix, pos_mismatch = make_confusion_matrix(true_annotation,pos_tag_prediction)
        naive_con_matrix, naive_mismatch = make_confusion_matrix(true_annotation,naive_prediction)

        if (writeInFile):
            f1 = open("POS_Results.csv",'a')
            f1.write(str(threshold) + ',' + str(pos_con_matrix[0][0]) + ',' + str(pos_con_matrix[0][1]) + ',' + str(pos_con_matrix[1][0]) + ',' + str(pos_con_matrix[1][1]) + "\n")
            f1.close()
            f2 = open("Naive_Results.csv",'a')
            f2.write(str(threshold) + ',' + str(naive_con_matrix[0][0]) + ',' + str(naive_con_matrix[0][1]) + ',' + str(naive_con_matrix[1][0]) + ',' + str(naive_con_matrix[1][1]) + "\n")
            f2.close()
        else:
            print ("Results:\n------------------------------------")
            print "POS TAG DD - "
            print pos_con_matrix
            print "----------------"
            print "NAIVE DD - "
            print naive_con_matrix

        if (printWrong):

            print "\nPOS MISMATCH\n--------------------------\n"
            for i in pos_mismatch:
                print dataset[i][0] + "|" + str(dataset[i][1])

            print "\nNAIVE MISMATCH\n--------------------------\n"
            for i in naive_mismatch:
                print dataset[i][0] + "|" + str(dataset[i][1])

############################################################################

# for i in range(20):
    # evaluate_corpus("camera_reviews_corpus.txt",1,0,5*float(i)/100)
evaluate_corpus("camera_reviews_corpus.txt",1,0,0,0.15,5)
