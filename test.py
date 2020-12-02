# -*- coding: utf-8 -*-

import os
from OhOne import aug_loader
from Augmentext_Functions import spell_mistake
        
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


