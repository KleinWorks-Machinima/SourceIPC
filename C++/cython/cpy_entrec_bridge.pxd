


from libcpp.list   cimport list
from libcpp.string cimport string




cdef extern from "../src/EntRecBridge/EntRecBridge.h":
    cdef cppclass Vector_t:
        Vector_t()
        char* name
        float x
        float y
        float z
    
    cdef cppclass Quaternion_t:
        Quaternion_t()
        char* name
        float w
        float x
        float y
        float z

    cdef cppclass ParsedEntData_t:
        ParsedEntData_t()
        int                ent_id
        int                engine_tick_count
        list[Vector_t]     ent_pos
        list[Quaternion_t] ent_rot

    cdef cppclass ParsedEntMetaData_t:
        ParsedEntMetaData_t()
        int         ent_id
        int         ent_type
        int         ent_numbones
        int         ent_parent_id
        char*       ent_name
        char*       ent_model

    cdef cppclass ParsedEntEvent_t:
        ParsedEntEvent_t()
        int                 event_type
        int                 ent_id
        ParsedEntMetaData_t ent_metadata

    cdef cppclass RecordedFrame_t:
        RecordedFrame_t()
        int                    frame_num
        list[ParsedEntEvent_t] recorded_events
        list[ParsedEntData_t]  recorded_entdata
        
    cdef cppclass EntRecBridge:
        EntRecBridge()
        int                        m_sv_lasttick
        int                        m_cl_lasttick
        int                        mb_record
        list[RecordedFrame_t]      m_parsed_recording
        list[ParsedEntMetaData_t]  m_filtered_initial_metadata
        int                        ClientRecv(char* recvdMsg, int msgNum, int engineTickCount)
        int                        ServerRecv(char* recvdMsg, int msgNum, int engineTickCount)
        int                        ClientInitialMetadata(char* initialMetadata)
        int                        ServerInitialMetadata(char* initialMetadata)
        void                       ParseRawMsgData()
        void                       FilterParsedMessages()
        void                       ClearContents()