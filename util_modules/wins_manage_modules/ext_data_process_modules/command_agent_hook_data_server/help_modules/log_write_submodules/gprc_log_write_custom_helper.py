import orjson

from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.log_write_submodules.grpc_log_write_handler import GrpcLogWriteHandler

'''
grpc log, 파일 저장구조로 변경, customize helper

mongodb, kibana 등 상황에 따라 변경될수 있다. 그때 변환로직은 여기에서 담당.
'''

class GrpcLogWriteCustomHelper:

    def __init__(self):
        pass

    #Browser Hook 메시지 데이터를 File로 저장하기 위해서 전달한다.
    def AddBrowserHookMessageData(self,            
            nAgentID:int, 
            strPromptQuery:str, 
            strSessionID:str,
            strUserRule:str,
            bAllowed:bool,
            strModifiedQuery:str,
            strErrorMessage:str,
            strReason:str,
            strIndexNamePrefix:str,
            grpcLogWriteHandler:GrpcLogWriteHandler):

        '''
        수집된 request를 string으로 변환후, grpcLogWriter로 전달
        우선은 mongodb의 row별 full json형태로 변환한다. => 어떤 DB연동이냐에 따라 상이하다.
        포맷팅은 나중에, 우선 python에서 문자열을 만들어서 전달한다.
        '''

        #TODO: bool to json 모듈화
        nAllowed = CONFIG_OPT_ENABLE if True == bAllowed else CONFIG_OPT_DISABLE
        
        #TODO: index, 일자별로 하나가 추가된다는 가정으로 개발
        #이 부분은 아쉽지만, custom helper에서 약간의 하드코딩을 추가한다.
        #날짜에 대해서는 로그가 들어올때마다 계속 만드는 것으로 우선 처리, 아래 date, now를 재활용한다.
        
        now = datetime.datetime.now()
        
        #TODO: index 접두어는 외부에서 받아오고, index full name은 여기서 만드는 것으로 정한다.
        
        #이 연산은 줄이자.
        # strOpenSearchIndexFullName:str = self.__generateIndexFullName(strIndexNamePrefix, now)

        # if False == bAllowed:
        #     nAllowed = CONFIG_OPT_DISABLE   

        #TODO: 우선 dictionary에 담고, dictionary를 string으로 변환후 저장하는 형태로 개발
        dictLog = {
            "index" : self.__generateIndexFullName(strIndexNamePrefix, now),
            "agent_id" : nAgentID,
            "timestamp" : now.strftime("%Y-%m-%d %H:%M:%S"),
            "prompt" : strPromptQuery,
            "session_id" : strSessionID,
            "user_role" : strUserRule,
            "allowed" : nAllowed,
            "modified_prompt" : strModifiedQuery,
            "error_message" : strErrorMessage,
            "reason" : strReason            
        }

        return self.__addToLogHandler(dictLog, GrpcLogWriteHandler.TYPE_BROWSER_MESSAGE, grpcLogWriteHandler)
        
        # return ERR_OK TODO: error check
    
    def AddLLMRequestData(self,            
            nAgentID:int, 
            strMessage:str,
            strLLMKey:str,
            nIteration:int,
            bStream:bool,
            bAllowed:bool,
            strModifiedMessage:str,
            strIndexNamePrefix:str,
            grpcLogWriteHandler:GrpcLogWriteHandler):

        '''
        '''

        nAllowed = CONFIG_OPT_ENABLE if True == bAllowed else CONFIG_OPT_DISABLE
        
        # strOpenSearchIndexName:str = f""
        now = datetime.datetime.now()

        dictLog = {
            "index" : self.__generateIndexFullName(strIndexNamePrefix, now),
            "agent_id" : nAgentID,
            "timestamp" : now.strftime("%Y-%m-%d %H:%M:%S"),
            "message" : strMessage,
            "llm_key" : strLLMKey,
            "iteration" : nIteration,
            "stream" : bStream,
            "allowed" : nAllowed,
            "modified_message" : strModifiedMessage            
        }
        
        # strLogData:str = JsonHelper.GetJsonString(dictLog, False, 0)

        # #TODO: 저장시, 로그 타입을 선언하여 전달. 로그 타입으로 Writer를 구분하여 관리하는 구조로 고려
        # grpcLogWriteHandler.AddData(GrpcLogWriteHandler.TYPE_BROWSER_MESSAGE, strLogData)

        return self.__addToLogHandler(dictLog, GrpcLogWriteHandler.TYPE_LLM_REQUEST, grpcLogWriteHandler)

        # return ERR_OK
    
    def AddMCPCallRequestData(self,
            nAgentID:int, 
            strServerName:str,
            strToolName:str,
            strArgument:str,
            bAllowed:bool,
            strModifiedArgument:str,
            strIndexNamePrefix:str,
            grpcLogWriteHandler:GrpcLogWriteHandler):

        '''
        '''

        nAllowed = CONFIG_OPT_ENABLE if True == bAllowed else CONFIG_OPT_DISABLE
        
        # strOpenSearchIndexName:str = f""
        now = datetime.datetime.now()

        dictLog = {
            "index" : self.__generateIndexFullName(strIndexNamePrefix, now),
            "agent_id" : nAgentID,
            "timestamp" : now.strftime("%Y-%m-%d %H:%M:%S"),
            "server_name" : strServerName,
            "tool_name" : strToolName,
            "argument" : strArgument,
            "allowed" : nAllowed,
            "modified_argument" : strModifiedArgument,                      
        }
        
        return self.__addToLogHandler(dictLog, GrpcLogWriteHandler.TYPE_MCP_CALL, grpcLogWriteHandler)
    
    def AddLLMStreamChunkData(self,            
            nAgentID:int, 
            strChunk:str,
            strAccumResponse:str,
            strMessages:str,
            strLLMKey:str,
            nIteration:int,
            bAllowed:bool,
            strModifiedChunk:str,
            bStopStream:bool,
            strIndexNamePrefix:str,
            grpcLogWriteHandler:GrpcLogWriteHandler):

        '''
        '''

        nAllowed = CONFIG_OPT_ENABLE if True == bAllowed else CONFIG_OPT_DISABLE
        
        # strOpenSearchIndexName:str = f""
        now = datetime.datetime.now()

        dictLog = {
            "index" : self.__generateIndexFullName(strIndexNamePrefix, now),
            "agent_id" : nAgentID,
            "timestamp" : now.strftime("%Y-%m-%d %H:%M:%S"),
            "chunk" : strChunk,
            "accumulated_response" : strAccumResponse,
            "message" : strMessages,
            "llm_key" : strLLMKey,
            "iteration" : nIteration,
            "allowed" : nAllowed,
            "modified_chunk" : strModifiedChunk,
            "stop_stream" : bStopStream
        }
        
        return self.__addToLogHandler(dictLog, GrpcLogWriteHandler.TYPE_LLM_STREAM_CHUNK, grpcLogWriteHandler)

    
    def AddLLMResponseData(self,            
            nAgentID:int, 
            strResponse:str,
            strMessage:str,
            strLLMKey:str,
            nIteration:int,
            bStream:bool,
            bAllowed:bool,
            strModifiedResponse:str,
            strIndexNamePrefix:str,
            grpcLogWriteHandler:GrpcLogWriteHandler):

        '''
        '''

        nAllowed = CONFIG_OPT_ENABLE if True == bAllowed else CONFIG_OPT_DISABLE
        
        # strOpenSearchIndexName:str = f""
        now = datetime.datetime.now()

        dictLog = {
            "index" : self.__generateIndexFullName(strIndexNamePrefix, now),
            "agent_id" : nAgentID,
            "timestamp" : now.strftime("%Y-%m-%d %H:%M:%S"),
            "response" : strResponse,
            "message" : strMessage,
            "llm_key" : strLLMKey,
            "iteration" : nIteration,
            "stream" : bStream,
            "allowed" : nAllowed,
            "modified_response" : strModifiedResponse           
        }
        
        return self.__addToLogHandler(dictLog, GrpcLogWriteHandler.TYPE_LLM_RESPONSE, grpcLogWriteHandler)

    
    def AddMCPResponseData(self,            
            nAgentID:int, 
            strServerName:str,
            strToolName:str,
            strArgument:str,
            strResponse:str,
            bAllowed:bool,
            strModifiedResponse:str,
            strIndexNamePrefix:str,
            grpcLogWriteHandler:GrpcLogWriteHandler):

        '''
        '''

        nAllowed = CONFIG_OPT_ENABLE if True == bAllowed else CONFIG_OPT_DISABLE
        
        # strOpenSearchIndexName:str = f""
        now = datetime.datetime.now()

        dictLog = {
            "index" : self.__generateIndexFullName(strIndexNamePrefix, now),
            "agent_id" : nAgentID,
            "timestamp" : now.strftime("%Y-%m-%d %H:%M:%S"),
            "server_name" : strServerName,
            "tool_name" : strToolName,
            "argument" : strArgument,
            "response" : strResponse,            
            "allowed" : nAllowed,
            "modified_response" : strModifiedResponse           
        }
        
        return self.__addToLogHandler(dictLog, GrpcLogWriteHandler.TYPE_MCP_RESPONSE, grpcLogWriteHandler)
    

    ###################################### private

    def __addToLogHandler(self, dictLog:dict, strType:str, grpcLogWriteHandler:GrpcLogWriteHandler):

        '''
        '''

        #TODO: 이시점에, 고속처리를 수행하기 위해 json대신 orjson을 사용한다.
        # strLogData:str = JsonHelperX.GetJsonString(dictLog, False, 0)
        # strLogData:str = JsonHelperX.GetJsonString(dictLog, False, 0)
        
        #속도 문제, bytearray로 변경
        byteLogData:bytes = orjson.dumps(dictLog)
        
        #마지막에 byte, 개행 추가
        byteLogData += b'\n'

        #TODO: 저장시, 로그 타입을 선언하여 전달. 로그 타입으로 Writer를 구분하여 관리하는 구조로 고려
        return grpcLogWriteHandler.AddData(strType, byteLogData)

        # return ERR_OK TODO: error check
        
    #opensearch index에 대한 전체 이름을 생성한다.
    def __generateIndexFullName(self, strIndexPrefix:str, now:datetime.datetime):
        
        '''
        '''
        
        #두개의 time 형식을 만들어야 하는 문제. 최대한 공통화 해보자.
        #TODO: 한줄이기는 하나, 이건 함수로 만들자.
        strDateYMD = now.strftime("%Y-%m-%d")
        strOpenSearchIndexName:str = f"{strIndexPrefix}-{strDateYMD}"
        
        return strOpenSearchIndexName

