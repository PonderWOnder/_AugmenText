from sys import stdout
import os
import multiprocessing as mp
import threading
import time

count=0
dic_size=10**6

def load():
    words=open('F:/Desktop/_AugmenText/words.txt','rb')
    txt=words.read().decode('utf8','ignore').split('\n')
    words.close()
    return txt

def create_list(txt):
    txt+=[' ','.','-']
    liste=[]
    for i in txt:
        liste.append((hash(i.lower()),i))
    return liste

def hashed_list(liste):
    global dic_size
    liste2=[]
    for i in liste:
        liste2.append((i[0] % dic_size,i[1]))
    return liste2

def make_dic(liste2):
    dictionary=[]
    global dic_size
    for i in range(dic_size):
        dictionary.append([])
    for pos,word in liste2:
        dictionary[pos].append(word)
    return dictionary

def threaded_build(dictionary,seg,seg2):
    x=0
    dude=dictionary[seg:seg2]
    stdout.write('segment '+str(seg)+' to '+str(seg2)+' has started with worker '+str(os.getpid())+'\n')
    for prog,stuff in enumerate(dude):
        global count                
        count+=1

        if len(stuff)>1:
            for i in range(1,len(stuff)):
                for pos,entry in enumerate(dictionary[seg+x:]):
                    if entry==[]:
                        pos+=x
                        entry.append(stuff[i])
                        stuff[i]=(stuff[i],pos+seg)
                        x=pos
                        break
    stdout.write('\rsegment '+str(seg)+' to '+str(seg2)+' has finished\n')

def load_bar(dic_size):
    s=time.time()
    global count
    while count<dic_size-1000 and time.time()-s<1600:
        tot_prog=count
        if tot_prog%(dic_size/100000)==0:
            stdout.write('\r['+'||'*int(tot_prog/(dic_size/10))+']'+str(round(tot_prog/dic_size*100,4))+'% ')
    stdout.write('\r 100.0%          '+str(count)+'          \n')
         

def threaded(dic):
    dictionary=dic
    global dic_size
    num_segs=mp.cpu_count()
    thread_list=[]
    segs=[x*int(len(dictionary)/num_segs) for x in range(num_segs+1)] 
    segs[-1]=dic_size

    things_todo=[[threaded_build,'Segment'+str(segs[i])+str(segs[i+1]),(dictionary,segs[i],segs[i+1])] for i in range(num_segs)]
    things_todo.append([load_bar,'Progresbar',(dic_size,)])

    for i in range(len(things_todo)):
        t=threading.Thread(target=things_todo[i][0],name=things_todo[i][1],args=things_todo[i][2])
        t.start()
        thread_list.append(t)

    for thread in thread_list:
        thread.join()
    
    return dictionary

def multi_proc(dic):
    dictionary=dic
    global dic_size
    num_segs=mp.cpu_count()
    if num_segs>5:
        num_segs=5
    segs=[x*int(dic_size/num_segs) for x in range(num_segs+1)]
    segs[-1]=dic_size
    process_list=[]
    things_todo=[[threaded_build,(dictionary,segs[i],segs[i+1])] for i in range(num_segs)]
    things_todo.append([load_bar,(dic_size,)])
    
    for i in range(len(things_todo)):
        p=mp.Process(target=things_todo[i][0],args=things_todo[i][1])
        process_list.append(p)
        p.start()

    for process in process_list:
        process.join()
    
    return dictionary


if __name__ == "__main__":
    dictionary=multi_proc(make_dic(hashed_list(create_list(load()))))
    dictionary2=threaded(make_dic(hashed_list(create_list(load()))))
