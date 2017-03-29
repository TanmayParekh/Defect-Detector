from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
import sys


def getSimilarityScore(word1,word2):
	word1synsets = wn.synsets(word1)
	word2synsets = wn.synsets(word2)
	synsetname1 = [wn.synset(str(syns.name())) for syns in word1synsets]
	synsetname2 = [wn.synset(str(syns.name())) for syns in word2synsets]
	pathsimlist = []
	for sset1, sset2 in [(sset1,sset2) for sset1 in synsetname1\
	for sset2 in synsetname2]:
		pathsim = sset1.path_similarity(sset2)
		#wupsim = sset1.wup_similarity(sset2)

		pol1=0
		pol2=0
		#print sset1.name()
		sense1 = swn.senti_synset(sset1.name())
		if sense1.pos_score() > sense1.neg_score():
			pol1=1
		else:
			pol1=-1

		sense2 = swn.senti_synset(sset2.name())
		if sense2.pos_score() > sense2.neg_score():
			pol2=1
		else:
			pol2=-1

		if pol1!=pol2:
			return pathsimlist

		if pathsim != None:
			pathsimlist.append(pathsim)
			#print "Path Sim Score: ",pathsim," WUP Sim Score: ",wupsim,\
			#"\t",sseta, "\t", ssetb, "\t", sseta.definition(), "\t", ssetb.definition()

	return pathsimlist

if __name__ == "__main__":
	
	word1 = sys.argv[1]
	word2 = sys.argv[2]
	sim = getSimilarityScore(word1,word2)
	print word1 + " " + word2 + " - "
	print sim