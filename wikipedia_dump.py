# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 12:55:22 2020

@author: GROKA
"""
import wikipedia

rec=False
count=0
current_page=''
with open('F://Desktop//enwiki-20201101-pages-articles-multistream.xml',encoding=('utf-8')) as wiki:
    for line in wiki:
        if '<page>' in line:
            rec=True
        if rec==True:
            current_page+=line
        if '</page>' in line:
            rec=False
            if '{{Redirect category shell|1' in current_page:
                current_page=''
            if '[[Category:Wikipedia medicine articles' in current_page:     
                print(current_page)
                count+=1
                current_page=''
        if count==4:
            break