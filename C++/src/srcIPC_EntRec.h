#pragma once

#include "SourceIPC.h"
#include "InSourceOutSource.h"


namespace srcIPC {


	class srcIPC_EntRec : public InSourceOutSource
	{
	public:

		using InSourceOutSource::InSourceOutSource;
		using InSourceOutSource::~InSourceOutSource;



		/*======Member-Variables======*/






		/*======Member-Functions======*/


		rapidjson::Document FromFrameToJSON(zframe_t* data_frame);

		zframe_t*           FromJSONToFrame(rapidjson::Document js_Data);




	};

}