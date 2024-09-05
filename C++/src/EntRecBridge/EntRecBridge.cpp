//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\
//
// Purpose: 
// 
// Product Contributors: Barber
//
//===================| PROPERTY OF THE KLEINWORKS™ CORPORTATION®® |===================\\

#include "EntRecBridge.h"



RawMsg_t::RawMsg_t(const char* msg_str, int frameNum, int engineTickCount)
{
	rapidjson::Document msg_js;

	msg_js.SetObject();

	msg_js.Parse(msg_str);


	// convert the entity data document into a string
	rapidjson::StringBuffer strBuffer;
	rapidjson::Writer<rapidjson::StringBuffer> writer(strBuffer);
	msg_js["ent_data"].Accept(writer);

	ent_data = new char[strBuffer.GetSize() + 1];

	strcpy_s(ent_data, strBuffer.GetSize() + 1, strBuffer.GetString());

	if (msg_js.HasMember("ent_events")) {
		has_events = true;

		msg_js["ent_events"].Accept(writer);

		ent_events = new char[strBuffer.GetSize() + 1];

		strcpy_s(ent_events, strBuffer.GetSize() + 1, strBuffer.GetString());
	}
	else
		has_events = false;

	frame_num = frameNum;
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

		parsedData.ent_pos.push_back(vec);
	}

	for (auto& quat_js : ent_data_js["ent_rot"].GetObjectW()) {
		Quaternion_t quat;

		quat.w = quat_js.value["w"].GetFloat();
		quat.x = quat_js.value["x"].GetFloat();
		quat.y = quat_js.value["y"].GetFloat();
		quat.z = quat_js.value["z"].GetFloat();

		parsedData.ent_rot.push_back(quat);
	}


	parsedData.engine_tick_count = engineTickCount;


	return parsedData;
}




ParsedEntMetaData_t ParsedEntMetaData_t::ParseFromJson(rapidjson::Value ent_metadata_js)
{
	ParsedEntMetaData_t parsedMetadata;


	parsedMetadata.ent_id = ent_metadata_js["ent_id"].GetInt();
	parsedMetadata.ent_type = ent_metadata_js["ent_type"].GetInt();
	parsedMetadata.ent_numbones = ent_metadata_js["ent_numbones"].GetInt();

	if (ent_metadata_js.HasMember("ent_parent_id"))
		parsedMetadata.ent_parent_id = ent_metadata_js["ent_parent_id"].GetInt();
	else
		parsedMetadata.ent_parent_id = parsedMetadata.ent_id;

	parsedMetadata.ent_name = new char[strlen(ent_metadata_js["ent_name"].GetString()) + 1];
	parsedMetadata.ent_model = new char[strlen(ent_metadata_js["ent_model"].GetString()) + 1];

	strcpy_s(parsedMetadata.ent_name, strlen(ent_metadata_js["ent_name"].GetString()) + 1, ent_metadata_js["ent_name"].GetString());
	strcpy_s(parsedMetadata.ent_model, strlen(ent_metadata_js["ent_model"].GetString()) + 1, ent_metadata_js["ent_model"].GetString());

	return parsedMetadata;
}




ParsedEntEvent_t ParsedEntEvent_t::ParseFromJson(rapidjson::Value ent_event_js)
{

	ParsedEntEvent_t parsedEvent;

	parsedEvent.event_type = ent_event_js["event_type"].GetInt();
	parsedEvent.ent_id = ent_event_js["ent_id"].GetInt();


	// if the event contains metadata, parse it
	if (ent_event_js.HasMember("ent_metadata"))
		parsedEvent.ent_metadata = ParsedEntMetaData_t::ParseFromJson(ent_event_js["ent_metadata"].GetObjectW());


	return parsedEvent;
}



EntRecBridge::EntRecBridge()
{
}


EntRecBridge::~EntRecBridge()
{

}




int EntRecBridge::ClientRecv()
{
	bool cl_donetransfer = m_zmq_client.m_peerIsDoneTransfering;
	bool cl_isreceiving  = m_zmq_client.m_isReceivingInput;

	int  cl_INPUT_tickcount	 = m_zmq_client.m_INPUT_tick_count;
	int	 cl_ENGINE_tickcount = m_zmq_client.m_peer_ENGINE_tick_count;


	if (cl_donetransfer) {
		m_zmq_client.RunFuncLoop();
		return 0;
	}

	// if the last tick is less than the current tick, it means we received a message
	if (m_cl_lasttick < cl_INPUT_tickcount) {

		RawMsg_t rawMsg = RawMsg_t(zframe_strdup(m_zmq_client.m_received_data_buffer), cl_INPUT_tickcount, cl_ENGINE_tickcount);
		m_cl_raw_messages.push_back(rawMsg);
	}

	m_cl_lasttick = cl_INPUT_tickcount;

	int cl_return_num = m_zmq_client.RunFuncLoop();

	if (cl_return_num == -1) {
		m_zmq_client.ReceiveData();
		return -1;
	}

	if (!cl_isreceiving)
		return -1;
	else
		return 1;

}




int EntRecBridge::ServerRecv()
{
	bool sv_donetransfer = m_zmq_server.m_peerIsDoneTransfering;
	bool sv_isreceiving  = m_zmq_server.m_isReceivingInput;

	int  sv_INPUT_tickcount = m_zmq_server.m_INPUT_tick_count;
	int	 sv_ENGINE_tickcount = m_zmq_server.m_peer_ENGINE_tick_count;



	if (sv_donetransfer) {
		m_zmq_server.RunFuncLoop();
		return 0;
	}

	// if the last tick is less than the current tick, it means we received a message
	if (m_sv_lasttick < sv_INPUT_tickcount) {

		RawMsg_t rawMsg = RawMsg_t(zframe_strdup(m_zmq_server.m_received_data_buffer), sv_INPUT_tickcount, sv_ENGINE_tickcount);
		m_sv_raw_messages.push_back(rawMsg);
	}

	m_sv_lasttick = sv_INPUT_tickcount;

	int sv_return_num = m_zmq_server.RunFuncLoop();

	if (sv_return_num == -1)
		m_zmq_server.ReceiveData();
	
	if (!sv_isreceiving)
		return -1;
	else
		return 1;


}




int EntRecBridge::Run()
{
	int cl_code;
	int sv_code;

	cl_code = ClientRecv();
	sv_code = ServerRecv();

	if (cl_code != sv_code) {

		if (cl_code == 0 && sv_code == 1) 
			while (sv_code == 1)
				sv_code = ServerRecv();
		
		if (sv_code == 0 && cl_code == 1)
			while (cl_code == 1)
				cl_code = ClientRecv();
		
	}

	// if both are done recording, parse their messages
	if (cl_code == 0 && sv_code == 0) {

		ParseRawMsgData();
		FilterParsedMessages();

		return 0;
	}

	// if one is still recording, don't do anything
	if (cl_code == 1 || sv_code == 1)
		return 1;

	
	// if none of the if statements passed then we're not recording
	return -1;
}



void EntRecBridge::ParseRawMsgData()
{
	// step 1. parse metadata
	rapidjson::Document cl_raw_metadata;
	rapidjson::Document sv_raw_metadata;

	cl_raw_metadata.SetObject();
	sv_raw_metadata.SetObject();

	cl_raw_metadata.Parse(zframe_strdup(m_zmq_client.m_received_metadata_buffer));
	sv_raw_metadata.Parse(zframe_strdup(m_zmq_server.m_received_metadata_buffer));

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

		raw_events_js.AddMember("ent_events", raw_events_js.Parse(raw_msg.ent_events), raw_events_js.GetAllocator());

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

		raw_events_js.AddMember("ent_events", raw_events_js.Parse(raw_msg.ent_events), raw_events_js.GetAllocator());

		for (auto& event_js : raw_events_js.GetObjectW())
			m_sv_parsed_events.push_back(ParsedEntEvent_t::ParseFromJson(event_js.value.GetObjectW()));
	}


}



void EntRecBridge::FilterParsedMessages()
{
	// No filtering as of right now, just combines everything together

	printf("\ndebug_metadata_size = [%d]\n", m_cl_initial_metadata.size());
	printf("\ndebug_metadata_size = [%d]\n", m_sv_initial_metadata.size());
	printf("\ndebug_data_size = [%d]\n", m_cl_parsed_data.size());
	printf("\ndebug_data_size = [%d]\n", m_sv_parsed_data.size());

	for (auto& metadata : m_cl_initial_metadata) 
		m_filtered_initial_metadata.push_back(metadata);
	
	for (auto& metadata : m_sv_initial_metadata)
		m_filtered_initial_metadata.push_back(metadata);

	int frameCount = 0;
	auto cl_data   = m_cl_parsed_data.begin();
	auto sv_data   = m_sv_parsed_data.begin();

	for (; cl_data != m_cl_parsed_data.end() && sv_data != m_sv_parsed_data.end(); cl_data++, sv_data++, frameCount++) {
		RecordedFrame_t recordedFrame;

		recordedFrame.recorded_entdata.push_back(*cl_data);
		recordedFrame.recorded_entdata.push_back(*sv_data);

		recordedFrame.frame_num = frameCount;
		
		m_parsed_recording.push_back(recordedFrame);
	}

	cl_data++;
	sv_data++;
	frameCount++;

	RecordedFrame_t recordedFrame;

	recordedFrame.recorded_entdata.push_back(*cl_data);
	recordedFrame.recorded_entdata.push_back(*sv_data);

	recordedFrame.frame_num = frameCount;

	m_parsed_recording.push_back(recordedFrame);
}