//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
//
// Purpose: 
// 
// Product Contributors: Barber
//
//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\

#include "EntRecBridge.h"



RawMsg_t::RawMsg_t(char* msg_str, int frameNum, int engineTickCount)
{
	rapidjson::Document msg_js;

	msg_js.SetObject();

	msg_js.Parse(msg_str);


	// convert the entity data document into a string
	rapidjson::StringBuffer entDataStrBuffer;
	rapidjson::Writer<rapidjson::StringBuffer> entDataWriter(entDataStrBuffer);
	msg_js["ent_data"].Accept(entDataWriter);

	ent_data = new char[entDataStrBuffer.GetSize() + 1];

	strcpy_s(ent_data, entDataStrBuffer.GetSize() + 1, entDataStrBuffer.GetString());

	if (msg_js.HasMember("ent_events")) {
		has_events = true;

		rapidjson::StringBuffer entEventsStrBuffer;
		rapidjson::Writer<rapidjson::StringBuffer> entEventsWriter(entEventsStrBuffer);
		msg_js["ent_events"].Accept(entEventsWriter);

		ent_events = new char[entEventsStrBuffer.GetSize() + 1];

		strcpy_s(ent_events, entEventsStrBuffer.GetSize() + 1, entEventsStrBuffer.GetString());
		printf("RawMsg_t: ent_events = %s.\n", ent_events);
	}
	else
		has_events = false;

	frame_num  = frameNum;
	tick_count = engineTickCount;

}





ParsedEntData_t ParsedEntData_t::ParseFromJson(rapidjson::GenericObject<false, rapidjson::Value> ent_data_js, int engineTickCount)
{
	ParsedEntData_t parsedData;



	parsedData.ent_id = ent_data_js["ent_id"].GetInt();


	// this entity might have bones, so check if it has more than one vector under ent_pos
	for (auto& vec_js : ent_data_js["ent_pos"].GetObjectW()) {
		Vector_t vec;

		vec.x = vec_js.value["x"].GetFloat();
		vec.y = vec_js.value["y"].GetFloat();
		vec.z = vec_js.value["z"].GetFloat();

		vec.name = new char[strlen(vec_js.name.GetString()) + 1];
		strcpy_s(vec.name, strlen(vec_js.name.GetString()) + 1, vec_js.name.GetString());

		parsedData.ent_pos.push_back(vec);
	}

	for (auto& quat_js : ent_data_js["ent_rot"].GetObjectW()) {
		Quaternion_t quat;

		quat.w = quat_js.value["w"].GetFloat();
		quat.x = quat_js.value["x"].GetFloat();
		quat.y = quat_js.value["y"].GetFloat();
		quat.z = quat_js.value["z"].GetFloat();

		quat.name = new char[strlen(quat_js.name.GetString()) + 1];
		strcpy_s(quat.name, strlen(quat_js.name.GetString()) + 1, quat_js.name.GetString());

		parsedData.ent_rot.push_back(quat);
	}


	parsedData.engine_tick_count = engineTickCount;


	return parsedData;
}




ParsedEntMetaData_t ParsedEntMetaData_t::ParseFromJson(rapidjson::Value ent_metadata_js)
{
	ParsedEntMetaData_t parsedMetadata;


	parsedMetadata.ent_id       = ent_metadata_js["ent_id"].GetInt();
	parsedMetadata.ent_type     = ent_metadata_js["ent_type"].GetInt();
	parsedMetadata.ent_numbones = ent_metadata_js["ent_numbones"].GetInt();


	if (ent_metadata_js.HasMember("ent_parent_id"))
		parsedMetadata.ent_parent_id = ent_metadata_js["ent_parent_id"].GetInt();
	else
		parsedMetadata.ent_parent_id = parsedMetadata.ent_id;
			

	parsedMetadata.ent_name  = new char[strlen(ent_metadata_js["ent_name"].GetString()) + 1];
	parsedMetadata.ent_model = new char[strlen(ent_metadata_js["ent_model"].GetString()) + 1];

	strcpy_s(parsedMetadata.ent_name, strlen(ent_metadata_js["ent_name"].GetString()) + 1, ent_metadata_js["ent_name"].GetString());
	strcpy_s(parsedMetadata.ent_model, strlen(ent_metadata_js["ent_model"].GetString()) + 1, ent_metadata_js["ent_model"].GetString());

	return parsedMetadata;
}




ParsedEntEvent_t ParsedEntEvent_t::ParseFromJson(rapidjson::Value ent_event_js)
{

	ParsedEntEvent_t parsedEvent;

	parsedEvent.event_type= ent_event_js["event_type"].GetInt();
	parsedEvent.ent_id	   = ent_event_js["ent_id"].GetInt();
	parsedEvent.tick_count = ent_event_js["tick_count"].GetInt();


	if (parsedEvent.event_type == static_cast<int>(ENTREC_EVENT::ENT_CREATED)) {

	}

	if (parsedEvent.event_type == static_cast<int>(ENTREC_EVENT::ENT_DELETED)) {

	}

	if (parsedEvent.event_type == static_cast<int>(ENTREC_EVENT::SOUND_CREATED)) {

		parsedEvent.sound_name = new char[strlen(ent_event_js["sound_name"].GetString() + 1)];
		strcpy_s(parsedEvent.sound_name, strlen(ent_event_js["sound_name"].GetString()) + 1, ent_event_js["sound_name"].GetString());

		parsedEvent.sound_volume = ent_event_js["sound_volume"].GetInt();
		parsedEvent.sound_pitch  = ent_event_js["sound_pitch"].GetInt();
		parsedEvent.sound_time   = ent_event_js["sound_time"].GetFloat();

		parsedEvent.sound_origin.x = ent_event_js["sound_origin"].GetObjectW()["x"].GetFloat();
		parsedEvent.sound_origin.y = ent_event_js["sound_origin"].GetObjectW()["y"].GetFloat();
		parsedEvent.sound_origin.z = ent_event_js["sound_origin"].GetObjectW()["z"].GetFloat();

		for (auto& vec_js : ent_event_js["sound_origins"].GetObjectW()) {
			Vector_t vec;

			vec.x = vec_js.value["x"].GetFloat();
			vec.y = vec_js.value["y"].GetFloat();
			vec.z = vec_js.value["z"].GetFloat();

			vec.name = new char[strlen(vec_js.name.GetString()) + 1];
			strcpy_s(vec.name, strlen(vec_js.name.GetString()) + 1, vec_js.name.GetString());

			parsedEvent.sound_origins.push_back(vec);
		}
	}



	// if the event contains metadata, parse it
	if (ent_event_js.HasMember("ent_metadata"))
		parsedEvent.ent_metadata = ParsedEntMetaData_t::ParseFromJson(ent_event_js["ent_metadata"].GetObjectW());


	return parsedEvent;
}



EntRecBridge::EntRecBridge()
{
	m_cl_lasttick = 0;
	m_sv_lasttick = 0;
	mb_record	  = false;
}


EntRecBridge::~EntRecBridge()
{

}




int EntRecBridge::ClientRecv(char* recvdMsg, int msgNum, int engineTickCount)
{
	char* msg = new char[strlen(recvdMsg) + 1];

	strcpy_s(msg, strlen(recvdMsg) + 1, recvdMsg);
	
	m_cl_raw_messages.push_back(RawMsg_t::RawMsg_t(msg, msgNum, engineTickCount));

	return 1;
}




int EntRecBridge::ServerRecv(char* recvdMsg, int msgNum, int engineTickCount)
{
	char* msg = new char[strlen(recvdMsg) + 1];

	strcpy_s(msg, strlen(recvdMsg) + 1, recvdMsg);
	
	m_sv_raw_messages.push_back(RawMsg_t::RawMsg_t(msg, msgNum, engineTickCount));

	return 1;
}




int EntRecBridge::ClientInitialMetadata(char* initialMetadata)
{
	m_cl_raw_initial_metadata = new char[strlen(initialMetadata) + 1];

	strcpy_s(m_cl_raw_initial_metadata, strlen(initialMetadata) + 1, initialMetadata);

	return 1;
}




int EntRecBridge::ServerInitialMetadata(char* initialMetadata)
{
	m_sv_raw_initial_metadata = new char[strlen(initialMetadata) + 1];

	strcpy_s(m_sv_raw_initial_metadata, strlen(initialMetadata) + 1, initialMetadata);

	return 1;
}




void EntRecBridge::ParseRawMsgData()
{
	rapidjson::Document cl_raw_metadata;
	rapidjson::Document sv_raw_metadata;

	printf("step 1. parse metadata\n");
	// step 1. parse metadata


	cl_raw_metadata.SetObject();
	sv_raw_metadata.SetObject();

	cl_raw_metadata.Parse(m_cl_raw_initial_metadata);
	sv_raw_metadata.Parse(m_sv_raw_initial_metadata);

	/*
	auto cl_ent_js = cl_raw_metadata.Begin();
	auto sv_ent_js = sv_raw_metadata.Begin();

	for (; cl_ent_js != cl_raw_metadata.End() && sv_ent_js != sv_raw_metadata.End(); cl_ent_js++, sv_ent_js++) {
		m_cl_initial_metadata.push_back(ParsedEntMetaData_t::ParseFromJson(cl_ent_js->GetObjectW()));
		m_sv_initial_metadata.push_back(ParsedEntMetaData_t::ParseFromJson(sv_ent_js->GetObjectW()));
	}
	*/


	// first parse client-side
	for (auto& ent_js : cl_raw_metadata["ent_metadata"].GetObjectW())
		m_cl_initial_metadata.push_back(ParsedEntMetaData_t::ParseFromJson(ent_js.value.GetObjectW()));

	// then parse server-side
	for (auto& ent_js : sv_raw_metadata["ent_metadata"].GetObjectW())
		m_sv_initial_metadata.push_back(ParsedEntMetaData_t::ParseFromJson(ent_js.value.GetObjectW()));



	printf("step 2. parse raw messages\n");
	// step 2. parse raw messages


	// first parse client-side
	for (auto& raw_msg : m_cl_raw_messages) {
		rapidjson::Document raw_data_js;

		raw_data_js.SetObject();

		raw_data_js.Parse(raw_msg.ent_data);

		// first, parse the data
		for (auto& ent_js : raw_data_js.GetObjectW())
			m_cl_parsed_data.push_back(ParsedEntData_t::ParseFromJson(ent_js.value.GetObjectW(), raw_msg.tick_count));


		// next, check if there are any events, and then parse them

		if (!raw_msg.has_events)
			continue;

		rapidjson::Document raw_events_js;

		raw_events_js.SetObject();

		raw_events_js.Parse(raw_msg.ent_events);

		for (auto& event_js : raw_events_js.GetObjectW())
			m_cl_parsed_events.push_back(ParsedEntEvent_t::ParseFromJson(event_js.value.GetObjectW()));


	}


	// then parse server-side
	for (auto& raw_msg : m_sv_raw_messages) {
		rapidjson::Document raw_data_js;

		raw_data_js.SetObject();

		raw_data_js.Parse(raw_msg.ent_data);

		// first, parse the data
		for (auto& ent_js : raw_data_js.GetObjectW())
			m_sv_parsed_data.push_back(ParsedEntData_t::ParseFromJson(ent_js.value.GetObjectW(), raw_msg.tick_count));


		// next, check if there are any events, and then parse them

		if (!raw_msg.has_events)
			continue;

		rapidjson::Document raw_events_js;

		raw_events_js.SetObject();

		raw_events_js.Parse(raw_msg.ent_events);

		for (auto& event_js : raw_events_js.GetObjectW())
			m_sv_parsed_events.push_back(ParsedEntEvent_t::ParseFromJson(event_js.value.GetObjectW()));
	}




}



void EntRecBridge::FilterParsedMessages()
{
	// No filtering as of right now, just combines everything together

	for (auto& metadata : m_cl_initial_metadata)
		m_filtered_initial_metadata.push_back(metadata);

	for (auto& metadata : m_sv_initial_metadata)
		m_filtered_initial_metadata.push_back(metadata);

	int  cl_frameCount = 0;
	int  sv_frameCount = 0;

	printf("for (; cl_data != m_cl_parsed_data.end(); cl_data++, cl_frameCount++) { \n");
	for (auto& cl_data : m_cl_parsed_data) {
		RecordedFrame_t recordedFrame;

		recordedFrame.recorded_entdata.push_back(cl_data);

		recordedFrame.frame_num = cl_frameCount;

		m_parsed_recording.push_back(recordedFrame);

		cl_frameCount++;
	}
	printf("for (; sv_data != m_sv_parsed_data.end(); sv_data++, sv_frameCount++) {\n");
	for (auto& sv_data : m_sv_parsed_data) {
		RecordedFrame_t* recordedFrame;

		if (cl_frameCount > sv_frameCount) {
			recordedFrame = &m_parsed_recording[sv_frameCount];

			recordedFrame->recorded_entdata.push_back(sv_data);
		}
		else {
			recordedFrame = new RecordedFrame_t();
			recordedFrame->frame_num = sv_frameCount;
			recordedFrame->recorded_entdata.push_back(sv_data);
			m_parsed_recording.push_back(*recordedFrame);
		}
		sv_frameCount++;
	}



	printf("for (auto& sv_event : m_sv_parsed_events) {\n");
	for (auto& sv_event : m_sv_parsed_events) {
		RecordedFrame_t* recordedFrame;

		if (sv_frameCount == 0 && cl_frameCount == 0) {
			recordedFrame = new RecordedFrame_t();
			recordedFrame->frame_num = 0;
			recordedFrame->recorded_events.push_back(sv_event);
			m_parsed_recording.push_back(*recordedFrame);
		}
		else {
			recordedFrame = &m_parsed_recording[0];

			recordedFrame->recorded_events.push_back(sv_event);
		}
	}

	for (auto& cl_event : m_cl_parsed_events) {
		RecordedFrame_t* recordedFrame;

		if (sv_frameCount == 0 && cl_frameCount == 0) {
			recordedFrame = new RecordedFrame_t();
			recordedFrame->frame_num = 0;
			recordedFrame->recorded_events.push_back(cl_event);
			m_parsed_recording.push_back(*recordedFrame);
		}
		else {
			recordedFrame = &m_parsed_recording[0];

			recordedFrame->recorded_events.push_back(cl_event);
		}
	}
}





void EntRecBridge::ClearContents()
{
	m_sv_lasttick = 0;
	m_cl_lasttick = 0;

	m_parsed_recording.clear();
	m_filtered_initial_metadata.clear();

	m_sv_initial_metadata.clear();
	m_cl_initial_metadata.clear();

	m_sv_parsed_events.clear();
	m_cl_parsed_events.clear();

	m_sv_parsed_data.clear();
	m_cl_parsed_data.clear();

	m_sv_raw_messages.clear();
	m_cl_raw_messages.clear();

	m_cl_raw_initial_metadata = NULL;
	m_sv_raw_initial_metadata = NULL;
}