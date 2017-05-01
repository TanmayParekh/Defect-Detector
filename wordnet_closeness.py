from similarity import getSimilarityScore
from nltk.corpus import wordnet as wn

def closeness(word,defect_list):

	word_ss_list = wn.synsets(word)
	max_defect_sim_score = 0
	closest_defect = 'None'

	for defect in defect_list:
		list_sim_scores = getSimilarityScore(word, defect)
		
		if len(list_sim_scores) == 0:
			continue

		if max(list_sim_scores) > max_defect_sim_score:
			max_defect_sim_score = max(list_sim_scores)
			closest_defect = defect

	return max_defect_sim_score, closest_defect