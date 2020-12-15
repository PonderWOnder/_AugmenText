# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 15:42:24 2020

@author: Andreas Braun
"""

import random
import string
import re
from nltk.tokenize import word_tokenize, sent_tokenize 
from Utilities import *

class Operation(object):
    
    def __init__(self,p=0.01,lex=lexicon()):
        self.p = p
        self.lex=lex
    
        
    def __str__(self):
        return self.__class__.__name__
    
    def perform_operation(self,text):
        raise RuntimeError('You cannot call base class.')
        

def nltk_split_text(text, to_words = True):
    if to_words == True:
        sep = word_tokenize(text)
    else:
        sep = sent_tokenize(text)
    return sep


def back_to_text(tokens):
    befor=['[','{','(']
    after=['.',',',':',';',')',']','}']
    neither_nor=['\'','\"',' ']
    res = "".join(i if tokens[pos+1 if pos<len(tokens)-1 else pos] in after or i in befor else i+' ' for pos,i in enumerate(tokens))
    return res
    

        
class RandomTypo(Operation):
    
    def __init__(self, p=None):
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        letters = string.ascii_lowercase
        token_list = nltk_split_text(text, to_words = True)
        final_list = []
        for token in token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < self.p:
                    if letter.isupper():  #optional: with all_chars
                        letter = letters[random.randint(0,len(letters)-1)].upper()
                    else:
                        letter = letters[random.randint(0,len(letters)-1)]         
                word_list.append(letter)
                new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text
    

class LetterSkip(Operation):
    
    def __init__(self, p=None):
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < self.p:
                    letter = ''
                word_list.append(letter)
                new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text
        
    
class LetterFlip(Operation):
    
    def __init__(self, p=None):
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = list(token)
            if len(word_list) > 2:
                if random.uniform(0,1) < self.p:
                    idx = random.randint(1,len(word_list)-1)
                    word_list[idx], word_list[idx-1] = word_list[idx-1], word_list[idx]
            new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text
    
    
class SpaceInserter(Operation):
    
    def __init__(self, p=None):
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < self.p:
                    letter = letter + ' '
                word_list.append(letter)
                string_word = ''.join(word_list)
            final_list.append(string_word)
        altered_text = back_to_text(final_list)
        return altered_text
    

class DoubleLetter(Operation):
    
    def __init__(self, p=None):
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        
    def perform_operation(self, text):
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = []
            for letter in token:
                if random.uniform(0,1) < self.p:
                    letter = 2*letter
                word_list.append(letter)
            new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text


class Syn_checker(Operation):
    
    def __init__(self,ant=False, lex=None):
        if lex==None:
            Operation.__init__(self,lex)
            if self.lex==None: self.lex=lexicon()
        else:
            self.lex=lex
        self.ant=ant
            
    def perform_operation(self,text):
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            try:
                if list in [type(x) for x in self.lex[token]]:
                    for num,i in enumerate(self.lex[token]):
                        if type(i)==list:
                            if i[self.ant]==[]:
                                final_list.append(token)
                                break
                            per=100
                            pos_per=random.randint(1,per)
                            base=len(i[self.ant])
                            which_one=int(round((base**(1/per))**pos_per,0))-1
                            final_list.append(self.lex[i[self.ant][which_one]][0])
                            break
                else:
                    final_list.append(token)
            except:
                final_list.append(token)
        altered_text = back_to_text(final_list)
        return altered_text


class Stemmenizer(Operation):
    
    def __init__(self, lex=None):
        if lex==None:
            Operation.__init__(self,lex)
            if self.lex==None: self.lex=lexicon()
        else:
            self.lex=lex
                
    def perform_operation(self, text):
        final_list=[]
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            x=1
            if len(token)<4:
                final_list.append(token)
                continue
            while True:
                pos=int(-1*x)                
                if None==self.lex[token[:pos]]:
                    x+=1
                    if len(token)-1==x:
                        break
                else:
                    final_list.append(self.lex[token[:pos]][0])
                    break
        altered_text = back_to_text(final_list)
        return altered_text  


class Vector(Operation):
    
    def __init__(self, lex=None):
        if lex==None:
            Operation.__init__(self,lex)
            if self.lex==None: self.lex=lexicon()
        else:
            self.lex=lex

    def perform_operation(self, text):
        final_list=[]
        token_list = nltk_split_text(text, to_words = True)
        if not hasattr(self, 'vec_pos'):
            self.vec_pos=0
        output=[]
        for word in token_list:
            tf,pos=self.lex.is_it_in_yet(word)
            if tf == True:
               if True==any([True for i in self.lex[pos] if type(i)==int]):
                   pos_return=[i for i in self.lex[pos] if type(i)==int][0]
                   output.append((pos_return,word))
               else:
                   self.lex[pos].append(self.vec_pos)
                   pos_return=self.vec_pos
                   self.vec_pos+=1
                   output.append((pos_return,word))
               
        return str(output)
    

class KeyDistTypo(Operation):
   
    def __init__(self, p=None):
        if p==None:
            Operation.__init__(self,p)
            if self.p==None: self.p=0.01
        else:
            self.p=p
        self.keyboard_positions_lower = {
            '`' : (-1,0),
            '1' : (0, 0),
            '2' : (1, 0),
            '3' : (2, 0),
            '4' : (3, 0),
            '5' : (4, 0),
            '6' : (5, 0),
            '7' : (6, 0),
            '8' : (7, 0),
            '9' : (8, 0),
            '0' : (9, 0),
            '-' : (10,0),
            '=' : (11,0),
          
            'q' : (0, 1),
            'w' : (1, 1),
            'e' : (2, 1),
            'r' : (3, 1),
            't' : (4, 1),
            'y' : (5, 1),
            'u' : (6, 1),
            'i' : (7, 1),
            'o' : (8, 1),
            'p' : (9, 1),
            '[' : (10,1),
            ']' : (11,1),
            '\\': (12,1),
          
            'a' : (0, 2),
            's' : (1, 2),
            'd' : (2, 2),
            'f' : (3, 2),
            'g' : (4, 2),
            'h' : (5, 2),
            'j' : (6, 2),
            'k' : (7, 2),
            'l' : (8, 2),
            ';' : (9, 2),
            "'" : (10,2),
           
           
            'z' : (0, 3),
            'x' : (1, 3),
            'c' : (2, 3),
            'v' : (3, 3),
            'b' : (4, 3),
            'n' : (5, 3),
            'm' : (6, 3),
            ',' : (7, 3),
            '.' : (8, 3),
            '/' : (9, 3),
          
            ' ' : (5, 4)
            }
          
        self.keyboard_positions_upper = {
            '~' : (-1,0),
            '!' : (0, 0),
            '@' : (1, 0),
            '#' : (2, 0),
            '$' : (3, 0),
            '%' : (4, 0),
            '^' : (5, 0),
            '&' : (6, 0),
            '*' : (7, 0),
            '(' : (8, 0),
            ')' : (9, 0),
            '_' : (10,0),
            '+' : (11,0),
           
            'Q' : (0, 1),
            'W' : (1, 1),
            'E' : (2, 1),
            'R' : (3, 1),
            'T' : (4, 1),
            'Y' : (5, 1),
            'U' : (6, 1),
            'I' : (7, 1),
            'O' : (8, 1),
            'P' : (9, 1),
            '{' : (10,1),
            '}' : (11,1),
            '|' : (12,1),
           
            'A' : (0, 2),
            'S' : (1, 2),
            'D' : (2, 2),
            'F' : (3, 2),
            'G' : (4, 2),
            'H' : (5, 2),
            'J' : (6, 2),
            'K' : (7, 2),
            'L' : (8, 2),
            ':' : (9, 2),
            '"' : (10,2),
           
            'Z' : (0, 3),
            'X' : (1, 3),
            'C' : (2, 3),
            'V' : (3, 3),
            'B' : (4, 3),
            'N' : (5, 3),
            'M' : (6, 3),
            '<' : (7, 3),
            '>' : (8, 3),
            '?' : (9, 3),
           
            ' ' : (5, 4)
            }
       
    def calculate_distance(self,x1, y1, x2, y2):
        xdist = x2-x1
        ydist = y2-y1
        return (xdist**2 + ydist**2)**0.5
   
    def calculating_probs(self,key):
        sum_inverse_dists = 0
        inverse_dists = {}
        if key in self.keyboard_positions_lower:
            keyboard_positions = self.keyboard_positions_lower
        else:
            keyboard_positions = self.keyboard_positions_upper
        posx, posy = keyboard_positions[key]
        for letter in keyboard_positions: 
            if letter != key:
                posx1, posy1 = keyboard_positions[letter]
                dist = self.calculate_distance(posx, posy, posx1, posy1)
                inverse_dist = 1/(dist**6)
                inverse_dists[letter] = inverse_dist
                sum_inverse_dists += inverse_dist
        probs = {}
        for key, value in inverse_dists.items():
            probs[key] = value/sum_inverse_dists
        return probs
   
    def pick_random_letter(self,prob_dist):
        letters = []
        probs = []
        for key, value in prob_dist.items():
            letters.append(key)
            probs.append(value)
        picked_letter = random.choices(letters, probs)
        return picked_letter[0]
       
    def perform_operation(self, text):
        key_list=list(self.keyboard_positions_lower.keys())+list(self.keyboard_positions_upper.keys())
        final_list = []
        token_list = nltk_split_text(text, to_words = True)
        for token in token_list:
            word_list = []
            for letter in token:
                if letter not in key_list:
                    continue
                if random.uniform(0,1) < self.p:
                    neighbour_probs = self.calculating_probs(letter)
                    letter = self.pick_random_letter(neighbour_probs)
                word_list.append(letter)
            new_word = ''.join(word_list)
            final_list.append(new_word)
        altered_text = back_to_text(final_list)
        return altered_text
    
# debug the back to text function (brackets)
# Check if the letter is in the "correct" signs (no @ for example)
# clear_pipe    
    



    