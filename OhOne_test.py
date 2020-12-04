# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:37:08 2020

@author: 'Schmatz, Pasic, Braun, Avramidis'
E-Mail: 'ds181019,ds182001,ds181026,ds181009@fhstp.ac.at'
"""

import os
from sys import stdout
from functools import reduce
from loader import aug_loader
from word_functions import spell_mistake
        
class augmentor(spell_mistake,aug_loader):
    
    def __init__(self, files=None,tokens=None):
        spell_mistake.__init__(self)
        aug_loader.__init__(self)
        
        self.somepath=files
        self.run()
        if type(tokens)==type(None):
            self.get_fresh_tokens()
        self.buffer=[]
            
    def get_fresh_tokens(self,pos=0,word=True):
        self.start=[self.bib[key][word] for key in self.bib][pos]
        self.token_list=self.start
        return 
    
    def one_long_one(self):
        self.token_list=reduce(lambda a,b:a+b,[self.bib[key][1] for key in self.bib])
        return
    
    def save_transformed_list(self):
        self.add_words(self.token_list)
        self.buffer.append(self.token_list)
        return 
    
    def return_vectors(self):
        [stdout.write(str(self.find_it(i))+',') for i in self.token_list]
        return 
    
    def __str__(self):
        return 'There are '+str(len(self.bib))+' Texts in Corpus\n'+ \
                'Current word count is '+ str(len(self.token_list))+ \
                '\nNumber of applied transformations is : '+ \
                str(sum([True for i,x in enumerate(self.token_list) if self.start[i]!=x]))

if __name__ == "__main__":
    liste=[os.path.abspath(''),
            'https://medium.com/@justinboylantoomey/fast-text-extraction-with-python-and-tika-41ac34b0fe61',
            'https://en.wikipedia.org/wiki/Tokenization_(lexical_analysis)']
    sometest=augmentor(liste)


