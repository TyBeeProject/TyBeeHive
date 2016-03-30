import os
import sys
import conf
import json
import requests
from time import sleep, time
from multiprocessing import Pool
from importlib.machinery import SourceFileLoader


#############
# Functions #
#############

def logCaptor(captor):
    return (captor.getId(), captor.callback())
    
def createMessage(listOfResult):
    return {'idHive':conf.idHive, 'timeStamp': time(), 'captorDatas':listOfResult}

def sendMessage (host, port, url, payload):
    r = requests.post(host+':'+port+'/'+url, json = payload)
    return r
    
#############
# MAIN LOOP #
#############

if __name__ == "__main__":

    ###
    ### Loading every captors' conf
    ###
    
    captorsObject = []
    captorsPath = []

    for root, dirs, files in os.walk(conf.captorPath):
        for name in files:
            if name[-3:] == ".py":
                captorsPath += [os.path.join(root,name)]
 

    # Charge tout les capteurs et les teste
    for captorPath in captorsPath :
    # On essaie d'importer le module du capteur
        try :
            captorLoader = SourceFileLoader('Captor', captorPath).load_module()
        except ImportError as e:
            print ('[FAIL] Loading :'+captorPath+' issued :\n'+e)#+errormessage
        else:

        # Test pour vérifier que le callback ne plante pas
            try :
                captorObject = captorLoader.Captor()
                captorObject.callback()
                captorObject.getId()
            except :
                e = sys.exc_info()
                print ('[FAIL] Testing :'+captorPath+' issued :\n' + str(e))
            else:
                captorsObject.append(captorObject)


    ###
    ### Launching every thread
    ###
    
    while "Loic est beau":

        # Loading the new pool
        #pool = Pool()

        result_list = []

        for captor in captorsObject:
            result_list.append(logCaptor(captor))
        #     pool.apply_async(logCaptor, args = (captor,), callback = result_list.append)
        # pool.close()
        # pool.join()
    
        # Create the payload to send
        payload=createMessage(result_list)

        # TODO : Start a thread for sending the request
        sendMessage(conf.hostIP, conf.hostPort, conf.hostURL, payload)
        
        sleep(conf.pauseDelay)
