#https://towardsdatascience.com/a-word2vec-implementation-using-numpy-and-python-d256cf0e5f28
#https://towardsdatascience.com/an-implementation-guide-to-word2vec-using-numpy-and-google-sheets-13445eebd281

import os
from loader import aug_loader
from word_functions import spell_mistake
import numpy as np
        
class augmentor(spell_mistake,aug_loader):
    
    def __init__(self, files=None,tokens=None):
        spell_mistake.__init__(self)
        aug_loader.__init__(self)
        
        self.somepath=files
        self.run()
        if type(tokens)==type(None):
            self.token_list=[self.bib[key][1] for key in self.bib][0]

if __name__ == "__main__":
    liste=[os.path.abspath(''),
           'https://medium.com/@justinboylantoomey/fast-text-extraction-with-python-and-tika-41ac34b0fe61',
           'https://en.wikipedia.org/wiki/Tokenization_(lexical_analysis)']
    sometest=augmentor(liste)
    
bib = sometest.bib[list(sometest.bib.keys())[0]]
bib1tokens = bib[1]


def generate_dictionary_data(tokens):
    word_to_index = {}
    index_to_word = {}
    corpus = []
    count = 0
    vocab_size = 0 
    for token in tokens:
        if token != '.' and token != ',':
            token = token.lower()
            corpus.append(token)
            if word_to_index.get(token) == None:
                word_to_index.update({token:count})
                index_to_word.update({count:token})
                count += 1
    vocab_size = len(word_to_index)
    length_of_corpus = len(corpus)   
    return word_to_index, index_to_word, corpus, vocab_size, length_of_corpus
    #word_to_index: keys: words; values: indices
    #index_to_word: keys: indices; values: words
    #corpus: list of tokens
    #vocab_size: amount of different words in the corpus
    #length_of_corpus: amount of total words in the corpus



def get_one_hot_vectors(target_word, context_words, vocab_size, word_to_index):
    trgt_word_vector = np.zeros(vocab_size)
    index_of_word_dictionary = word_to_index.get(target_word)
    trgt_word_vector[index_of_word_dictionary] = 1
    ctxt_word_vector = np.zeros(vocab_size)   
    for word in context_words:
        index_of_word_dictionary = word_to_index.get(word)
        ctxt_word_vector[index_of_word_dictionary] = 1        
    return trgt_word_vector, ctxt_word_vector

word_to_index, index_to_word, corpus, vocab_size, length_of_corpus = generate_dictionary_data(bib1tokens)


def generate_training_data(corpus,window_size,vocab_size,word_to_index,length_of_corpus):
    training_data =  []
    #training_sample_words =  []
    for i,word in enumerate(corpus):
        index_target_word = i
        target_word = word
        context_words = []
        if i == 0:  
            context_words = [corpus[x] for x in range(i + 1 , window_size + 1)] 
        elif i == len(corpus)-1:
            context_words = [corpus[x] for x in range(length_of_corpus - 2 ,length_of_corpus -2 - window_size  , -1 )] #the -1 means backwards
        else:
            before_target_word_index = index_target_word - 1
            for x in range(before_target_word_index, before_target_word_index - window_size , -1): #the -1 means backwards
                if x >=0: #to stay inside the vector
                    context_words.append(corpus[x])
            after_target_word_index = index_target_word + 1
            for x in range(after_target_word_index, after_target_word_index + window_size):
                if x < len(corpus): #to stay inside the vector
                    context_words.append(corpus[x])
        trgt_word_vector,ctxt_word_vector = get_one_hot_vectors(target_word,context_words,vocab_size,word_to_index)
        training_data.append([trgt_word_vector,ctxt_word_vector])   
        
        
    return training_data#,training_sample_words
    #it is a list (every word in the corpus) containing lists containing 2 arrays (one_hot_vectors for a target word and its context words)



training_data = generate_training_data(corpus=corpus, window_size=2, vocab_size=vocab_size, word_to_index=word_to_index, length_of_corpus=length_of_corpus)


def forward_prop(w1, w2, target_word):
    hidden_layer = np.dot(w1.T, target_word)# target is the input vector!!!
    u = np.dot(w2.T, hidden_layer)
    y_predicted = softmax(u)
    return y_predicted, hidden_layer, u

def softmax(x):
    e_x = np.exp(x-np.max(x))
    return e_x/e_x.sum(axis=0)


def train_w2v(lr = 0.01, epochs = 50, hidden_layer_size = 80):    
    w1 = np.random.rand(vocab_size, hidden_layer_size)
    w2 = np.random.rand(hidden_layer_size, vocab_size)
    
    for i in range(epochs):
        for word in training_data:
            target_word = word[0]
            ctxt_words = word[1]
            pred, hidden, u = forward_prop(w1, w2, target_word)
            diff = pred-ctxt_words
            delta_w2 = np.outer(hidden, diff)
            dot_w2_diff = np.dot(w2, diff)
            delta_w1 = np.outer(target_word, dot_w2_diff)
            w1 = w1-(lr*delta_w1)
            w2 = w2-(lr*delta_w2)
    return w1
            
def get_word_vecs():        
    word_vec = {}
    trained_model = train_w2v()
    for word, idx in word_to_index.items():
        vec = trained_model[idx]
        word_vec.update({word:vec})
    return word_vec

def calculate_wordvec_dists():
    wordvecs = get_word_vecs()
    dists = {}    
    for word, vector in wordvecs.items():    
        for _word, _vector in wordvecs.items():
            if word != _word:
                word_pair = [word, _word]
                word_pair = str(sorted(word_pair))
                if dists.get(word_pair) == None:
                    dist = np.linalg.norm(vector - _vector)
                    dists[word_pair] = dist
    return dists

word_dists = calculate_wordvec_dists()