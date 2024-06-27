
from pysource_ipc import pysrc_ipc
import json
import os


import re
path = "E:\\Kleinworks Storage\\3d models\\Half-Life 2 (raw)\\models\\props_real\\soda.mdl"
file = "models\\props_real\\soda.mdl"
path = re.sub(r"\\[^\\]*?\.mdl$", "", path)
file = re.sub(r'.*\\', "", file)
print(path)
print(file)



#bpy.context.scene.entrec_props.models_filepath = "E:\\Kleinworks Storage\\3d models\\Half-Life 2 (raw)\\"







"""


client = pysrc_ipc.InSourceOutSource("tcp://*:5556", "tcp://localhost:5555")


receivedMessage = ""

client.ReceiveData()

def UpdateGUI():
    os.system('cls')
    
    print("PYTHON INPUT status: ",      client.currentINPUTStatus)
    #print("PYTHON OUTPUT status: ",     client.currentOUTPUTStatus, "\n")
    #print("PYTHON INPUT activity: ",    client.currentINPUTActivity)
    #print("PYTHON OUTPUT activity: ",   client.currentOUTPUTActivity, "\n\n")
    #print("PYTHON isReceivingInput: ",  client.isReceivingInput)
    #print("PYTHON isSendingOutput: ",   client.isSendingOutput, "\n")
    print("PYTHON INPUT tick count: ",  client.INPUTtickCount)
    #print("PYTHON OUTPUT tick count: ", client.OUTPUTtickCount, "\n\n")
    print("PYTHON Received metadata: ", client.receivedMetaDataBuffer)
    print("PYTHON Received message: ",  receivedMessage, "\n")

    


alreadySetClientToStopDataTransfering = False

oldTickCount = client.INPUTtickCount


#UpdateGUI()
while True:
    #UpdateGUI()
    client.receivedDataBuffer = None
    if client.RunFuncLoop() == -1:
        client.ReceiveData()
    
    if client.receivedDataBuffer != None:
        receivedMessage = json.loads(client.receivedDataBuffer)
    else:
        receivedMessage = client.receivedDataBuffer

    

    if oldTickCount + 1 == client.INPUTtickCount:
        print("PYTHON Received metadata: ", client.receivedMetaDataBuffer)
        print("PYTHON Received message: ",  receivedMessage, "\n")

    oldTickCount = client.INPUTtickCount
    


    #if client.OUTPUTtickCount == 50 and alreadySetClientToStopDataTransfering != True:
    #    client.isDoneTransfering = True

#UpdateGUI()

#input()






"""