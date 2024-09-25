//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
//
// Purpose: 
// 
// Product Contributors: Barber
//
//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\

#include <iostream>
#include <list>
#include <vector>
#include <math.h>
#include <string>
#include <exception>

#include "czmq/czmq.h"
#include "rapidjson/rapidjson.h"
#include "rapidjson/Document.h"
#include "rapidjson/Writer.h"


const enum class ENTREC_EVENT : int
{
	ENT_CREATED = 0xE01,
	ENT_BROKEN = 0xE02,
	ENT_DELETED = 0xE03,

	EFFECT_CREATED = 0xE04,

	SOUND_CREATED = 0xE05,
};


struct Vector_t { char* name; float x; float y; float z; };

struct Quaternion_t { char* name; float w; float x; float y; float z; };



struct RawMsg_t
{
	char*		ent_data;
	char*		ent_events;

	bool		has_events;
	int			frame_num;
	int			tick_count;

public:

	RawMsg_t(char* msg_str, int frameNum, int engineTickCount);
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
	int				 ent_id;
	int			 	 ent_type;
	int			 	 ent_numbones;
	int			 	 ent_parent_id;
	char*			 ent_name;
	char*			 ent_model;

public:

	static ParsedEntMetaData_t ParseFromJson(rapidjson::Value ent_metadata_js);
};


// An entity event, incase something special happens
// mid recording, like an entity being destroyed/created,
// or entity becoming un-parented (ex. ent1 dies, so ent1's weapon becomes unparented).
struct ParsedEntEvent_t
{
	int					 event_type;
	int					 ent_id;
	int					 tick_count;
	ParsedEntMetaData_t	 ent_metadata;

	int					 sound_volume;
	int					 sound_pitch;
	float				 sound_time;
	char*				 sound_name;
	Vector_t			 sound_origin;
	std::list<Vector_t>  sound_origins;

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

	int								m_sv_lasttick;
	int								m_cl_lasttick;

	bool							mb_record;


	// Populated by recorded frames during a recording.
	// When a new recording starts, this list is cleared of its contents.
	std::vector<RecordedFrame_t>		m_parsed_recording;

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

	char*							m_cl_raw_initial_metadata;
	char*							m_sv_raw_initial_metadata;

	/*======Member-Functions======*/
public:

	int				ClientRecv(char* recvdMsg, int msgNum, int engineTickCount);
	int				ServerRecv(char* recvdMsg, int msgNum, int engineTickCount);

	int				ClientInitialMetadata(char* initialMetadata);
	int				ServerInitialMetadata(char* initialMetadata);


public:

	void			ParseRawMsgData();
	void			FilterParsedMessages();

	void			ClearContents();

};
