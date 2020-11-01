# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:37:08 2020

@author: GROKA
"""
import os
#import time
import threading as th
import multiprocessing as mp
from urllib.request import urlopen
from bs4 import BeautifulSoup as urlreader 
from sys import stdout

PYTHONHASHSEED=0

class augmentext():
    
    def __init__(self, path_to_text=None,
                 dictionary=None,
                 dict_size=10**6,
                 signs=[' ','.',',','-',':'],
                 list_of_supported_files=['.doc','.pdf','http:','https:','www.','.htm','.txt'],
                 supported_chr=[chr(i) for i in range(32,127)]+['ä','ü','ö','Ä','Ü','Ö']):
        self.somepath=path_to_text
        self.bib={}
        self.dict_size=dict_size
        self.signs=signs
        self.list_of_supported_files=list_of_supported_files
        self.supported_chr=supported_chr
        self.dirctionary=dictionary
        self.count=0
        self.lock=mp.Lock()
     
    def dir_file_or_url(self,location):
        if any(phrase in location for phrase in self.list_of_supported_files):      #very brittle going to be updated
            return [location]
        else:
            try:
                files_there=os.listdir(location)
                usefull_files=[]
                for i in files_there:
                    if any(phrase in i[-4:] for phrase in self.list_of_supported_files):
                        usefull_files.append(location+'\\'+i)
                return usefull_files
            except:
                print('cant find anything usefull at location'+location)
     
    def load_url_text(self,location): #URL
        response=urlopen(location)
        return urlreader(response.read(),'lxml').text
    
    def load_worddoc_text(self,location):
        pass
    
    def load_pdf_text(self,location):
        pass
    
    def load_txt(self,location): #TXT
        txt=open(location,'rb')
        inter=txt.read().decode('utf8','ignore')
        txt.close()
        return inter 

    def split_text(self,text,corpus=3): #Tokenizer
        sep=[' ','.','\n']
        return [text.split(i) for i in sep if i in text]
    
    def drop_stuff(self,text): #
        supp_chr=self.supported_chr
        new_text=[i if i in supp_chr else ' ' for i in text]
        return ''.join(new_text)
    
    def work_through(self):
        for key in self.bib.keys():
            self.bib[key]+=self.split_text(self.bib[key][0])
            print('text '+str(key)+' was seperated')        
    
    def add_to_bib(self, path_list):
        for i in path_list:
            dic_hash=self.hash_it(i)
            
            if any(suffix in i[-4:] for suffix in ['pdf','doc']):
                pass
            
            elif 'txt' in i[-4:]:
                try:
                    self.bib[dic_hash]=[self.drop_stuff(self.load_txt(i))]
                    print('resource '+i+' is now available under '+str(dic_hash))
                except:
                    print('couldn\'t find txt '+i)
                    
            elif any(prefix in i[:4] for prefix in ['http','www']):
                try:
                    self.bib[dic_hash]=[self.drop_stuff(self.load_url_text(i))]
                    print('resource '+i+' is now available under '+str(dic_hash))
                except:
                    print('couldn\'t find resource '+i)
        
    def inputtype_detect(self):
        op_sys=os.name
            
        if self.somepath is None:
            self.somepath=str(input('Enter dir file or URL: '))
            self.somepath=self.dir_file_or_url(self.somepath)
        
        elif type(self.somepath) is str:
            self.somepath=self.dir_file_or_url(self.somepath)
        
        elif type(self.somepath) is list:
            temp_list=[]
            for whats_in_list in self.somepath:
                temp_list+=self.dir_file_or_url(whats_in_list)
            self.somepath=temp_list
        
        elif type(self.somepath) is dict:
            for key, string in self.somepath.items():
                self.bib[self.hash_it(key)]=string
            self.somepath=list(self.somepath.keys())
        
        elif any(type(self.somepath) is supported_types for supported_types in [None,str,list,dict])==False:
            print('Format is not recognizable')
        
    def word_it(self,word):
        if len(word)>1:    
            while True:
                if word[-1] in self.signs: #not good for dosages
                    word=word[:-1]
                else:
                    break
        return word.lower()
    
    def hash_it(self,word):
        return hash(self.word_it(word))%self.dict_size
        
    
    def is_it_in_yet(self,word):
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
                       
         
    def add_words(self,liste):
        if len(liste)>100: 
            self.threaded([self.add_words,'addwords',liste])
        else:
            stdout.write('\n\nwith worker '+str(os.getpid())+'\n')
            for i in liste:
                i=self.word_it(i)
                in_yet, target=self.is_it_in_yet(i)
                if in_yet==True:
                    to_list=self.dictionary[target]
                    if int in [type(in_list) for in_list in to_list]:
                        for pos, val in enumerate(to_list):#predefining structur would be very helpful ti keep checking overhead in bay
                            if type(val)==int:
                                to_list[pos]+=1
                                break
                    else:
                        to_list.append(1)
                        
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
                                    to_list.append(1)
                                    self.dictionary[k]=to_list#over complicated by multiprocessing.managers.ListProxy
                                    stdout.write('\r'+i+' added at Position '+str(k)+'\n')
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
                                    to_list.append(1)
                                    self.dictionary[k]=to_list#over complicated by multiprocessing.managers.ListProxy
                                    stdout.write('\r'+i+' added at Position '+str(k)+'\n')
                                    break 
                    except:
                        self.dictionary.append([i])
                        pos=len(self.dictionary)-1
                        self.dictionary[target].append((i,pos))
                        stdout.write('\r'+i+' added at Position '+str(pos)+'\n')# if there are no open positiones anymore
                    # if type(self.dictionary)==type(mp.Manager().list()):   
                    #     self.lock.release()
    
    def threaded(self,func):
        num_threads=mp.cpu_count()
        segs=[x*int(len(func[2])/num_threads) for x in range(num_threads+1)]
        segs[-1]=len(func[2])
        thread_list=[]
            
        for i in range(len(segs)-1):
            if len(func)==3:  
                t=th.Thread(target=func[0],name=func[1],args=(func[2][segs[i]:segs[i+1]],))
            elif len(func)==2:
                t=th.Thread(target=func[0],name=func[1])
            t.start()
            thread_list.append(t)
    
        # for thread in thread_list:
        #     thread.join()     
                          
    
    def build_dict(self,path='F:/Desktop/_AugmenText/dictionary/words.txt'): 
        words=open(path,'rb')
        txt=words.read().decode('utf8','ignore').split('\n')
        words.close()
        txt+=self.signs+self.supported_chr
        liste=[]
        
        for i in txt:
            liste.append((self.hash_it(i),i))
        
        self.dictionary=[]
        self.rejected=[]
        for i in range(10**6):
            self.dictionary.append([])
        x,k=0,0
        for i,y in liste:
            in_yet,_=self.is_it_in_yet(y)
            if in_yet!=True:
                self.dictionary[i].append(self.word_it(y))
                k+=1
            else:
                self.rejected.append(y)
            x+=1
        print('\n'+str(k)+' from '+str(x)+' Words added\n')
        
        txt=None
        liste=None
          
     
    def threaded_build(self,seg,seg2):
        x=0
        dude=self.dictionary[seg:seg2]
        stdout.write('segment '+str(seg)+' to '+str(seg2)+' has started with worker '+str(os.getpid())+'\n')
        for prog,stuff in enumerate(dude):         
            if prog%1000==0:                           
                self.lock.acquire()
                self.count.value+=1000
                self.lock.release()
    
            if len(stuff)>1:
                for i in range(1,len(stuff)):
                    for pos,entry in enumerate(dude[x:]):
                        if entry==[]:
                            pos+=x
                            entry.append(stuff[i])
                            stuff[i]=(stuff[i],pos+seg)
                            x=pos
                            break
                        
        self.lock.acquire()
        self.dictionary[seg:seg2]=dude
        self.lock.release()
        stdout.write('\rsegment '+str(seg)+' to '+str(seg2)+' has finished\n')
    
    
    def load_bar(self):
        while self.count.value<self.dict_size:           
            tot_prog=self.count.value
            if tot_prog%(self.dict_size/1000) in [0,1,2,3,4,5,6,7,8,9]:
                stdout.write('\r['+'||'*int(tot_prog/(self.dict_size/10))+']'+str(round(tot_prog/self.dict_size*100,4))+'% ')
        stdout.write('\r 100.0%          '+str(tot_prog)+'          \n')

            
    def multi_proc(self):
        
        self.count=mp.Manager().Value('i',0,lock=True)
        self.dictionary=mp.Manager().list(self.dictionary)
        
        num_segs=mp.cpu_count()
        if num_segs>5:
            num_segs=int(input('Number of workers? Max is '+str(num_segs)+' '))
        segs=[x*int(self.dict_size/num_segs) for x in range(num_segs+1)]
        segs[-1]=self.dict_size
        process_list=[]
        things_todo=[[self.threaded_build,(segs[i],segs[i+1])] for i in range(num_segs)]
        things_todo.append([self.load_bar])
        
        for i in range(len(things_todo)):
            if len(things_todo[i])==2:  
                p=mp.Process(target=things_todo[i][0],args=things_todo[i][1])
            elif len(things_todo[i])==1:
                 p=mp.Process(target=things_todo[i][0])
            process_list.append(p)
            p.start()
        for process in process_list:
            process.join()
    
    def run(self):
        self.inputtype_detect()
        self.add_to_bib(self.somepath) 
        self.work_through()
        self.build_dict()
        self.multi_proc()

# if __name__ == "__main__":
#     augmentext().run()        
        
        

        
        

        