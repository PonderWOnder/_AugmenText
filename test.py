# -*- coding: utf-8 -*-

from OhOne import augmentext

if __name__ == "__main__":
    liste=['F:\Desktop\\_AugmenText',
           'https://medium.com/@justinboylantoomey/fast-text-extraction-with-python-and-tika-41ac34b0fe61',
           'https://en.wikipedia.org/wiki/Tokenization_(lexical_analysis)']
    sometest=augmentext(liste)
    sometest.run()
    for item in sometest.bib:
        sometest.add_words(sometest.bib[item][1])

