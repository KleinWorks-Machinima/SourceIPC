


from libcpp.list cimport list




cdef extern from "../EntRecBridge/EntRecBridge.h":
    cdef cppclass Vector_t:
        float x
        float y
        float z
    
    cdef cppclass Quaternion_t:
        float w
        float x
        float y
        float z

    cdef cppclass ParsedEntData_t:
        int                ent_id
        int                engine_tick_count
        list[Vector_t]     ent_pos
        list[Quaternion_t] ent_rot

    cdef cppclass ParsedEntMetaData_t:
        int ent_id
        int ent_type
        int ent_numbones
        int ent_parent_id
        char* ent_name
        char* ent_model

    cdef cppclass ParsedEntEvent_t:
        int              event_type
        int              ent_id
        ParsedEntEvent_t ent_metadata

    cdef cppclass RecordedFrame_t:
        int frame_num
        list[ParsedEntEvent_t] recorded_events
        list[ParsedEntData_t]  recorded_entdata
        
    cdef cppclass EntRecBridge:
        EntRecBridge()
        int                        m_sv_lasttick
        int                        m_cl_lasttick
        int                        mb_record
        list[RecordedFrame_t]      m_parsed_recording
        list[ParsedEntMetaData_t]  m_filtered_initial_metadata
        int                        Run()