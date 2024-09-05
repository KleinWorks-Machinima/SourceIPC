
# distutils: language = c++


from cpy_entrec_bridge cimport EntRecBridge        as c_EntRecBridge
from cpy_entrec_bridge cimport Vector_t            as c_Vector_t
from cpy_entrec_bridge cimport Quaternion_t        as c_Quaternion_t
from cpy_entrec_bridge cimport ParsedEntData_t     as c_ParsedEntData_t
from cpy_entrec_bridge cimport ParsedEntMetaData_t as c_ParsedEntMetaData_t
from cpy_entrec_bridge cimport ParsedEntEvent_t    as c_ParsedEntEvent_t
from cpy_entrec_bridge cimport RecordedFrame_t     as c_RecordedFrame_t


def EntRecBridgeTest():
    bridge_ptr = new c_EntRecBridge()
    try:
        print(bool(bridge_ptr.mb_record))
    finally:
        del bridge_ptr