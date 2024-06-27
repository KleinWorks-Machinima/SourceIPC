#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
# 
#  Purpose: 
# 
#  Product Contributors: Barber
# 
#//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\


import zmq

if "bpy" in locals():
    import importlib
    importlib.reload(pysrcIPC_messages)
else:
    from . import pysrcIPC_messages

src_IPC_MESSAGE = pysrcIPC_messages.src_IPC_MESSAGE


class InSourceOutSource:

    def __init__(self, INPUTaddr, OUTPUTaddr) -> None:

        self.context = zmq.Context.instance()

        self.INPUTsocket  = self.context.socket(zmq.ROUTER)
        self.OUTPUTsocket = self.context.socket(zmq.DEALER)
        self.poller       = zmq.Poller()

        self.poller.register(self.INPUTsocket, zmq.POLLIN)
        self.poller.register(self.OUTPUTsocket, zmq.POLLIN)

        self.INPUTsocket.bind(INPUTaddr)
        self.OUTPUTsocket.connect(OUTPUTaddr)

        self.INPUTFuncLoop  = None
        self.OUTPUTFuncLoop = None

        self.OUTPUTtickCount = 0
        self.INPUTtickCount  = 0

        self.lastTickReceivedByPeer   = 0
        self.lastTickReceivedFromPeer = 0

        self.pollerTimeout = 1
        self.dropOutTolerance = 50

        self.peer_routing_ID = None

        self.isSendingOutput  = False
        self.isReceivingInput = False

        self.isDoneTransfering     = False
        self.peerIsDoneTransfering = False

        self.sendingDataBuffer      = None
        self.sendingMetaDataBuffer  = None

        self.receivedDataBuffer     = None
        self.receivedMetaDataBuffer = None

        self.currentINPUTStatus   = "Initialized."
        self.currentOUTPUTStatus = "Initialized."
        self.currentINPUTActivity = "Idle."
        self.currentOUTPUTActivity = "Idle."






    def RunFuncLoop(self):

        if self.INPUTFuncLoop != None:
            if self.INPUTFuncLoop(True)  == 0:
                self.INPUTFuncLoop = None

        
        if self.OUTPUTFuncLoop != None:
            if self.OUTPUTFuncLoop(True) == 0:
                self.OUTPUTFuncLoop  = None

        if self.OUTPUTFuncLoop == None and self.INPUTFuncLoop == None:
            return -1
        
        return 0
    




    def DisconnectSockets(self):
        pass





    

    def ConnectSockets(self, INPUTaddr, OUTPUTaddr):
        pass
        



        


    def OutputReady(self, isInFuncLoop=False):
        
        self.currentOUTPUTStatus = "Readying Output..."

        if isInFuncLoop == False:
            if self.OUTPUTFuncLoop == None:
                self.OUTPUTFuncLoop = self.OutputReady

            self.OUTPUTsocket.send_multipart(pysrcIPC_messages.CreateOutputReadyMsg())
            self.currentOUTPUTActivity = "Sent output ready message."



        # Poll every pending message
        
        pollResult = self.PollSocketForMessages(self.OUTPUTsocket)
        while pollResult != (None, None):

            if pollResult[0] == src_IPC_MESSAGE.INPUT_READY:
                self.isSendingOutput = True
                self.currentOUTPUTStatus = "Output readied!"
                self.currentOUTPUTActivity = "Idle."

                return 0

            if pollResult[0] == src_IPC_MESSAGE.INPUT_DISCONNECT:

                self.currentOUTPUTStatus = "Received INPUT_DISCONNECT message! Aborting..."

                self.isDoneTransfering = False
                self.isSendingOutput   = False

                self.currentOUTPUTActivity = "Idle."

                return 0


            if pollResult[0] == src_IPC_MESSAGE.NO_MESSAGE:
                self.currentOUTPUTStatus = "ERROR! Received NO_MESSAGE message! Something must have went wrong."
                self.currentOUTPUTActivity = "Idle."

            

            pollResult = self.PollSocketForMessages(self.OUTPUTsocket)

        self.currentOUTPUTActivity = "Awaiting InputReady message..."
        return -1






    def InputReady(self, isInFuncLoop=False):

        self.currentINPUTStatus = "Readying Input..."
        self.currentINPUTActivity = "Awaiting OutputReady message."
        if isInFuncLoop == False:
            if self.INPUTFuncLoop == None:
                self.INPUTFuncLoop = self.InputReady
        

        # Poll every pending message
        
        pollResult = self.PollSocketForMessages(self.INPUTsocket)
        while pollResult != (None, None):
            
            if pollResult[0] == src_IPC_MESSAGE.OUTPUT_READY:

                self.isReceivingInput = True
                self.currentINPUTStatus = "Input readied!"
                self.currentINPUTActivity = "Idle."
                self.peer_routing_ID = pollResult[1][0]

                self.INPUTsocket.send_multipart(pysrcIPC_messages.CreateInputReadyMsg(pollResult[1][0]))

                return 0


            if pollResult[0] == src_IPC_MESSAGE.OUTPUT_DISCONNECT:
                self.currentINPUTStatus   = "Received OUTPUT_DISCONNECT message! Aborting..."
                self.currentINPUTActivity = "Idle."

                self.isReceivingInput       = False
                self.peerIsDoneTransfering  = False
                self.INPUTtickCount         = 0
                return 0


            if pollResult[0] == src_IPC_MESSAGE.NO_MESSAGE:

                self.currentINPUTActivity = "ERROR! Received NO_MESSAGE message! Something must have went wrong."
                


            pollResult = self.PollSocketForMessages(self.INPUTsocket)

        
        return -1
    


    



    def TransferData(self, isInFuncLoop=False):

        if self.sendingDataBuffer == None:
            self.currentOUTPUTStatus   = "Failed to transfer data: Data buffer was empty."
            self.currentOUTPUTActivity = "Idle."
            self.isSendingOutput = False
            return 0
        
        if isInFuncLoop == False:
            self.OUTPUTFuncLoop = self.TransferData

        





        # Check if we are done transfering, if so end data transfer.
        if (self.isDoneTransfering != False):
            self.currentOUTPUTStatus = "Ending data transfer..."

            if (self.isSendingOutput != False):
                self.OUTPUTsocket.send_multipart(pysrcIPC_messages.CreateTransferingDoneMsg(self.OUTPUTtickCount))

                self.isSendingOutput = False

            self.currentOUTPUTActivity = "Waiting for peer to finish receiving data."
        
        elif self.isSendingOutput == False:
            self.currentOUTPUTActivity = "Readying output for data transfering..."
            if (self.OutputReady(isInFuncLoop) == -1):
                return -1
            
            self.OUTPUTtickCount = 0
            self.lastTickReceivedByPeer = 0

            self.OUTPUTsocket.send_multipart(pysrcIPC_messages.CreateTransferingDataMsg(self.OUTPUTtickCount, self.sendingMetaDataBuffer))

            return -1
        








        # Poll every pending message
        pollResult = self.PollSocketForMessages(self.OUTPUTsocket)
        while pollResult != (None, None):
            if pollResult[0] == src_IPC_MESSAGE.INPUT_DISCONNECT:
                self.currentOUTPUTStatus   = "Received INPUT_DISCONNECT message! Aborting..."

                self.isDoneTransfering = False
                self.isSendingOutput   = False

                self.currentOUTPUTActivity = "Idle."

                return 0

            if pollResult[0] == src_IPC_MESSAGE.RECEIVED_DATA:

                self.lastTickReceivedByPeer = int.from_bytes(pollResult[1][1], 'little')

                self.currentOUTPUTActivity = "Received a DataReceived message!"

                if self.isDoneTransfering != False:

                    if self.lastTickReceivedByPeer != self.OUTPUTtickCount:
                        self.currentOUTPUTActivity  = "Waiting for peer to finish receiving data."
                        return -1

                    self.currentOUTPUTActivity = "Idle."
                    self.currentOUTPUTStatus   = "Data transfer finished."

                    self.isDoneTransfering = False
                    return 0


            if pollResult[0] == src_IPC_MESSAGE.NO_MESSAGE:
                self.currentOUTPUTStatus   = "ERROR! Received NO_MESSAGE message! Something must have went wrong."
                self.currentOUTPUTActivity = "Idle."


            pollResult = self.PollSocketForMessages(self.OUTPUTsocket)













        self.currentOUTPUTStatus = "Actively transfering data..."

        self.OUTPUTtickCount += 1

        self.OUTPUTsocket.send_multipart(pysrcIPC_messages.CreateDataMsg(self.OUTPUTtickCount, self.sendingDataBuffer))
        self.currentOUTPUTActivity = "Sent a Data message."


        #  if tolerance is -1 then ignore drop-out checks.
        if self.dropOutTolerance == -1:
            return -1


        
        # for detecting peer connection dropouts...
        if abs(self.lastTickReceivedByPeer - self.OUTPUTtickCount) >= self.dropOutTolerance:
            self.currentOUTPUTActivity = "Error! Peer hasn't confirmed that it has received any recent ticks! Peer assumed to have dropped connection! Aborting..."
            self.currentOUTPUTStatus   = "ERROR. Didn't receive any confirmation of data transfer from peer."

            self.isSendingOutput = False
            self.OUTPUTtickCount = 0
            self.isDoneTransfering = False

            return 0


        
        return -1






    def ReceiveData(self, isInFuncLoop=False):
        
        if isInFuncLoop == False:
            self.INPUTFuncLoop = self.ReceiveData

        
        if self.isReceivingInput != True:
            if self.InputReady(isInFuncLoop) != 0:
                return -1
            self.INPUTtickCount = 0



        # check if peer is done transfering, if so try to end the data transfer
        if self.peerIsDoneTransfering == True:
                if self.INPUTtickCount == self.lastTickReceivedFromPeer:

                    
                    self.INPUTsocket.send_multipart(pysrcIPC_messages.CreateReceivedDataMsg(self.INPUTtickCount, self.peer_routing_ID))

                    self.currentINPUTStatus   = "All messages received from peer, data transfer ended."
                    self.currentINPUTActivity = "Idle."

                    self.isReceivingInput       = False
                    self.peerIsDoneTransfering  = False
                    self.INPUTtickCount         = 0
                    return 0
                
                self.currentINPUTStatus = "Haven't received all pending data messages, can't end data transfer yet."


        # for sending DATA_RECEIVED messages
        if self.INPUTtickCount != 0 and self.INPUTtickCount % (self.dropOutTolerance / 2) == 0:

            self.INPUTsocket.send_multipart(pysrcIPC_messages.CreateReceivedDataMsg(self.INPUTtickCount, self.peer_routing_ID))
            self.currentINPUTActivity = "Sent received data message."





        # Poll every pending message
        pollResult = self.PollSocketForMessages(self.INPUTsocket)
        while pollResult != (None, None):


            if pollResult[0] == src_IPC_MESSAGE.OUTPUT_DISCONNECT:
                self.currentINPUTStatus   = "Received OUTPUT_DISCONNECT message! Aborting..."
                self.currentINPUTActivity = "Idle."

                self.isReceivingInput       = False
                self.peerIsDoneTransfering  = False
                self.INPUTtickCount         = 0
                return 0


            if pollResult[0] == src_IPC_MESSAGE.TRANSFERING_DATA:

                self.currentINPUTActivity = "Received metadata message."
                self.currentINPUTStatus   = "Receiving data."
                    
                # this try-except block may be temporary, trying to fix a bug involving this exception
                try:
                    self.receivedMetaDataBuffer = bytes.decode(pollResult[1][3], 'utf-8')
                except UnicodeDecodeError as err:
                    print("ERROR OCCURED WHILE RECEIVING METADATA! Problem message is the following:")
                    print(str(pollResult[1][3]))

                    self.receivedMetaDataBuffer = bytes.decode(pollResult[1][3], 'utf-8', 'replace')

                    


            if pollResult[0] == src_IPC_MESSAGE.DATA_MESSAGE:

                self.currentINPUTActivity = "Received data message."
                
                self.receivedDataBuffer   = bytes.decode(pollResult[1][3], "utf-8")

                self.INPUTtickCount += 1

                return -1
                

            if pollResult[0] == src_IPC_MESSAGE.TRANSFERING_DONE:

                self.currentINPUTActivity  = "Received transfering done message."

                self.peerIsDoneTransfering = True

                self.lastTickReceivedFromPeer = int.from_bytes(pollResult[1][2], 'little')
                
                return -1


            if pollResult[0] == src_IPC_MESSAGE.NO_MESSAGE:

                self.currentINPUTActivity = "ERROR! Received NO_MESSAGE message! Something must have went wrong."

                


            pollResult = self.PollSocketForMessages(self.INPUTsocket)


        return -1






    def PollSocketForMessages(self, socketToPoll):

        events = dict(self.poller.poll(self.pollerTimeout))

        if socketToPoll in events and events[socketToPoll] == zmq.POLLIN:

            message = socketToPoll.recv_multipart(copy=True)
            assert(message[0])


            messageType = int.from_bytes(message[0], 'little')

            
            # first frame can only contain INPUT messages

            if messageType == src_IPC_MESSAGE.INPUT_DISCONNECT:
                return src_IPC_MESSAGE.INPUT_DISCONNECT, message
            
            if messageType == src_IPC_MESSAGE.INPUT_READY:
                return src_IPC_MESSAGE.INPUT_READY, message
            
            if messageType == src_IPC_MESSAGE.RECEIVED_DATA:
                return src_IPC_MESSAGE.RECEIVED_DATA, message
            

            messageType = int.from_bytes(message[1], 'little')
            assert(message[1])


            # second frame can only contain OUTPUT messages

            if messageType == src_IPC_MESSAGE.OUTPUT_DISCONNECT:
                return src_IPC_MESSAGE.OUTPUT_DISCONNECT, message
            
            if messageType == src_IPC_MESSAGE.OUTPUT_READY:
                return src_IPC_MESSAGE.OUTPUT_READY, message

            if messageType == src_IPC_MESSAGE.TRANSFERING_DATA:
                return src_IPC_MESSAGE.TRANSFERING_DATA, message
            
            if messageType == src_IPC_MESSAGE.DATA_MESSAGE:
                return src_IPC_MESSAGE.DATA_MESSAGE, message
            
            if messageType == src_IPC_MESSAGE.TRANSFERING_DONE:
                return src_IPC_MESSAGE.TRANSFERING_DONE, message

            # if the message is of no known message type
            if messageType == src_IPC_MESSAGE.NO_MESSAGE:
                return src_IPC_MESSAGE.NO_MESSAGE, None
        else:
            return None, None


            

            
        
            



        










