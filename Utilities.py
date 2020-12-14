# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 14:24:23 2020

@author: GROKA
"""
import multiprocessing as mp
import random
import os
from json import load
from hashlib import md5

class load_files():
    '''
    The class :class:`load_files` is meant to load files within the Pipeline module.
    '''
    def __init__(self, files):
        '''
        Initializes subroutine that produces an outputable file-list
        
        :param files: File-list
        :type files: String
        '''
        self.input=files
        self.files_list=self.load_text_loc()
        self.iter=0
        
        
    def load_text_loc(self):
        '''
        Subroutine that produces file-list
        
        :return: File-list 
        '''
        try:
            self.input=os.path.abspath(self.input)
            within=os.listdir(self.input)
            return [os.path.join(self.input,i) for i in within if '.txt' in i]
        except:
            self.input=input("Please provide Input directory: ")
            return self.load_text_loc()
            
    def import_text(self,rand=True):
        '''
        Imports text that file-list points to.
        
        :param rand: Decides if files are loaded randomly or in order provided
                     in directory.
        :type rand: Boolean
        :return: String of text present in file location.
        '''
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
    '''
    The class :class:`lexicon` is a Wrapper for groundthrough dictionary-list
    for accelerate interaction with said list 
    '''
    
    def __init__(self):
        '''
        Calls subroutine _load_dict.
        '''
        self._load_dict()
        self.dict_size=len(self.dictionary)
    
    def __getitem__(self, value):
        '''
        Python routine to interact.
        
        :param value: Search request for dictionary-entry.
        
        :type value: Integer or String
        '''
        if type(value)==int:
            try:
                return self.dictionary[value]
            except:
                print(value,'exceeds lexicon size')
        elif type(value)==str:
            try:
                return self.dictionary[self.find_it(value)]
            except:
                print(value,'not yet in lexicon')
        elif type(value)==slice:
            try:
                return self.dictionary[value]
            except:
                print(value,'exceeds lexicon size')
                
    def add(self,data):
        '''
        Adds entry into dictionary
        :param data: Data to add in String
        :type data: String
        '''        
        try:
            self.add_words(data)
        except:
            print('something went wrong')
        
            
        
    def _load_dict(self,location='ouput.new'):
        '''
        Loads cson file into memory and corrects list including position to
        tuples.        
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
        Standardizes strings for hashing. Drops . , on the end for example.
        
        :param word: Single tokenized word to be standardized.
        :type word: String
        :return: Dropped everything on the end of the word that is in 
                 self.sings string.
        '''
        signs=[' ','.',',','-',':',')']
        if len(word)>1:    
            while True:
                if word[-1] in signs and len(word)>1: #not good for dosages
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
    
    def add_words(self,word,occurrence=0,mc=False):
        '''
        Adds tokens to the dictionary either counting their appearence or not. 
        For larger corpus (10**6) it switches in threaded mode
        
        :param word: input.
        :type liste: List
        :param occurence: The default is 0. Deprecated will be removed in 
                          later versions.
        :type occurence: Integer
        :yields: Postition string pairs to be added into self.dictionary at 
                 position
        '''
        
        if str==type(word):
            liste=[word]
        seg_length=100000
        if len(liste)>seg_length and mc==False:
            self.num_segs=mp.cpu_count()
            if type(self.dictionary)!=type(mp.Manager().list()):
                self.dictionary=mp.Manager().list(self.dictionary)
            stepsize=int(len(liste)/self.num_segs)
            stuff_todo=[]
            for x,i in enumerate(range(0,len(liste),stepsize)):
                if x==self.num_segs:
                    stepsize=(len(liste)%i)-1                    
                
                stuff_todo.append([self.add_words,(liste[i:i+stepsize],occurrence,True)])
            self.multi_proc(stuff_todo)
            self.dictionary=list(self.dictionary)
        else:
            for i in liste:
                try:
                    i=self.word_it(i)
                except:
                    continue
                if i=='':#this is a hack to avoid empty strings
                    continue
                if ord(max(i))>122 or ord(min(i))<97:
                    self._word_asstimator(i)
                    if len([let for let in i if let not in self.lower_letters])>1 or len(i)>45:#45 is the longest english word according to wikipedia or more special characters
                        continue
                in_yet, target=self.is_it_in_yet(i)
                if in_yet==True:
                    to_list=self.dictionary[target]
                    if int in [type(in_list) for in_list in to_list]:
                        for pos, val in enumerate(to_list):#predefining structur would be very helpful to keep checking overhead in bay
                            if type(val)==int:
                                to_list[pos]+=occurrence
                                self.vector_size+=occurrence
                                break
                    else:
                        if occurrence>0:
                            to_list.append(occurrence)
                            self.vector_size+=1
                        
                    self.dictionary[target]=to_list
                    continue#stdout.write('\r'+i+' is already in dictionary at position '+str(target)+'\n')
                else:
                    # if type(self.dictionary)==type(mp.Manager().list()):
                    #     self.lock.acquire()
                    try:
                        if target<self.dict_size/2:
                            for k in range(target,self.dict_size-1):
                                if self.dictionary[k]==[]:
                                    if k!=target:
                                        to_list=self.dictionary[target]
                                        to_list.append((i,k))
                                        self.dictionary[target]=to_list 
                                    to_list=self.dictionary[k]
                                    to_list.append(i)
                                    if occurrence>0:
                                        to_list.append(occurrence)
                                        self.vector_size+=occurrence
                                    self.dictionary[k]=to_list#over complicated by multiprocessing.managers.ListProxy
                                    #stdout.write('\r'+i+' added at Position '+str(k)+'\n')
                                    break
                        else:
                            for k in range(target,-1,-1):
                                if self.dictionary[k]==[]:
                                    if k!=target:
                                        to_list=self.dictionary[target]
                                        to_list.append((i,k))
                                        self.dictionary[target]=to_list 
                                    to_list=self.dictionary[k]
                                    to_list.append(i)
                                    if occurrence>0:
                                        to_list.append(occurrence)
                                        self.vector_size+=occurrence
                                    self.dictionary[k]=to_list#over complicated by multiprocessing.managers.ListProxy
                                    #stdout.write('\r'+i+' added at Position '+str(k)+'\n')
                                    break 
                    except:
                        self.dictionary.append([i])
                        if occurrence>0:
                            self.dictionary[len(self.dictionary)-1].append(occurrence)
                        pos=len(self.dictionary)-1
                        to_list=self.dictionary[target]
                        to_list.append((i,pos))
                        self.dictionary[target]=to_list
                        #stdout.write('\r'+i+' added at Position '+str(pos)+'\n')# if there are no open positiones anymore
                    # if type(self.dictionary)==type(mp.Manager().list()):   
                    #     self.lock.release()