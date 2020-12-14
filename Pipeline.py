# -*- coding: utf-8 -*-
"""
@author: Avramidis, Braun, Pasic
"""


from Operations import *
from Utilities import *

class Pipeline():
    '''
    The class :class: pipeline provides the interface for the user to interact
    with different objects in module Operations
    '''
    
    def __init__(self,files=None):
        '''
        Create a new Pipeline object pointing to the directory.
        '''
        self.text=self.get_text(files=files)
        self.pipeline=[]
    
    
    def get_text(self,rand=True,files=None):
        '''
        :param rand: If true ,loads a random file from directory. IF false
                     loads first time from directory.
        :type rand: Boolean
        :param files: String pointing to the directory where the files are.
        :type files: If None subroutine is called that ask user to provide 
                     directory. Else String
        :returns: String from files provided in location files
        '''
        try:
            return self.file_obj.import_text(rand)
        except:
            self.file_obj=load_files(files)
            return self.file_obj.import_text(rand)
    
    
    def run(self):
        '''
        Executes all functions within the pipeline list
        '''
        text=self.text
        for operation in self.pipeline:
            if callable(operation)==True:
                text=operation(.01).perform_operation(text)
        print(text)
            
    
    def random_operations(self):
        '''
        Adds an random entry from the Operation class to the pipeline list

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

