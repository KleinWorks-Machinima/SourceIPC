
# distutils: language = c++

from mathutils import Vector, Quaternion

from cpy_entrec_bridge cimport Vector_t            as c_Vector_t
from cpy_entrec_bridge cimport Quaternion_t        as c_Quaternion_t
from cpy_entrec_bridge cimport ParsedEntData_t     as c_ParsedEntData_t
from cpy_entrec_bridge cimport ParsedEntMetaData_t as c_ParsedEntMetaData_t
from cpy_entrec_bridge cimport ParsedEntEvent_t    as c_ParsedEntEvent_t
from cpy_entrec_bridge cimport RecordedFrame_t     as c_RecordedFrame_t
from cpy_entrec_bridge cimport EntRecBridge        as c_EntRecBridge



cdef class PyVector_t:
    cdef c_Vector_t m_vec

    def __init__(self):
        self.m_vec = c_Vector_t()


    def Get(self):

        return {str(self.m_vec.name, "UTF-8") : Vector((self.m_vec.x, self.m_vec.y, self.m_vec.z))}




cdef class PyQuaternion_t:
    cdef c_Quaternion_t m_quat
    
    def __init__(self):
        self.m_quat = c_Quaternion_t()


    def Get(self):
        
        return {str(self.m_quat.name, "UTF-8") : Quaternion((self.m_quat.w, self.m_quat.x, self.m_quat.y, self.m_quat.z))}




cdef class PyParsedEntData_t:
    cdef c_ParsedEntData_t m_parsed_entdata

    def __init__(self):
        self.m_parsed_entdata = c_ParsedEntData_t()


    # Attribute access
    @property
    def ent_id(self):
        return self.m_parsed_entdata.ent_id

    # Attribute access
    @property
    def engine_tick_count(self):
        return self.m_parsed_entdata.engine_tick_count

    # Attribute access
    @property
    def ent_pos(self):
        pos_list = {}

        cdef c_Vector_t c_vec
        for c_vec in self.m_parsed_entdata.ent_pos:
            pyVec = PyVector_t()
            pyVec.m_vec = c_vec

            pos_list.update(pyVec.Get())
        
        return pos_list

    # Attribute access
    @property
    def ent_rot(self):
        rot_list = {}

        cdef c_Quaternion_t c_quat
        for c_quat in self.m_parsed_entdata.ent_rot:
            pyQuat = PyQuaternion_t()
            pyQuat.m_quat = c_quat

            rot_list.update(pyQuat.Get())
        
        return rot_list




cdef class PyParsedEntMetaData_t:
    cdef c_ParsedEntMetaData_t m_parsed_metadata

    def __init__(self):
        self.m_parsed_metadata = c_ParsedEntMetaData_t()



    # Attribute access
    @property
    def ent_id(self):
        return self.m_parsed_metadata.ent_id

    # Attribute access
    @property
    def ent_type(self):
        return self.m_parsed_metadata.ent_type

    # Attribute access
    @property
    def ent_numbones(self):
        return self.m_parsed_metadata.ent_numbones

    # Attribute access
    @property
    def ent_parent_id(self):
        return self.m_parsed_metadata.ent_parent_id

    # Attribute access
    @property
    def ent_name(self):
        return str(self.m_parsed_metadata.ent_name, "UTF-8")

    # Attribute access
    @property
    def ent_model(self):
        return str(self.m_parsed_metadata.ent_model, "UTF-8")




cdef class PyParsedEntEvent_t:
    cdef c_ParsedEntEvent_t m_parsed_event


    def __init__(self):
        self.m_parsed_event = c_ParsedEntEvent_t()


    # Attribute access
    @property
    def ent_id(self):
        return self.m_parsed_event.ent_id

    # Attribute access
    @property
    def event_type(self):
        return self.m_parsed_event.event_type

    # Attribute access
    @property
    def ent_metadata(self):

        pyMetadata = PyParsedEntMetaData_t()
        pyMetadata.m_parsed_metadata = self.m_parsed_event.ent_metadata
        
        return pyMetadata




cdef class PyRecordedFrame_t:
    cdef c_RecordedFrame_t m_recorded_frame

    def __init__(self):
        self.m_recorded_frame = c_RecordedFrame_t()


    # Attribute access
    @property
    def frame_num(self):
        return self.m_recorded_frame.frame_num

    # Attribute access
    @property
    def recorded_events(self):

        event_list = []

        cdef c_ParsedEntEvent_t c_event
        for c_event in self.m_recorded_frame.recorded_events:
            pyEvent = PyParsedEntEvent_t()
            pyEvent.m_parsed_event = c_event

            event_list.append(pyEvent)
        
        return event_list

    # Attribute access
    @property
    def recorded_entdata(self):

        entdata_list = []

        cdef c_ParsedEntData_t c_entdata
        for c_entdata in self.m_recorded_frame.recorded_entdata:
            pyEntData = PyParsedEntData_t()
            pyEntData.m_parsed_entdata = c_entdata

            entdata_list.append(pyEntData)
        
        return entdata_list



cdef class PyEntRecBridge:
    cdef c_EntRecBridge m_bridge

    def __init__(self):
        self.m_bridge = c_EntRecBridge()


    def ClientRecv(self, recvdMsg , msgNum, engineTickCount):


        #cdef long long int c_msgNum          = msgNum
        #cdef long long int c_engineTickCount = engineTickCount
        
        return self.m_bridge.ClientRecv(recvdMsg, msgNum, engineTickCount)

    def ServerRecv(self, recvdMsg, msgNum, engineTickCount):


        #cdef long long int c_msgNum          = msgNum
        #cdef long long int c_engineTickCount = engineTickCount
        
        return self.m_bridge.ServerRecv(recvdMsg, msgNum, engineTickCount)

    
    def ClientInitialMetadata(self, frame_char):
        return self.m_bridge.ClientInitialMetadata(frame_char)

    def ServerInitialMetadata(self, frame_char):
        return self.m_bridge.ServerInitialMetadata(frame_char)


    def ParseRawMsgData(self):
        return self.m_bridge.ParseRawMsgData()

    def FilterParsedMessages(self):
        return self.m_bridge.FilterParsedMessages()

    def ClearContents(self):
        return self.m_bridge.ClearContents()


    # Attribute access
    @property
    def m_sv_lasttick(self):
        return self.m_bridge.m_sv_lasttick

    # Attribute access
    @property
    def m_cl_lasttick(self):
        return self.m_bridge.m_cl_lasttick

    # Attribute access
    @property
    def mb_record(self):
        return self.m_bridge.mb_record
    @mb_record.setter
    def mb_record(self, mb_record):
        self.m_bridge.mb_record = mb_record

    # Attribute access
    @property
    def m_filtered_initial_metadata(self):

        metadata_list = []

        cdef c_ParsedEntMetaData_t c_metadata
        for c_metadata in self.m_bridge.m_filtered_initial_metadata:
            pyMetadata = PyParsedEntMetaData_t()
            pyMetadata.m_parsed_metadata = c_metadata

            metadata_list.append(pyMetadata)
        
        return metadata_list

    @property
    def m_parsed_recording(self):

        parsed_recording_list = []

        cdef c_RecordedFrame_t c_frame
        for c_frame in self.m_bridge.m_parsed_recording:
            pyFrame = PyRecordedFrame_t()
            pyFrame.m_recorded_frame = c_frame

            parsed_recording_list.append(pyFrame)

        return parsed_recording_list