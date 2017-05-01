import gensim

model = gensim.models.Word2Vec.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
model.save("Google_Word2Vec_Model")
