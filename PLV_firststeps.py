# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 02:08:39 2020

@author: benip
"""

import nltk

text = """Hey my Name is Benjamin 
and I'm trying my
first steps with text augmentation"""

print(text)
print("-------------")
                                   #TOKENIZE
import re                          # Regular expression operations
pattern = re.compile("\n")         #Überall wo neue Zeile, setze ein "," -> spliten
print(pattern.split(text))
print("-------------")

pattern2 = re.compile ("\W")       #\W all this kind of characters which are not alphanumeric and split text at all this postitions
print(pattern2.split(text))        # hier auch leerer Strings dabei. Lösung:
print("-------------")

print(list(filter(lambda x: x!='' , pattern2.split(text))))     #returns true if the element that passint is not an empty string
print("-------------")

pattern3 = re.compile ("\W")
print(pattern3.split(text, maxsplit = 3)) # die ersten drei in ein extriges string

print("--------------------------------------------")



import regex
regex.split("[\s\.\,]", text)              #space, "." und ","
print(regex.split("[\s\.\,]", text))

print("....................")

#import nltk
#nltk.download('punkt')
print(nltk.word_tokenize(text))           #unterscheidet zwischen I'm und i am


print("--------------------------------------------")
print("--------------------------------------------")
from nltk.stem import PorterStemmer       #STEMMER
stemmer = PorterStemmer()
plurals = ['buses', 'wishes','babies','women']

for w in plurals:
    print(w, ":", stemmer.stem(w))
    
from nltk.stem.snowball import SnowballStemmer
SnowballStemmer.languages                   #supportet verschiene Sprachen
print(SnowballStemmer.languages)
print("-------------------------------")

lang_stemmer = SnowballStemmer("english")
print(lang_stemmer.stem("generously"))
print(stemmer.stem("generously"))           #Snowball Stemmer better but similar to PorterStemmer

print("--------------------------------------------")
print("--------------------------------------------")

#import nltk
#nltk.download("wordnet")
from nltk.stem import WordNetLemmatizer     #LEMMATIZER
lemmatizer = WordNetLemmatizer()

for w in plurals:
    print(w,":", lemmatizer.lemmatize(w))


