# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 10:13:25 2020

@author: Konstantin Avramidis
"""


from Operations import *
from Utilities import *

class Pipeline():
    
    def __init__(self,files=None):
        self.text=self.get_text(files=files)
        self.pipeline=[]
    
    
    def get_text(self,rand=True,files=None):
        '''
        
        :returns: string from files provided in location files
        '''
        try:
            return self.file_obj.import_text(rand)
        except:
            self.file_obj=load_files(files)
            return self.file_obj.import_text(rand)
    
    
    def run(self):
        '''
        
        executes all functions within the pipeline list

        '''
        text=self.text
        for operation in self.pipeline:
            if callable(operation)==True:
                text=operation(.01).perform_operation(text)
        print(text)
            
    
    def random_operations(self):
        '''
        adds an random entry from the Operation class to the pipeline list

        :yields: random function within the Operation class

        '''
        try:
            self.pipeline.append(self.ops[random.randint(0,len(self.ops)-1)])
        except:
            self.ops=[cls for cls in Operation.__subclasses__()]
            self.pipeline.append(self.ops[random.randint(0,len(self.ops)-1)])
    
    
    def random_typo(p = 0.01):
        if not 0 < probability <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        elif not isinstance(word_distance, int):
            raise TypeError("Word distance must be an integer.")
        else:
            self.pipeline.append(RandomTypo(p = p))

first_try=Pipeline()
for i in range(5):
    first_try.random_operations()
print(first_try.pipeline)
first_try.run()