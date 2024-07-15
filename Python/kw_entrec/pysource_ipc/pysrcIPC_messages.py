#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
# 
#  Purpose: 
# 
#  Product Contributors: Barber
# 
#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\


import zmq
import enum

class src_IPC_MESSAGE(enum.IntEnum):

#   /*ERROR messages*/

	NO_MESSAGE        = 0xE00


#   /*OUTPUT messages*/

	OUTPUT_DISCONNECT = 0xA00
	OUTPUT_READY	  = 0xA01
	TRANSFERING_DATA  = 0xA02
	DATA_MESSAGE	  = 0xA03
	TRANSFERING_DONE  = 0xA04


#   /*INPUT messages*/

	INPUT_DISCONNECT = 0xB00
	INPUT_READY	     = 0xB01
	RECEIVED_DATA    = 0xB02




def CreateOutputDisconenctMsg():
     
    masgType_frame = zmq.Frame(int(src_IPC_MESSAGE.OUTPUT_DISCONNECT).to_bytes(4, 'little'))

    return [masgType_frame]



def CreateOutputReadyMsg():
    
    msgType_frame = zmq.Frame(int(src_IPC_MESSAGE.OUTPUT_READY).to_bytes(4, 'little'))

    return [msgType_frame]
    

def CreateTransferingDataMsg(tickCount, messageMetaData):

    msgType_frame   = zmq.Frame(int(src_IPC_MESSAGE.TRANSFERING_DATA).to_bytes(4, 'little'))
    tickCount_frame = zmq.Frame(tickCount.to_bytes(4, 'little'))
    metaData_frame  = zmq.Frame(messageMetaData)

    return [msgType_frame, tickCount_frame, metaData_frame]


def CreateDataMsg(tickCount, data):
     
    msgType_frame   = zmq.Frame(int(src_IPC_MESSAGE.DATA_MESSAGE).to_bytes(4, 'little'))
    tickCount_frame = zmq.Frame(tickCount.to_bytes(4, 'little'))
    data_frame      = zmq.Frame(data)

    return [msgType_frame, tickCount_frame, data_frame]

def CreateTransferingDoneMsg(tickCount):

    msgType_frame   = zmq.Frame(int(src_IPC_MESSAGE.TRANSFERING_DONE).to_bytes(4, 'little'))
    tickCount_frame = zmq.Frame(tickCount.to_bytes(4, 'little'))

    return [msgType_frame, tickCount_frame]







def CreateInputDisconenctMsg():
     
    masgType_frame = zmq.Frame(int(src_IPC_MESSAGE.INPUT_DISCONNECT).to_bytes(4, 'little'))
    
    return [masgType_frame]


def CreateInputReadyMsg(peerRoutingID):

    routingID_frame = zmq.Frame(peerRoutingID)

    msgType_frame = zmq.Frame(int(src_IPC_MESSAGE.INPUT_READY).to_bytes(4, 'little'))
    


    return [routingID_frame, msgType_frame]

def CreateReceivedDataMsg(tickCount, peerRoutingID):
     
    routingID_frame = zmq.Frame(peerRoutingID)
    
    msgType_frame   = zmq.Frame(int(src_IPC_MESSAGE.RECEIVED_DATA).to_bytes(4, 'little'))
    tickCount_frame =  zmq.Frame(tickCount.to_bytes(4, 'little'))

    return [routingID_frame, msgType_frame, tickCount_frame]

