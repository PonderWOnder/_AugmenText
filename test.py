# -*- coding: utf-8 -*-

from OhOne import augmentext

if __name__ == "__main__":
    liste=['F:\Desktop\\_AugmenText','https://de.wikipedia.org/wiki/Tokenizer',
           'https://en.wikipedia.org/wiki/Tokenization_(lexical_analysis)']
    sometest=augmentext(liste)
    sometest.run()
    for item in sometest.bib:
        sometest.add_words(sometest.bib[item][1])

