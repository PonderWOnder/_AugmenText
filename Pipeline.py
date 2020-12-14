# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 10:13:25 2020

@author: Konstantin Avramidis
"""


from sys import stdout
from Operations import *
#from Utilities import *

class Pipes():
    
    def __init__(self,files=None):
        self.text=self.get_text(files=files)
        self.pipeline=self.clear()
        #self.lex=lexicon()
    
    
    def get_text(self,rand=True,files=None):
        '''
        
        :returns: string from files provided in location files
        '''
        try:
            if not hasattr(self, 'text'):
                return self.file_obj.import_text(rand)
            else:
                self.text=self.file_obj.import_text(rand)
        except:
            self.file_obj=load_files(files)
            if not hasattr(self, 'text'):
                return self.file_obj.import_text(rand)
            else:
                self.text=self.file_obj.import_text(rand)
    
    def clear(self):
        if not hasattr(self, 'pipeline'):
            return []
        else:
            self.pipeline=[]
       
    
    
    def run(self):
        '''
        
        executes all functions within the pipeline list

        '''
        text=self.text
        stdout.write(text[:100]+'\n\n')
        #self.pipeline=[for op in self.pipeline]
        for x,operation in enumerate(self.pipeline):
            print(str(x)+': '+str(operation)+'\n')
            # if callable(operation)==True:
            #     print('x')
            text=operation.perform_operation(text)
            stdout.write(text[:100]+'\n')
            text=self.text
            
    
    def random_operations(self):
        '''
        adds an random entry from the Operation class to the pipeline list

        :yields: random function within the Operation class

        '''
        try:
            self.pipeline.append(self.ops[random.randint(0,len(self.ops)-1)]())
        except:
            self.ops=[cls for cls in Operation.__subclasses__()]
            self.pipeline.append(self.ops[random.randint(0,len(self.ops)-1)]())
    
    
    def random_typo(self,p=None):
        self.pipeline.append(RandomTypo(p))
            
    def syn_ant(self,ant=False):
        self.pipeline.append(Syn_checker(ant))
         
    def stem(self):
        self.pipeline.append(Stemmenizer())
    
    def vectorize(self):
        self.pipeline.append(Vector())
        
    def keydist_typo(self,p):
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(KeyDistTypo(p))

    def letter_flip(self,p):
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(LetterFlip(p))


    def letter_skip(self,p):
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(LetterSkip(p))


    def double_letter(self,p):
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(DoubleLetter(p))


    def space_inserter(self,p):
        if not 0 < p <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        else:
            self.pipeline.append(SpaceInserter(p))
    
    def _auto(self):
        while True:
            self.get_text()
            for i in range(0,random.randint(1,5)):
                self.random_operations()
            self.run()
            self.clear()
