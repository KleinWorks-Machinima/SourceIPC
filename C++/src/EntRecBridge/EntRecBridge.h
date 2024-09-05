//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
//
// Purpose: 
// 
// Product Contributors: Barber
//
//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\

#include <iostream>
#include <list>
#include <math.h>
#include <string>

#include "InSourceOutSource.h"
#include "rapidjson/rapidjson.h"


#define KW_SV_INPUT_PORTNUM  5550
#define KW_SV_OUTPUT_PORTNUM 5577

#define KW_CL_INPUT_PORTNUM  5551
#define KW_CL_OUTPUT_PORTNUM 5533

using namespace srcIPC;


struct Vector_t { float x; float y; float z; };

struct Quaternion_t { float w; float x; float y; float z; };



struct RawMsg_t
{
	char*		ent_data;
	char*		ent_events;

	bool		has_events;
	int			frame_num;
	int			tick_count;

public:

	RawMsg_t(const char* msg_str, int frameNum, int engineTickCount);
};



// Recorded entity data. Contains position/rotation
// values, the frame number to animate this data on,
// and the ID of the entity this data belongs to.
struct ParsedEntData_t
{
	int						ent_id;
	int						engine_tick_count;
	std::list<Vector_t>		ent_pos;
	std::list<Quaternion_t>	ent_rot;

public:

	static ParsedEntData_t ParseFromJson(rapidjson::GenericObject<false, rapidjson::Value> ent_data_js, int engineTickCount);
};


// Entity metadata, everything Blender needs to know
// to animate that entity.
struct ParsedEntMetaData_t
{
	int				ent_id;
	int				ent_type;
	int				ent_numbones;
	int				ent_parent_id;
	char*			ent_name;
	char*			ent_model;

public:

	static ParsedEntMetaData_t ParseFromJson(rapidjson::Value ent_metadata_js);
};


// An entity event, incase something special happens
// mid recording, like an entity being destroyed/created,
// or entity becoming un-parented (ex. ent1 dies, so ent1's weapon becomes unparented).
struct ParsedEntEvent_t
{
	int					event_type;
	int					ent_id;
	ParsedEntMetaData_t	ent_metadata;

public:

	static ParsedEntEvent_t ParseFromJson(rapidjson::Value ent_event_js);
};


struct RecordedFrame_t
{
	int							frame_num;

	std::list<ParsedEntEvent_t>	recorded_events;
	std::list<ParsedEntData_t>	recorded_entdata;
};







class EntRecBridge
{
public:
	EntRecBridge();
	~EntRecBridge();

	/*======Member-Variables======*/
public:

	InSourceOutSource m_zmq_server = InSourceOutSource(KW_SV_OUTPUT_PORTNUM, KW_SV_INPUT_PORTNUM);
	InSourceOutSource m_zmq_client = InSourceOutSource(KW_CL_OUTPUT_PORTNUM, KW_CL_INPUT_PORTNUM);

public:

	int								m_sv_lasttick;
	int								m_cl_lasttick;

	bool							mb_record;


	// Populated by recorded frames during a recording.
	// When a new recording starts, this list is cleared of its contents.
	std::list<RecordedFrame_t>		m_parsed_recording;

	// The metadata of every entity in the latest recording.
	// When a new recording starts, this list is cleared of its contents.
	std::list<ParsedEntMetaData_t>  m_filtered_initial_metadata;

private:

	
	std::list<ParsedEntMetaData_t>  m_cl_initial_metadata;
	std::list<ParsedEntMetaData_t>  m_sv_initial_metadata;

	std::list<ParsedEntEvent_t>		m_sv_parsed_events;
	std::list<ParsedEntEvent_t>		m_cl_parsed_events;

	std::list<ParsedEntData_t>		m_sv_parsed_data;
	std::list<ParsedEntData_t>		m_cl_parsed_data;

	std::list<RawMsg_t>				m_sv_raw_messages;
	std::list<RawMsg_t>				m_cl_raw_messages;

	/*======Member-Functions======*/
public:

	// Listens for incoming messages from the Server and Client,
	// and passes recieved messages to ParseMsgData.
	// Returns -1 when not recording, returns 1 when recording and return 0 when a recording has finished.
	int				Run();

private:

	int				ClientRecv();
	int				ServerRecv();

	void			ParseRawMsgData();

	void			FilterParsedMessages();

};
