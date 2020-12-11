# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 10:13:25 2020

@author: GROKA
"""


from Operations import *
from Utilities import *

class Pipeline():
    
    def __init__(self,files=None):
        self.text=self.get_text(files)
        self.pipeline=[]
    
    
    def get_text(self,files,rand=True):
        try:
            return self.file_obj.import_text(rand)
        except:
            self.file_obj=load_files(files)
            return self.file_obj.import_text(rand)
    
    
    def run(self):
        text=self.text
        for operation in self.pipeline:
            operation(.01).perform_operation(text)
        print(text)
            
    
    def random_operations(self):
        try:
            self.pipeline.append(self.ops[random.randint(0,len(self.ops)-1)])
        except:
            self.ops=[cls for cls in Operation.__subclasses__()]
            self.pipeline.append(self.ops[random.randint(0,len(self.ops)-1)])
            
    
    def random_typo(p = 0.01):
        if not 0 < probability <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        elif word_distance <= 0:
            raise ValueError("The word distance must be graster than 1.")
        elif not isinstance(word_distance, int):
            raise TypeError("Word distance must be an integer.")
        else:
            self.pipeline.append(RandomTypo(p = p))
    
    
    def random_typo(p = 0.01):
        if not 0 < probability <= 1:
            raise ValueError("Probability must be between 0 and 1.")
        elif not isinstance(word_distance, int):
            raise TypeError("Word distance must be an integer.")
        else:
            self.pipeline.append(RandomTypo(p = p))