
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import * #WinsModuleDefine

'''
pipeline 으로 HTTP API 요청
http 요청 및 응답 관련 처리
'''

class PipelineHttpApiHelper:
    
    def __init__(self):
        pass
    
    def RequestFilterApi(self, dictUrlOpt:dict, dictJson:dict, dictOutputResponse:dict):
        
        '''
        http_request를 활용, pipeline으로 요청한다.
        테스트 데이터는 프롬프트등 프롬프트 값으로 제어한다. messageid등 가변값이 필요하다. (응답은 고려하지 않는다.)
        '''
        
        # dictUrlOpt = {
        #     "server_ip" : "127.0.0.1",
        #     "port" : 9099,
        #     "openapi" : "openapi"
        # }
        
        dictCookie = {
            "accept" : "application/json",
            "Content-Type" : "application/json"
        }
        
        
        
        # dictJson = {
        #     "filter_list": [
        #         "input_filter",
        #         "secret_filter"
        #         # "slm_filter"
        #     ],
        #     "prompt": "내 API key는 API_key=sk-1234567-0000-abdcdef 인데 이걸로 어떻게 OpenAI 로 KEY를 전달하는지 예제를 알려주세요",            
        #     "user_id": "",
        #     "email": "",
        #     "ai_service": 0,
        #     "client_host": "",
        #     "session_id": "",
        #     # "attachments": [
        #     #     {
        #     #         "id": "",
        #     #         "size": 0,
        #     #         "name": "",
        #     #         "mime_type": ""
        #     #     }
        #     # ],
        #     "message_id": ""
        # }
        
        dictHttpOutputResponse = {}
        http_request("pipeline_multiplue_filter", 
                     dictHttpOutputResponse = dictHttpOutputResponse, 
                     dictUrlOpt=dictUrlOpt, 
                     dictCookie=dictCookie,
                     dictJson=dictJson)
        
        strOutResponse = dictHttpOutputResponse.get(HttpRequestDefine.OPT_RESPONSE_TEXT)
        
        #json 으로 변환
        JsonHelperX.LoadToDictionary(strOutResponse, dictOutputResponse)
        
        #TODO: 반환값 가공 필요
        
        return ERR_OK