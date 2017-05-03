# from nltk.parse.stanford import StanfordDependencyParser
# from nltk import word_tokenize
# import os

# # export CLASSPATH=/home/tanmay/Desktop/RnD/Standord_Parser/stanford-parser-python-r22186/ThirdParty/stanford-parser/englishPCFG.ser.gz

# # jar = '/home/tanmay/Desktop/RnD/Parser_new/stanford-parser-full-2016-10-31/stanford-parser.jar'
# # model = '/home/tanmay/Desktop/RnD/Parser_new/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser'

# dep_parser=StanfordDependencyParser(model_path="/home/tanmay/Desktop/RnD/Standord_Parser/stanford-parser-python-r22186/3rdParty/stanford-parser/englishPCFG.ser.gz")
# # dep_parser = StanfordDependencyParser(model, jar, encoding='utf8')

# print [parse.tree() for parse in dep_parser.raw_parse("The quick brown fox jumps over the lazy dog.")]

import re
import networkx as nx
from practnlptools.tools import Annotator

neg_words = ["no","not","'t","neither","none","never"]

def check_neg(text,keyword):

    annotator = Annotator()
    dep_parse = annotator.getAnnotations(text, dep_parse=True)['dep_parse']

    dp_list = dep_parse.split('\n')
    pattern = re.compile(r'.+?\((.+?), (.+?)\)')

    edges = []
    for dep in dp_list:
        m = pattern.search(dep)
        word1 = m.group(1).split('-')[0]
        word2 = m.group(2).split('-')[0]
        # print word1, word2
        if (word1 == keyword and word2 in neg_words) or (word1 in neg_words and word2 == keyword):
             return 1

    return 0

# print check_neg("The pictures are not blurry","blurry")
