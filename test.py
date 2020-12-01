# -*- coding: utf-8 -*-

import os
from OhOne import aug_input, aug_loader
from Augmentext_Functions import spell_mistake

if __name__ == "__main__":
    liste=[os.path.abspath(''),
           'https://medium.com/@justinboylantoomey/fast-text-extraction-with-python-and-tika-41ac34b0fe61',
           'https://en.wikipedia.org/wiki/Tokenization_(lexical_analysis)']
    sometest=aug_input(liste)


