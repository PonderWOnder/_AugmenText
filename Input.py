# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 11:44:56 2020

@author: GROKA
"""

from OhOne import aug_loader as al



class aug_input:
    
    def __init__(self, files):
        inst=al(files)
        inst.run()
        self.bib=inst.bib
        self.dictionary=inst.dictionary
        
    
    