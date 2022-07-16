import sys, re, os
import requests
from threading import Thread
import queue

import json
from threading import Semaphore

writeLock = Semaphore(value=1)

database = sys.argv[1]
output_folder = sys.argv[2]

rx_prefix_catch = re.compile(r'(\w+):\w+')

ko_list_url = "https://rest.kegg.jp/list/" + database

module_url_prefix = "https://rest.kegg.jp/get/"


in_queue = queue.Queue()
out_queue = queue.Queue()


def work():
    while True:
        
        package = in_queue.get()

        #print ("first", package, package[1]

        
        #try:
        detail = requests.get(module_url_prefix + package).text


            

        #writeLock.acquire()


        output_file = os.path.join(output_folder, package.replace(":", "_"))
        with open(output_file, 'a+') as output:
            output.write(detail)
        #print (detail)
        #writeLock.release()
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

exists = set()

for (head, dirs, files) in os.walk(output_folder):
    for file in files:
        exists.add(file)
        

ko_list = requests.get(ko_list_url).text
print (ko_list)

for line in ko_list.split("\n"):
    fields = line.strip().split("\t")
    #print (fields)
    if len(fields) == 2:
        kegg = fields[0]
        name = fields[1]

        if kegg.replace(":", "_") not in exists:

            in_queue.put(kegg)

in_queue.join()
