# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 14:24:23 2020

@author: GROKA
"""

import random
import os
from json import load
from hashlib import md5

class load_files():
    def __init__(self, files):
        self.input=os.path.abspath(files)
        self.files_list=self.load_text_loc()
        self.iter=0
        
        
    def load_text_loc(self):
        try:
           return [os.path.join(self.input,i) for i in os.listdir(self.input) if '.txt' in i]
        except:
            self.files=input("Please provide Input directory: ")
            self.load_text_loc()
            
    def import_text(self,rand=True):
        if rand==True:
            location=self.files_list[random.randint(0, len(self.files_list)-1)]
            txt=open(location,'rb')
            inter=txt.read().decode('utf8','ignore')
            txt.close()
            return inter
        else:
            location=self.files_list[self.iter]
            txt=open(location,'rb')
            inter=txt.read().decode('utf8','ignore')
            txt.close()
            self.iter+=1
            if self.iter>=len(self.files_list):
                self.iter=0
            return inter
            

class lexicon():
    def __init__(self):
        self.dictionary=self._load_dict()
        
        
    def _load_dict(self,location='ouput.new'):
        '''        
        :param location: The default is 'output.new'
        :type location: String
        :return: None
        '''
        
        try:
            location=os.path.abspath(location)
            with open(location, "r") as fp:
                self.dictionary=[list(map(
                    lambda i:tuple(i) if type(i)==list and 
                    len(i)==2 and 
                    str in [type(q) for q in i] else i,x)) for x in load(fp)]
        except:
            print('Can\'t find .new file @ '+location,end=' ')
            location=input('Please specify location: ')
            self._load_dict(location)

    
    def word_it(self,word):
        '''
        Standardizes strings for hashing. Drops . , on the and for example.
        
        :param word: Single tokenized word to be standardized.
        :type word: String
        :return: Dropped everything on the end of the word that is in 
                 self.sings string.
        '''
        
        if len(word)>1:    
            while True:
                if word[-1] in self.signs and len(word)>1: #not good for dosages
                    word=word[:-1]
                else:
                    break
        return word.lower()
    
    
    def hash_it(self,word):
        '''
        Standardizes and numerically hashes string that resembles a word, 
        sentence or paragraph although word would be preferable.
        
        :param word: Unaltered string most likly from the tokenizer.
        :type word: String
        :return: Numerical hash representation of to provided string in 
                 integer.
        '''
        
        return int(md5(str.encode(self.word_it(word))).hexdigest(),16)%self.dict_size
    
    
    def is_it_in_yet(self,word):
        '''
        Checks if word is already in self.dictionary and returns its position 
        also considering hash collissions if word is already in dic
        
        :param word: Some unaltered word
        :type word: String
        :return: True if word returns true if word is in self.dictionary in 
                 string
        '''
        
        word=self.word_it(word)
        pos=self.hash_it(word)
        loc=self.dictionary[pos]
        if word in loc:
            return True ,pos  
        elif len(loc)>1:
            in_yet=False
            for stuff in loc:
                if type(stuff)==tuple: 
                    if word in stuff:
                        in_yet=True
                        pos=stuff[1]
                        break
            return in_yet, pos
        else:
            return False, pos  


    def find_it(self,word):
        '''
        Takes string and checks if it is in lexikon
        
        :param word: Unaltered string most likly from the tokenizer.
        :type word: String
        :return: Numerical hash representation of to provided or Failure string
                 if word is not in lexikon
        '''
        tf,pos=self.is_it_in_yet(word)
        return pos if tf==True else 'Failure'   