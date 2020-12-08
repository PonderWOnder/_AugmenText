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
import nltk.tokenize as to_token
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
        
        
        
        :param path_to_text: The default is None.
        :type path_to_text: Type
        :param dictionary: The default is None.
        :type dictionary: Type
        :param syn_loc: The default os.path.abspath('dictionary\Syn_Ant.txt').
        :type syn_loc: Type
        :param dict_size: The default is 10**6.
        :type dict_size: Type
        :param signs: The default is [' ','.',',','-',':',')'].
        :type sings: Type
        :param list_of_supported_files: The default is 
        ['.doc','.pdf','http:','https:','www.','.htm','.txt'].
        :type list_of_supported_files: Type
        :param supported_chr: The default is 
        [chr(i) for i in range(32,127)]+['ä','ü','ö','Ä','Ü','Ö'].
        :type supported_chr: Type
        :return: None
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
        print('Konsti loaded')
        
    def dir_file_or_url(self,location):
        '''
        Checks input type.
        
        :param location: The list of resource identifiers or directories.
        :type location: list of strings
        :return: Returns only values that carry predefined strings in a List 
                 of strings.
       '''
       
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
        '''
        Handels txt files.
        
        :param location: Resource identifier pointing towards local file.
        :type location: string
        :return: Text in file in string.
        '''
        
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
        '''
        Handles Links in text by spliting them into words present 
        in the dictionary and droping everything else.
        
        :param string: Containing special characters
        :type string: String
        :yields: Splitted Input string by its special characters an just 
        returns words inside self.dictionary as list of strings and passes them
        into addwords.
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
        '''
        Basic NLTK tokenizer for words and sentences.
        
        :param text: Whole document which is going to be tokenized
        :type text: String
        :return: Returns String in Lists in List that were seperated by 
                 individual words and sentences.
        '''
        sep=[to_token.word_tokenize,to_token.sent_tokenize]
        return [i(text) for i in sep]
    
    
    def split_text(self,text,corpus=3):
        '''
        Basic tokenizer. Will be replaced by nltk in th future.
        
        :param text: Whole document which is going to be tokenized
        :type text: String
        :param corpus: Optional Value that determins for how many seperation 
                       character should be accounted for.
        :type corpus: Integer
        :return: Returns lists that were seperated by characters in sep 
                 (max lenth = 5)
        '''
       
        sep=['',' ','.','\n','\t','\r']
        if corpus > 5:
            corpus=3
        return [text.split(i) for i in sep[:corpus] if i in text]
    
    
    def drop_stuff(self,text): 
        '''
        Checks text for non predefined ASCII values and replaces them with an 
        empty string.
        
        :param text: Single word out of the tokenizer
        :type text: String
        :return: Cleaned from everything that is not in self.supported_chr in 
                 string.
        '''
        
        supp_chr=self.supported_chr
        new_text=[i if i in supp_chr else ' ' for i in text]
        return ''.join(new_text)
    
    
    def work_through(self):
        '''
        Applies tokenizer to extend self.bib(bibliography) entries by 
        tokenized representations of text
        
        :param self: Adds return of self.slit_text to self.bib
        :type self: List of strings
        :yields: Adds the return of self.split_text to self.bib in a List of 
                 strings
        '''
        
        for key in self.bib.keys():
            self.bib[key]+=self.nltk_split_text(self.bib[key][0])
            #self.bib[key]+=self.split_text(self.bib[key][0])
            print('text '+str(key)+' was seperated')        
    
    
    def add_to_bib(self):
        ''' 
        Adds entries to self.bib(bibliography). Depend on their type 
        different interfaces are used.
        
        :param path_list: List of resource identifiers (self.somepath).
        :type path_list: List
        :yields: Full text entries to self.bib(bibliography) as one string in 
                 List.
        '''
        
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
        '''        
        Handles various different ways of supplying locations of text corpus 
        provided by URLs in self.somepath variable from the constructor.
        
        :return: None
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
            for key, read_string in self.somepath.items():
                self.bib[self.hash_it(key)]=read_string
            self.somepath=list(self.somepath.keys())
        
        elif any(type(self.somepath) is supported_types for supported_types in [None,str,list,dict])==False:
            print('Format is not recognizable')
    
        
    def word_it(self,word):
        '''
        Standardizes strings for hashing. Drops . , on the and for example.
        
        :param word: Single tokenized word to be standardized.
        :type word: String
        :return: Dropped everything on the end of the word that is in 
                 self.sings string.
        '''
        
        if len(word)>1:    
            while True:
                if word[-1] in self.signs and len(word)>1: #not good for dosages
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
            
        
    def add_words(self,liste=None,occurrence=0):
        '''
        Adds tokens to the dictionary either counting their appearence or not. 
        For larger corpus (10**6) it switches in threaded mode
        
        :param liste: Words from self.bib.
        :type liste: List
        :param occurence: The default is1.
        :type occurence: Integer
        :yields: Postition string pairs to be added into self.dictionary at 
                 position
        '''
        
        if type(None)==type(liste):
            liste=self.token_list
        self.seg_length=100000
        if len(liste)>self.seg_length:
            self.num_segs=mp.cpu_count()
            stepsize=int(len(liste)/self.num_segs)
            stuff_todo=[]
            for i in range(0,len(liste),stepsize):
                rest=len(liste)%stepsize
                if rest==len(liste)-i:
                    add=rest
                else:
                    add=0
                stuff_todo.append([self.add_words,liste[i:i+stepsize+add]])
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
        return
    
    def __threaded(self,func):
        '''
        Multi threading setup to handel processes in parallel.
        
        :param func: Includes function, handler name for function and argument 
        for function.
        :type func: List
        :return: None
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
        '''
        Maps words from line seperated txt provided in parameter path to hash 
        postions in list self.dictionary. Does not do any hash collission 
        detection!
        
        :param path: Locates the dictionary txt '~dictionary/words.txt').
        :type path: String
        :yields: Crued self.dict not checked for collisions.
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
        '''
        Detects collissions in segments of self.dictionary and maps them to 
        empty positions within the segment. Should only be used if no other 
        processes has altered self.dictionary
        
        :param seg: Beginning
        :type seg: Integer
        :param seg2: End
        :type seg2: Integer
        :return: None
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
    
    
    def __syno_ant(self,syn_loc=None):
        '''
        Far to long function to transform synonym dictionary provided under the
        location parameter into useable input to append self.dictionary with 
        synonym capabilities.
        
        :param syn_loc: The defailt is None but is later changed to 
        self.syn_ant which is location of synonym antonym dictionary. 
        Function would work with any other.
        
        :type syn_loc: None
        :yields: List of strings of entries in this specific synonym antonym 
        dictionary. 
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
        '''
        Adding synonyms from self.syn_list tailored to be passed into 
        multi_proc modul for faster processing.
        
        :param seg1: Beginning
        :type seg1: Integer
        :param seg2: End
        :type seg2: Integer
        :yields: Adds Synonyms and Antonyms to self.dictionary.
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
        '''
        Finds synonyms prefering first entries
        
        :param word: Function chooses how to progress
        :type word: String orInteger
        :param ant: Choose antonym if True. The default is False.
        :type word: Boolian
        :return: String or integer from input.
        '''
        
        what_it_is=('Synonym','Antonym')
        if type(word)==str:
            pos=self.find_it(word)
            info=self.dictionary[pos]
        elif type(word)==int:
            info=self.dictionary[word]
        elif type(word)==list:
            pos=self.find_it(word[0])
            info=self.dictionary[pos]
        if list in [type(x) for x in info]:
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
        '''
        Just a for fun progressbar for initial hash collission detection.
        
        :param length: To set the total amount of entries that will be changed
        :type length: Integer
        :return: None
        '''
        
        while self.count.value<length:           
            tot_prog=self.count.value
            if tot_prog%(length/increment) in [0,1,2,3,4,5,6,7,8,9]:
                stdout.write('\rLoading'+' ['+'||'*int(tot_prog/(length/10))+']'+str(round(tot_prog/length*100,4))+'% ')
        stdout.write('\r100.0%\t'+str(tot_prog)+'\t\t\n')

            
    def multi_proc(self,things_todo):
        '''
        Multi processing setup to handel processes in parallel on different 
        CPU Cores.
        
        :param things_todo: Function and args.
        :type things_todo: List of Items
        :returns: None
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
    
    
    def _create_task_list(self):
        '''
        Actual execution order for multiprocessed tasks.
        
        :return: Contains Includes function and argument for function in 
        List of Lists.
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
        


    def _save_dict(self,location='ouput.new'):
        '''        
        :param location: the default is 'output.new'
        :type location: String
        :return: None
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
        '''        
        Actual execution order for pipeline tasks
        
        :returns: None
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
        '''        
        Actual execution order for pipeline tasks
        :return: None
        '''
        
        self.add_to_bib() 
        self._load_dict()
        self.build_dict()
        self.syno_ant()
        stuff_todo=self._create_task_list()
        for things_todo in stuff_todo:
            self.multi_proc(things_todo)
        #self._save_dict()
        input(':')
        return self






        