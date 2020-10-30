# -*- coding: utf-8 -*-

from OhOne import augmentext

if __name__ == "__main__":
    liste=['F:\Desktop\\_AugmenText']
    sometest=augmentext(liste)
    sometest.run()
    print(sometest.dictionary[hash('like'.lower())%10**6])
    sometest.add_words(sometest.bib[sometest.hash_it(sometest.somepath[0])][1])
