
import logging
import time
import ast
from typing import Dict, Any, List, Optional

#AgentHook 소스에 맞춰 수정
import sys
sys.path.append("/app/plugins/")

import grpc
import traceback

import hook_pb2
import hook_pb2_grpc


#TODO: logger는 기존 디노티시아 logger와 사용 방식 통일
logger = logging.getLogger(__name__)

'''
'''
################################################### grpc client

def grpc_error_handler(timeout:int = 15, error_retry:int = 3):

    def decorator(func):

        def wrapper(self, strRPCUrl:str, strGrpcMethodName:str, grpcRequest:Any, *args, **kwargs):

            for nTry in range(error_retry):

                try:
                    return func(self, strRPCUrl, strGrpcMethodName, grpcRequest, *args, timeout=timeout, **kwargs)
                
                except grpc.RpcError as e:

                    logger.error(traceback.format_exc())
                    time.sleep(1)

                except Exception as e:

                    logger.error(traceback.format_exc())
                    time.sleep(1)

            raise Exception('unknown grpc handller exception')
        
        return wrapper
    
    return decorator

class WinsGrpcClient:

    def __init__(self):

        self.__channel = None
        pass

    #서버 접속
    def __Connect(self, strRPCUrl:str):

        '''
        TODO: 이것까지 넣어야 한다. 예외처리는 같이, 우선 연결세션은 미고려
        '''

        self.__channel = grpc.insecure_channel(strRPCUrl)
        stub = hook_pb2_grpc.HookProxyStub(self.__channel)
        
        return stub

    #서버 종료
    def __Close(self, ):

        self.__channel.close()
    
    grpc_error_handler(timeout = 5, error_retry = 3)
    def call(self, strRPCUrl:str, strGrpcMethodName:str, request:Any, *args, **kwargs) -> Any:

        '''
        '''

        stub = self.__Connect(strRPCUrl)
        
        method = getattr(stub, strGrpcMethodName)

        response:Any = method(request, **kwargs)
        
        self.__Close()

        return response

################################################### 통신 client, main

class WinsSecurityClient:

    CONFIG_WINS_IP = "wins_ip"
    CONFIG_WINS_PORT = "wins_port"
    CONFIG_AGENT_ID = "agent_id"

    METHOD_HOOK_BROWSER_MESSAGE = "HookBrowserMessage"
    METHOD_HOOK_LLM_REQUEST = "HookLLMRequest"
    METHOD_HOK_MCP_CALL = "HookMCPCall"

    METHOD_HOOK_LLM_STREAM_CHUNK = "HookLLMStreamChunk"
    METHOD_HOOK_LLM_RESPONSE = "HookLLMResponse"
    METHOD_HOOK_MCP_RESPONSE = "HookMCPResponse"

    def __init__(self):

        #접속정보, default는 아래 값으로 설정, 업데이트 기능 제공
        self.__connectInfo = {
            
            WinsSecurityClient.CONFIG_WINS_IP : "127.0.0.1",
            WinsSecurityClient.CONFIG_WINS_PORT : 0,
            WinsSecurityClient.CONFIG_AGENT_ID : 0
        }

        self.__winsGrpcClient = WinsGrpcClient()
        pass

    ##################################### static
    
    @staticmethod
    def UtilGetModifiedStringData(strNewData:str, strOriginalData:str) -> str:

        '''
        '''

        if None == strNewData or 0 == len(strNewData):
            return strOriginalData
        
        return strNewData
        
    @staticmethod
    def UtilGetModifiedCollectionData(strNewData:str, lstOriginalData:Any) -> Any:

        '''
        '''

        if None == strNewData or 0 == len(strNewData):
            return lstOriginalData
        else:
            
            anyNewData = ast.literal_eval(strNewData)
            return anyNewData


    ##################################### public

    #데이터 초기화
    def Initialize(self, dictLocalConfig:dict):

        '''
        기본 정보 초기화, 업데이트 기능도 향후 제공
        '''
        self.UpdateServerConfig(dictLocalConfig)
        pass

    #접속정보, 업데이트 기능 제공
    def UpdateServerConfig(self, dictUpdateConfig:dict):
        '''
        '''

        self.__connectInfo = dictUpdateConfig
        pass

    def GetServerConfig(self, strKey:str) -> Any:
        '''
        '''

        return self.__connectInfo.get(strKey, None)

    #데이터 전송
    def SendToWinsServer(self, strGrpcMethodName:str, request:Any) -> Any:

        '''
        '''

        strServerIP = str(self.__connectInfo.get(WinsSecurityClient.CONFIG_WINS_IP))
        nPort = int(self.__connectInfo.get(WinsSecurityClient.CONFIG_WINS_PORT))

        strRPCUrl:str = f"{strServerIP}:{nPort}"
        
        response:Any = self.__winsGrpcClient.call(strRPCUrl, strGrpcMethodName, request)
        return response
    
################################################### customize, Hook Request

'''
Agent Hook에서 전달할 Browser Request 객체 반환
'''

class WinsHookRequestCustomizeHelper:

    def __init__(self):
        pass

    @staticmethod
    def BrowserHookRequest(winsSecurityClient:WinsSecurityClient, 
        query: str, 
        session_id: Optional[str], 
        user_role: Optional[str]
        ) -> Any:

        '''
        '''

        nAgentID:int = winsSecurityClient.GetServerConfig(WinsSecurityClient.CONFIG_AGENT_ID)

        request = hook_pb2.BrowserHookRequest(
            request_id = "0",
            agent_id = nAgentID,

            query = query,
            session_id = session_id,
            user_role = user_role
        )

        return request

    @staticmethod
    def LLMRequest(winsSecurityClient:WinsSecurityClient, 
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int,
        stream: bool
        ) -> Any:

        '''
        '''

        nAgentID:int = winsSecurityClient.GetServerConfig(WinsSecurityClient.CONFIG_AGENT_ID)

        request = hook_pb2.LLMRequest(
            request_id = "0",
            agent_id = nAgentID,

            messages = str(messages),
            llm_key = llm_key,
            iteration = int(iteration),
            stream = stream
        )

        return request
    
    @staticmethod
    def MCPCallRequest(winsSecurityClient:WinsSecurityClient,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
        ) -> Any:

        '''
        '''

        nAgentID:int = winsSecurityClient.GetServerConfig(WinsSecurityClient.CONFIG_AGENT_ID)

        request = hook_pb2.MCPCallRequest(
            request_id = "0",
            agent_id = nAgentID,

            server_name = server_name,                
            tool_name = tool_name,
            arguments = str(arguments)
        )

        return request
    

    @staticmethod
    def LLMStreamChunkRequest(winsSecurityClient:WinsSecurityClient,
        chunk: str,
        accumulated_response: str,
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int
        ) -> Any:

        '''        
        '''

        nAgentID:int = winsSecurityClient.GetServerConfig(WinsSecurityClient.CONFIG_AGENT_ID)

        request = hook_pb2.LLMStreamChunkRequest(
            request_id = "0",
            agent_id = nAgentID,   
            chunk = chunk,
            accumulated_response = accumulated_response,
            messages = str(messages),
            llm_key = llm_key,
            iteration = iteration
        )

        return request
    

    @staticmethod
    def LLMResponseRequest(winsSecurityClient:WinsSecurityClient,
        response: str,
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int,
        stream: bool
        ) -> Any:

        '''
        '''

        nAgentID:int = winsSecurityClient.GetServerConfig(WinsSecurityClient.CONFIG_AGENT_ID)

        request = hook_pb2.LLMResponseRequest(
            request_id = "0",
            agent_id = nAgentID,   

            response = response,
            messages = str(messages),
            llm_key = llm_key,
            iteration = iteration,
            stream = stream
        )

        return request
    

    @staticmethod
    def MCPResponseRequest(winsSecurityClient:WinsSecurityClient,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
        response: Dict[str, Any]
        ) -> Any:

        '''
        '''

        nAgentID:int = winsSecurityClient.GetServerConfig(WinsSecurityClient.CONFIG_AGENT_ID)

        request = hook_pb2.MCPResponseRequest(
            request_id = "0",
            agent_id = nAgentID,  

            server_name = server_name,
            tool_name = tool_name,
            arguments = str(arguments),
            response = str(response)                      
        )

        return request


