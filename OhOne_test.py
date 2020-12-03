# -*- coding: utf-8 -*-

import os
from sys import stdout
from OhOne import aug_loader
from Augmentext_Functions import spell_mistake
        
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
        self.token_list=[self.bib[key][word] for key in self.bib][pos]
        return 
    
    def one_long_one(self):
        from functools import reduce
        self.token_list=reduce(lambda a,b:a+b,[self.bib[key][1] for key in self.bib])
        return
    
    def save_transformed_list(self):
        self.buffer.append(self.token_list)
        return 
    
    def return_vectors(self):
        [stdout.write(str(self.find_it(i))+',') for i in self.token_list]
        return 

if __name__ == "__main__":
    liste=[os.path.abspath(''),
            'https://medium.com/@justinboylantoomey/fast-text-extraction-with-python-and-tika-41ac34b0fe61',
            'https://en.wikipedia.org/wiki/Tokenization_(lexical_analysis)']
    sometest=augmentor(liste)


