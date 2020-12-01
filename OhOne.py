# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 09:37:08 2020

@author: 'Schmatz, Pasic, Braun, Avramidis'
E-Mail: 'ds181019,ds182001,ds181026,ds181009@fhstp.ac.at'
"""
import os
from sys import stdout
import threading as th
import multiprocessing as mp
import time
import nltk.tokenize as token
from json import load, dump
from hashlib import md5
from random import randint
from urllib.request import urlopen
from bs4 import BeautifulSoup as urlreader 





class aug_loader:
    
    
    def __init__(self, path_to_text=None,
                 dictionary=None,
                 syn_loc=os.path.abspath('dictionary\Syn_Ant.txt'),
                 dict_size=10**6,
                 signs=[' ','.',',','-',':',')'],
                 list_of_supported_files=['.doc','.pdf','http:','https:','www.','.htm','.txt'],
                 supported_chr=[chr(i) for i in range(32,127)]+['ä','ü','ö',
                                                                'Ä','Ü','Ö']):
        '''
        

        Parameters
        ----------
        path_to_text : TYPE, optional
            DESCRIPTION. The default is None.
        dictionary : TYPE, optional
            DESCRIPTION. The default is None.
        syn_loc : TYPE, optional
            DESCRIPTION. The default is os.path.abspath('dictionary\Syn_Ant.txt').
        dict_size : TYPE, optional
            DESCRIPTION. The default is 10**6.
        signs : TYPE, optional
            DESCRIPTION. The default is [' ','.',',','-',':',')'].
        list_of_supported_files : TYPE, optional
            DESCRIPTION. The default is ['.doc','.pdf','http:','https:','www.','.htm','.txt'].
        supported_chr : TYPE, optional
            DESCRIPTION. The default is [chr(i) for i in range(32,127)]+['ä','ü','ö','Ä','Ü','Ö'].

        Returns
        -------
        None.

        '''
        self.somepath=path_to_text#should be list of URLs pointing to text of some sort
        self.syn_ant=syn_loc
        self.bib={}#will contain bibliography
        self.dict_size=dict_size#predefines size of hashtable dictionary (will be extended automatically if full)
        self.signs=signs#no idea if we need them but should be used for single words if they are distorted on th end
        self.list_of_supported_files=list_of_supported_files#nomen est omen
        self.supported_chr=supported_chr#nomen est omen
        self.dictionary=dictionary  #list sturcture to be used as hashed list
        self.count=0#just exists for loading bar function no greater us so far
        self.lock=mp.Lock()#function to coordinate dictioary writes in multiprocessing enviorment
        self.vector_size=0#depented on the amount of individual words used in text.  Since transformations are applied to text value most likely will be estimated by propabilities of transforamtion
        self.lower_letters=[chr(i) for i in range(97,123)]
        
    def dir_file_or_url(self,location):
        '''Checks input type.
       
        Parameters
        ----------
        location : list of strings
            DESCRIPTION. This is the list of resource identifiers or directories.
            
        Returns
        -------
        list of strings
           DESCRIPTION. Returns only values that carry predefined strings'''
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
   
    
    def load_txt(self,location): #TXT
        '''handels txt files.
        
        Parameters
        ----------
        location : string
            DESCRIPTION. resource identifier pointing towards local file.
        
        Returns
        -------
        inter: string
           DESCRIPTION. Returns string containing text in file'''
        txt=open(location,'rb')
        inter=txt.read().decode('utf8','ignore')
        txt.close()
        return inter 
    
    
    def __load_worddoc_text(self,location):
        ''''''
        pass
    
    
    def __load_pdf_text(self,location):
        ''''''
        pass
    
                   
    def _word_asstimator(self,string): 
        '''handles Links in text by spliting them into words present 
        in the dictionary and droping everything else
        
        Parameters
        ----------
        string: string
            DESCRIPTION. String containing special characters
        
        Yields
        ----------
        output_list: list of strings
            DESCRIPTION. splited Input string by its special characters an just returns words inside self.dictionary
        '''
        clean_string=''
        for i in string:
            if i in self.lower_letters:
                clean_string+=i
            else:
                if clean_string!='':
                    if clean_string[-1]==' ':
                        pass
                    else:
                        clean_string+=' '
        inter=clean_string.split(' ')
        output_list=[]
        for i in inter:
            tf,_=self.is_it_in_yet(i)
            if tf==True and len(i)>1:
                output_list.append(i)
        self.add_words(output_list,0)
    
    
    def nltk_split_text(self,text):
        sep=[token.word_tokenize,token.sent_tokenize]
        return [i(text) for i in sep]
    
    
    def split_text(self,text,corpus=3):
        '''Basic tokenizer. Will be replaced by nltk in th future
        
        Parameters
        ----------
        text: string
            DESCRIPTION. whole document which is going to be tokenized
        corpus: integer, optional(default=3,max=5)
            DESCRIPTION. optional value that determins for how many seperation character should be accounted for
        
        Returns
        ----------
        list of list of strings
            DESCRIPTION. Returns lists that were seperated by characters in sep (max length=5)'''
        sep=['',' ','.','\n','\t','\r']
        if corpus > 5:
            corpus=3
        return [text.split(i) for i in sep[:corpus] if i in text]
    
    
    def drop_stuff(self,text): 
        '''Checks text for non predefined ASCII values and replaces them with an empty string.
        
        Parameters
        ----------
        text: string
            DESCRIPTION. single word out of the tokenizer
        
        Returns
        ----------
        string
            DESCRIPTION. cleaned from everything that is not in self.supported_chr'''
        supp_chr=self.supported_chr
        new_text=[i if i in supp_chr else ' ' for i in text]
        return ''.join(new_text)
    
    
    def work_through(self):
        '''Applies tokenizer to extend self.bib(bibliography) entries by tokenized representations of text
        
        Yields
        ----------
        list of list of strings
            DESCRIPTION. adds the return of self.split_text to self.bib''' 
        for key in self.bib.keys():
            self.bib[key]+=self.nltk_split_text(self.bib[key][0])
            #self.bib[key]+=self.split_text(self.bib[key][0])
            print('text '+str(key)+' was seperated')        
    
    
    def add_to_bib(self):
        '''adds entries to self.bib(bibliography). Depend on their type different interfaces are used.

        Parameters
        ----------
        path_list : list
            List of reource identifiers (self.somepath).

        Yields
        -------
        list
            Full text entries to self.bib(bibliography) as one string in list.'''
        self.inputtype_detect()
        path_list=self.somepath
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
        self.work_through()
        
    
        
    def inputtype_detect(self):
        '''handles various different ways of supplying locations of text corpus provided by URLs in self.somepath variable from the constructor.

        Returns
        -------
        None.

        '''
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
        '''Standardizes strings for hashing. Drops . , on the and for example.

        Parameters
        ----------
        word : string
            DESCRIPTION. single toknized word to be standardized.

        Returns
        -------
        string
            DESCRIPTION. droped everything on the end of the word that is in self.signs.

        '''
        if len(word)>1:    
            while True:
                if word[-1] in self.signs: #not good for dosages
                    word=word[:-1]
                else:
                    break
        return word.lower()
    
    
    def hash_it(self,word):
        '''standardizes and numerically hashes string that resembles a word, sentence or paragraph although word would be preferable.

        Parameters
        ----------
        word : string
            DESCRIPTION. unaltered string most likly from the tokenizer.

        Returns
        -------
        integer
            DESCRIPTION. numerical hash representation of to provided string

        '''
        return int(md5(str.encode(self.word_it(word))).hexdigest(),16)%self.dict_size
    
    
    def is_it_in_yet(self,word):
        '''Checks if word is already in self.dictionary and returns its position also considering hash collissions if word is already in dic

        Parameters
        ----------
        word : string
            some unaltered word.

        Returns
        -------
        boolian
            True if word is in self.dictionary.
        pos : integer
            position within self.dictionary.

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
        _,pos=self.is_it_in_yet(word)
        return pos             
            
        
    def add_words(self,liste,occurrence=0):
        '''adds tokens to the dictionary either counting their appearence or not. For larger corpus (10**6) it switches in threaded mode

        Parameters
        ----------
        liste : list
            DESCRIPTION. words from self.bib.
        occurrence : integer, optional
            DESCRIPTION. The default is 1.

        Yields
        -------
            DESCRIPTION. position string pairs to be added into self.dictionary at position

        '''
        self.seg_length=10000000
        if len(liste)>self.seg_length: 
            self.threaded([self.add_words,'addwords',liste])
        else:
            for i in liste:
                i=self.word_it(i)
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
                        stdout.write('\r'+i+' added at Position '+str(pos)+'\n')# if there are no open positiones anymore
                    # if type(self.dictionary)==type(mp.Manager().list()):   
                    #     self.lock.release()
    
    
    def threaded(self,func):
        '''Multi threading setup to handel processes in parallel

        Parameters
        ----------
        func : list
            DESCRIPTION. Includes function, handler name for function and argument for function.

        Returns
        -------
        None.

        '''
        if len(func)>2:
            for i in range(2,len(func[2])):
                if len(func[2])/i < self.seg_length:        
                    num_threads=i
                    break
            segs=[x*int(len(func[2])/num_threads) for x in range(num_threads+1)]
            segs[-1]=len(func[2])
        thread_list=[]
            
        for i in range(len(segs)-1):
            if len(func)==3:  
                t=th.Thread(target=func[0],name=func[1],args=(func[2][segs[i]:segs[i+1]],))
            elif len(func)==2:
                t=th.Thread(target=func[0],name=func[1])
            t.start()
            stdout.write('\n\nwith worker '+str(os.getpid())+'\n')
            thread_list.append(t)
    
        for thread in thread_list:
            thread.join()     
                          
    
    def build_dict(self,path=os.path.abspath('dictionary/words.txt')): 
        '''Just maps words from line seperated txt provided in parameter path to hash postions in list self.dictionary. Does not do any hash collission detection!

        Parameters
        ----------
        path : string, optional
            DESCRIPTION. Locates the dictionary txt '~dictionary/words.txt').

        Yields
        -------
            DESCRIPTION. Crued self.dict not checked for collisions.

        '''
        words=open(path,'rb')
        txt=words.read().decode('utf8','ignore').split('\n')
        words.close()
        txt+=self.signs+self.supported_chr
        liste=[]
        
        for i in txt:
            liste.append((self.hash_it(i),i))
        
        self.dictionary=[]
        self.rejected=[]
        for i in range(self.dict_size):
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
        '''Detects collissions in segments of self.dictionary and maps them to empty positions within the segment. Should only be used if no other processes has altered self.dictionary
        

        Parameters
        ----------
        seg : integer
            DESCRIPTION. Beginning
        seg2 : integer
            DESCRIPTION. End

        Returns
        -------
        None.

        '''
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
    
    
    def syno_ant(self,syn_loc=None):
        '''far to long function to transform synonym dictionary provided under the location parameter into useable input to append self.dictionary with synonym capabilities.

        Parameters
        ----------
        syn_loc : None, optional
            DESCRIPTION. The default is None but is later changed to self.syn_ant which is location of synonym antonym dictionary. Function would work with any other.

        Yields
        -------
        self.syn_list : list of strings
            DESCRIPTION. List of entries in this specific synonym antonym dictionary 

        '''
        if syn_loc==None:
            syn_loc=self.syn_ant
        txt=open(syn_loc,'rb')
        inter=txt.read().decode('utf8','ignore')
        txt.close()
        window_len=4
        sliding=''
        entries=[]
        record=False
        word=-1
        for i in inter:
            if len(sliding)>window_len:
                sliding=sliding[1:]
            sliding+=i
            if '\nKEY:' == sliding:
                record=True
                i=sliding
                entries.append('')
                word+=1
            elif '\r\n=' in sliding:
                record=False
            if record==True:
                if i=='_':
                    i=' '
                entries[word]+=i.lower()
        
        stuff_to_drop=len(entries)      
        for num,entry in enumerate(entries[:stuff_to_drop]):
            sliding=''
            entries.append('')
            for i in entry:
                if len(sliding)>window_len:
                    sliding=sliding[1:]
                if i not in ['\r','\n']:
                    sliding+=i
                    entries[stuff_to_drop+num]+=i.lower()
                if 'key: ' == sliding:
                    entries[stuff_to_drop+num]=entries[stuff_to_drop+num][:-1*(window_len+1)]
                elif 'syn: ' == sliding:
                    entries[stuff_to_drop+num]=entries[stuff_to_drop+num][:-1*(window_len+1)]
                elif 'ant: ' == sliding:
                    entries[stuff_to_drop+num]=entries[stuff_to_drop+num][:-1*(window_len+1)]
        entries=entries[stuff_to_drop:]
        
        for num,entry in enumerate(entries[:stuff_to_drop]):
            to_stomp=0
            in_turn,to_turn=0,0
            two_evils=['[','{','\\']
            count=False
            end=None
            entries.append('')
            for pos,i in enumerate(entry):
                if i in two_evils and i!=end:
                    if len(two_evils)!=1:
                        count=True
                        in_turn+=1
                        two_evils=[i]
                        if i=='[':
                            end=']'
                        elif i=='{':
                            end='}'
                        elif i=='\\':
                            end='\\'
                    else:
                        in_turn+=1
                
                if count==True:
                    to_stomp+=1
                    
                entries[stuff_to_drop+num]+=i.lower()
                if i==end and to_stomp>1 or i=='.':
                    to_turn+=1
                    if in_turn==to_turn or i=='.':
                        entries[stuff_to_drop+num]=entries[stuff_to_drop+num][:-1*(to_stomp+1)]
                        count=False
                        to_stomp=0
                        two_evils=['[','{','\\']
                        in_turn,to_turn=0,0
                        end=None
                    if i=='.':
                        entries[stuff_to_drop+num]+='. '
        entries=entries[stuff_to_drop:]
        
        print(str(stuff_to_drop)+' Synonyms found in '+syn_loc+'!\n')

        self.syn_list=[]
        print('Dropped Lines:',end=' ')
        for num,entry in enumerate(entries):
            line=[i for i in entry]
            if '\\' in line:
                print(str(num),end=', ')
            elif '[' in line:
                print(str(num),end=', ')
            elif ']' in line:
                print(str(num),end=', ')
            elif '{' in line:
                print(str(num),end=', ')
            elif '}' in line:
                print(str(num),end=', ')
            else:
                self.syn_list.append(entry)
        print('\n')
    
    
    def add_syns(self,seg1,seg2):
        '''adding synonyms from self.syn_list tailored to be passed into multi_proc modul for faster processing.

        Parameters
        ----------
        seg1 : integer
            DESCRIPTION. beginning 
        seg2 : TYPE
            DESCRIPTION. end

        Yields
        -------
            DESCRIPTION. Adds Synonyms and Antonyms to self.dictionary.

        '''
        inter_list=[]
        stdout.write('segment '+str(seg1)+' to '+str(seg2)+' has started with worker '+str(os.getpid())+'\n')
        working_on=self.syn_list[seg1:seg2]
        for stuff in working_on:
            stuff=''.join([i for i in stuff if i!=' '])
            stuff=''.join([stuff[i] for i in range(len(stuff)) if stuff[i:i+2]!='..'])
            stuff=stuff.split('.')[:-1]
            stuffed=[]
            if len(stuff)>1:
                for stuffing in stuff:
                    stuffing=stuffing.split(',')
                    stuffed.append(stuffing)
                stuffed[0]=self.word_it(stuffed[0][0])
                #stdout.write('\n'+stuffed[0])
                inter_list.append(stuffed)
                way_to_go=len(inter_list)
                stdout.write('\r'+str(way_to_go)+' '+
                             str(len(working_on))+
                             (' False',' True ')[way_to_go==len(working_on)])
            else:
                stdout.write('\nNo Synonyms for '+stuff[0]+'\n')
        stdout.write('\n')
        
        for prog,word in enumerate(inter_list):
            if word[0]=='':
                continue
            in_yet,where_to=self.is_it_in_yet(word[0])
            stdout.write((' False',' True')[in_yet]+
                         ' '+str(where_to)+
                         ' '+str(prog)+' '+word[0])
            to_list=self.dictionary[where_to]
            if to_list==[]:
                to_list.append(word[0])
            from_list=[]
            for tab in word[1:]:
                self.add_words(tab,0)
                syn_ant_list=[]
                for syn_ant in tab:#this is stupid. there sure is a way to do it better
                    tf,pos=self.is_it_in_yet(syn_ant)
                    if tf==True:
                        if pos!=178366:
                            syn_ant_list.append(pos)
                    else:
                        self.add_words(syn_ant,0)
                        tf,pos=self.is_it_in_yet(syn_ant)
                        syn_ant_list.append(pos)  
                from_list.append(syn_ant_list)
            to_list.append(from_list)
            self.lock.acquire()
            self.dictionary[where_to]=to_list
            if prog%int(way_to_go/100)==0:                           
                self.count.value+=way_to_go/100
            self.lock.release()
            stdout.write(' '+str(where_to)+'\n ')
    
    
    def find_syn(self,word,ant=False):
        '''finds synonyms prefering first entries

        Parameters
        ----------
        word : string/integer
            DESCRIPTION. function chooses how to progress
        ant : boolian, optional
            DESCRIPTION. choose antonym if True. The default is False.

        Returns
        -------
        string/integer
            DESCRIPTION. what ever was the input

        '''
        what_it_is=('Synonym','Antonym')
        if type(word)==str:
            pos=self.find_it(word)
            info=self.dictionary[pos]
        elif type(word)==int:
            info=self.dictionary[word]
        if list in [type(i) for i in info]:
            for num,i in enumerate(info):
                if type(i)==list:
                    if i[ant]==[]:
                        stdout.write('No '+what_it_is[ant]+' found for '+word)
                        return word
                        break
                    per=100
                    pos_per=randint(1,per)
                    base=len(i[ant])
                    which_one=int(round((base**(1/per))**pos_per,0))-1
                    return i[ant][which_one]
                    break
        else:
            stdout.write('No '+what_it_is[ant]+' found for '+word)
            return word

    
    def load_bar(self,length,increment):
        '''Just a for fun progressbar for initial hash collission detection

        Parameters
        ----------
        length : integer
            DESCRIPTION. To set the total amount of entries that will be changed

        Returns
        -------
        None.

        '''
        while self.count.value<length:           
            tot_prog=self.count.value
            if tot_prog%(length/increment) in [0,1,2,3,4,5,6,7,8,9]:
                stdout.write('\rLoading'+' ['+'||'*int(tot_prog/(length/10))+']'+str(round(tot_prog/length*100,4))+'% ')
        stdout.write('\r100.0%\t'+str(tot_prog)+'\t\t\n')

            
    def multi_proc(self,things_todo):
        '''Multi processing setup to handel processes in parallel on different CPU Cores
        

        Parameters
        ----------
        things_todo : list of items
            DESCRIPTION. function and args

        Returns
        -------
        None.

        '''
        self.count=mp.Manager().Value('i',0,lock=True)
        
        process_list=[]
        s=time.time()
        for task in things_todo:
            if len(task)==2:  
                p=mp.Process(target=task[0],args=task[1])
            elif len(task)==1:
                 p=mp.Process(target=task[0])
            process_list.append(p)
            p.start()
        for process in process_list:
            process.join()
        k=time.time()-s
        stdout.write(str(len(process_list))+' processes took '+str(int(k/60))+'min '+str(int(k%60))+'sec\n\n')
    
    
    def create_task_list(self):
        '''Actual execution order for multiprocessed tasks

        Returns
        -------
        stuff_todo : list of lists
            DESCRIPTION. Contains Includes function and argument for function.

        '''
        stuff_todo=[]
        self.num_segs=mp.cpu_count()
        if self.num_segs>5:
            self.num_segs=int(input('How many CPU-Cores shall be utilized? Max is '+str(self.num_segs)+' '))
        
        if type(self.dictionary)!=type(mp.Manager().list()): 
            self.dictionary=mp.Manager().list(self.dictionary)
            
        segs=[x*int(self.dict_size/self.num_segs) for x in range(self.num_segs+1)]
        segs[-1]=self.dict_size
        things_todo=[[self.threaded_build,(segs[i],segs[i+1])] for i in range(self.num_segs)]
        #things_todo.append([self.load_bar,(self.dict_size,)])
        stuff_todo.append(things_todo)
        
        things_todo=[]
        things_todo=[[self.add_words,(self.bib[item][1],)] for item in self.bib]  
        stuff_todo.append(things_todo)
        
        if type(self.syn_list)!=type(mp.Manager().list()): 
            self.syn_list=mp.Manager().list(self.syn_list)
        things_todo=[]
        syn_dic=len(self.syn_list)
        segs=[x*int(syn_dic/self.num_segs) for x in range(self.num_segs+1)]
        segs[-1]=syn_dic
        things_todo=[[self.add_syns,(segs[i],segs[i+1])] for i in range(self.num_segs)]  
        #things_todo.append([self.load_bar,(len(self.syn_list),)])
        stuff_todo.append(things_todo)
        return stuff_todo
    
    
    def _load_dict(self,location='ouput.new'):
        '''
        

        Parameters
        ----------
        location : string, optional
            DESCRIPTION. The default is 'ouput.new'.

        Returns
        -------
        None.

        '''
        try:
            location=os.path.abspath(location)
            with open(location, "r") as fp:
                self.dictionary=load(fp)
        except:
            print('Can\'t find .new file @ '+location,end=' ')
            location=input('Please specify location: ')
            self._load_dict(location)
        


    def _save_dict(self,location='ouput.new'):
        '''
        

        Parameters
        ----------
        location : string, optional
            DESCRIPTION. The default is 'ouput.new'.

        Returns
        -------
        None.

        '''
        location=os.path.abspath(location)
        if '.new' in location:     
            with open(location, "w") as fp:
                if type(self.dictionary)!=list:
                    self.dictionary=list(self.dictionary)
                dump(self.dictionary,fp)
        else:
            print("wrong format!",end=' ')
            location=input('Please specify location: ')
            self.__save_dict(location)

            
    
    def run(self):
        '''Actual execution order for pipeline tasks

        Returns
        -------
        None.

        '''
        #self.inputtype_detect()
        self.add_to_bib() 
        self._load_dict()
        # self.work_through()
        # self.build_dict()
        # self.syno_ant()
        # stuff_todo=self.create_task_list()
        # for things_todo in stuff_todo:
        #     self.multi_proc(things_todo)
        # input(':')
        return self
    
    
    def _run_2(self):
        '''Actual execution order for pipeline tasks

        Returns
        -------
        None.

        '''
        self.add_to_bib() 
        self._load_dict()
        self.build_dict()
        self.syno_ant()
        stuff_todo=self.create_task_list()
        for things_todo in stuff_todo:
            self.multi_proc(things_todo)
        input(':')
        return self

        
class aug_input(aug_loader):
    
    def __init__(self, files=None):
        aug_loader.__init__(self,path_to_text=files)
    

        

class input_aug(aug_loader):
    pass     



        