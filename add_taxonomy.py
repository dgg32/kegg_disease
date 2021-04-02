import sys, re, os
from urllib.request import urlopen
from threading import Thread
import queue

import json
from threading import Semaphore

writeLock = Semaphore(value=1)

input_file = sys.argv[1]

module_url_prefix = "http://rest.kegg.jp/get/gn:"

print ("ko,name,taxonomy")

in_queue = queue.Queue()
out_queue = queue.Queue()


def work():
    while True:
        
        package = in_queue.get()

        #print ("first", package, package[1]

        kegg = package[0].replace('"', "")
        name = package[1].replace('"', "")
        taxonomy = ""
        #try:
        detail = urlopen(module_url_prefix + kegg).read().decode("utf-8")


        for line in detail.split("\n"):
            line = line.strip()

            if line.startswith("LINEAGE"):
                taxonomy = line.replace("LINEAGE", "").strip()


        writeLock.acquire()

        print (",".join([f'"{kegg}"', f'"{name}"', f'"{taxonomy}"']))
        writeLock.release()
        #except:
            #in_queue.put(kegg)
            #pass
        
        #finally:
        #out_queue.put([kegg, taxid_count])

        in_queue.task_done()


for i in range(1):
    t = Thread(target=work)
    t.daemon = True
    t.start()


is_header = False

        

for line in open(input_file, 'r'):

    if is_header == False:
        is_header = True
    
    else:
        fields = line.strip().split(",")
        #print (fields)
        kegg = fields[0]
        name = fields[1]

        in_queue.put([kegg, name])

in_queue.join()