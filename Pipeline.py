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
            self.text=self.file_obj.import_text(rand)
    
    def run(self):
        text=self.text
        for func in self.pipeline:
            func
        return text
            
    def random_operations(self):
        ops=[cls]