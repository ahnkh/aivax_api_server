
import grpc
from functools import wraps

from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

# import hook_pb2
# import hook_pb2_grpc

from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.hook_pb2 import (
    BrowserHookResponse,
    LLMResponse,
    MCPCallResponse,
    LLMStreamChunkResponse,
    LLMResponseResponse,
    MCPResponseResponse
)

from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.hook_pb2_grpc import HookProxyServicer
from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.grpc_proxy_custom_helper import GrpcProxyCustomHelper

from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.log_write_submodules.grpc_log_write_handler import GrpcLogWriteHandler

'''
grpc 요청에 대한 proxy
TODO: 동시성 접근에 대한 처리 필요. Queue, lock
TODO: hook만 선언하고, 실제 호출은 별도 helper에서 관리한다.
'''

#예외처리 decorator, intercepter와 같이 사용
def grpc_error_handler(default_status=grpc.StatusCode.INTERNAL):
    '''
    gRPC 서비스 함수에 공통 예외 핸들러를 적용하는 데코레이터
    '''

    def decorator(func):
        
        @wraps(func)
        # def wrapper(self, request, context, *args, **kwargs):
        def wrapper(self, request, context):
            try:
                # return func(self, request, context, *args, **kwargs)
                return func(self, request, context)
            
            except grpc.RpcError as e:  # 이미 gRPC에서 발생한 예외는 그대로 전달

                LOG().error(traceback.format_exc())
                raise Exception(f"grpc - rpc error {e}")
            
            except Exception as e:
                
                # traceback.print_exc()
                LOG().error(traceback.format_exc())

                # 클라이언트에 에러 전달
                context.abort(default_status, f"Server Error: {e}")

        return wrapper
    
    return decorator

class GrpcProxy(HookProxyServicer):

    def __init__(self, ):

        #grpc 의 proxy이후 부가기능은 custom helper에서 처리
        self.__grpcProxyHelper = GrpcProxyCustomHelper()

        # 로그 저장 스레드, 스레드, 상태를 가지는 모듈.
        self.__grpcLogWriteHandler = None
        
        #설정정보, local config 정보의 참조
        self.__dictGrpcRecvServerCommandLocalConfig:dict = None
        pass

    #grpc 모듈 초기화.
    def Initialize(self, gprcLogWriteHandler:GrpcLogWriteHandler, dictGrpcRecvServerCommandLocalConfig:dict):

        '''
        '''

        self.__grpcLogWriteHandler = gprcLogWriteHandler
        
        self.__dictGrpcRecvServerCommandLocalConfig = dictGrpcRecvServerCommandLocalConfig

        return ERR_OK

    #on_browse_message 수신
    @grpc_error_handler()
    def HookBrowserMessage(self, request, context) -> BrowserHookResponse:

        '''
        TODO: 수집된 데이터는 그대로 DB에 저장 (분석 데이터는 Maria, 수집/통계는 no-sql을 검토.)
        TODO: 제어 데이터, request를 그대로 전달하지 않고, 가공된 값을 전달하도록 변경
        '''

        # LOG().debug(f"recv browser message hook, request = {request}")

        #TODO: request의 노출은 grpc_proxy로 제한한다.

        nAgentID:int = request.agent_id 
        strPromptQuery:str = request.query
        strSessionID:str = request.session_id

        #TODO: 사용자 계정, 세션, 권한 관리는 다시 검토 필요.
        strUserRule:str = request.user_role


        #허용여부, 설정의 제어는 FilterManager에서 수행후 결과 전달

        #TODO: 차단, 수정된 메시지 생성 => helper에서 반환한다.
        #TODO: PromptQuery , 필터 된 결과로 response, DB 결과 제어 로직 필요
        #2차로 개발, 우선은 response 와 allowed를 그냥 전달 한다.
        #약간의 customize => 부하 최소화, 응답이 없으면 기존 쿼리를 사용하도록 Hook쪽 수정
        # strModifiedQuery:str = "" #TODO: 차단여부, 수정된 쿼리에 대한 모듈화, ProxyHelper에서 처리

        (bAllowed, strModifiedQuery, strErrorMessage, strReason) = self.__grpcProxyHelper.FilterManager().FilterBrowserMessage(strPromptQuery, strUserRule)

        #helper는 기능별 분리, DB에 저장, 저장은 Bulk기능으로, 다시 위임 필요.
        #TODO: RDB저장은, 여기서는 수행하지 않는다. 로그가 남기 때문에, 2차로 향후 다른 곳에서 가능
        # dictDBResult = {}
        # self.__grpcProxyHelper.LocalCustomDBHelper().WriteBrowserHookMessageToDB(nAgentID, 
        #                                                                          strPromptQuery, 
        #                                                                          strSessionID, 
        #                                                                          strUserRule, 
        #                                                                          bAllowed, 
        #                                                                          strModifiedQuery, 
        #                                                                          strReason, 
        #                                                                          dictDBResult)

        #TODO: string으로 Log 저장 하는 기능 제공
        #alllowed, errormessage 까지 저장 => 인자가 늘어날때마다 다시 작업해야 하는 문제 개선 검토.
        #일단 디노티시아 모델은 이 형상으로 진행, index를 config에서 가져와야 하나, 우선 하드코딩, 향후 외부에서 설정하도록 변경한다.
        strIndexNamePrefix:str = "browser-message"
        #TODO: 로그명으로 index 지정, 아쉽지만 보류, 일단 소스코드는 유지
        
        self.__grpcProxyHelper.GrpcLogWriteCustomHelper().AddBrowserHookMessageData(
                                                                                    nAgentID, 
                                                                                    strPromptQuery, 
                                                                                    strSessionID, 
                                                                                    strUserRule, 
                                                                                    bAllowed, 
                                                                                    strModifiedQuery, 
                                                                                    strErrorMessage, 
                                                                                    strReason,
                                                                                    strIndexNamePrefix,
                                                                                    self.__grpcLogWriteHandler)

        #응답 데이터 생성
        responseMessage = BrowserHookResponse(
            response_id = request.request_id,

            allowed = bAllowed,            
            modified_query = strModifiedQuery, # modified_query = "test",
            error_message = strErrorMessage,
            reason = strReason
        )
        
        LOG().debug(f"response browser request hook, response = {responseMessage}")

        return responseMessage

    @grpc_error_handler()
    def HookLLMRequest(self, request, context) -> LLMResponse:

        '''
        '''

        #request, 로그만 관리하고, 저장은 하지 않는다.
        # LOG().debug(f"recv llm request hook, request = {request}")        

        nAgentID:int = request.agent_id
        strMessage:str = request.messages
        
        strLLMKey:str = request.llm_key
        nIteration:int = request.iteration
        bStream:bool = request.stream

        #TODO: Filter Manager
        #수정된 메시지, 로직 최소화, 공백으로 전달하면 Hook에서 기존 메시지를 전달한다. => grpc로 제어도 검토        
        # strModifiedMessage:str = ""
        # bAllowed = True
        strIndexNamePrefix:str = "llm-request"

        (bAllowed, strModifiedMessage) = self.__grpcProxyHelper.FilterManager().FilterLLMRequest(strMessage)

        #저장 -> file로 export 한다. mongodb 포맷
        # self.__grpcProxyHelper.WriteLLMRequestToDB(request)

        self.__grpcProxyHelper.GrpcLogWriteCustomHelper().AddLLMRequestData(nAgentID,
                                                                            strMessage,
                                                                            strLLMKey,
                                                                            nIteration,
                                                                            bStream,
                                                                            bAllowed,
                                                                            strModifiedMessage,
                                                                            strIndexNamePrefix,
                                                                            self.__grpcLogWriteHandler)

        #응답 데이터 생성
        responseMessage = LLMResponse(
            response_id = request.request_id,

            allowed = bAllowed,
            # modified_message = "test",
            modified_message = strModifiedMessage, #TODO: 여기를 최소화, 공백이면 기존값 쓰도록.. 우선 테스트
        )

        LOG().debug(f"response llm request hook, response = {responseMessage}")

        return responseMessage
        
    @grpc_error_handler()
    def HookMCPCall(self, request, context) -> MCPCallResponse:
        
        '''
        '''

        # LOG().debug(f"recv mcp call hook, request = {request}")

        nAgentID:int = request.agent_id

        strServerName:str = request.server_name
        strToolName:str = request.tool_name
        strArgument:str = request.arguments

        # bAllowed = True
        # strModifiedArgument:str = "" #동일로직으로 관리, 필요한 기능인지도 확인.

        (bAllowed, strModifiedArgument) = self.__grpcProxyHelper.FilterManager().FilterMCPRequest()

        #DB 저장
        strIndexNamePrefix:str = "mcp-request"
        # self.__grpcProxyHelper.WriteMCPCallRequestToDB(request)
        self.__grpcProxyHelper.GrpcLogWriteCustomHelper().AddMCPCallRequestData(nAgentID,
                                                                                strServerName,
                                                                                strToolName,
                                                                                strArgument,
                                                                                bAllowed,
                                                                                strModifiedArgument,
                                                                                strIndexNamePrefix,
                                                                                self.__grpcLogWriteHandler)

        #응답 데이터 생성
        responseMessage = MCPCallResponse(
            response_id = request.request_id,

            allowed = bAllowed,
            modified_arguments = strModifiedArgument
        )

        LOG().debug(f"response mcp call hook, response = {responseMessage}")

        return responseMessage
    
    @grpc_error_handler()
    def HookLLMStreamChunk(self, request, context) -> LLMStreamChunkResponse:

        '''        
        '''

        # LOG().debug(f"recv llm stream chunk hook, request = {request}")

        nAgentID:int = request.agent_id

        strChunk:str = request.chunk
        strAccumResponse:str = request.accumulated_response
        strMessages:str = request.messages
        strLLMKey:str = request.llm_key
        nIteration:int = request.iteration

        bAllowed:bool = True
        strModifiedChunk:str = ""
        bStopStream:bool = False

        #TODO: chunk에 대한 차단 로직.

        #DB 저장
        # self.__grpcProxyHelper.WriteLLMStreamChunkToDB(request)
        strIndexNamePrefix:str = "llm-stream-chunk"
        self.__grpcProxyHelper.GrpcLogWriteCustomHelper().AddLLMStreamChunkData(nAgentID,
                                                                                strChunk,
                                                                                strAccumResponse,
                                                                                strMessages,
                                                                                strLLMKey,
                                                                                nIteration,
                                                                                bAllowed,
                                                                                strModifiedChunk,
                                                                                bStopStream,
                                                                                strIndexNamePrefix,
                                                                                self.__grpcLogWriteHandler)

        #응답 데이터 생성
        responseMessage = LLMStreamChunkResponse(
            response_id = request.request_id, #TODO: 이름 실수, 사용하지 않는 필드라서, 우선 수정 안함.

            allowed = bAllowed,
            modified_chunk = strModifiedChunk,
            stop_stream = bStopStream
        )

        LOG().debug(f"response llm stream chunk, response = {responseMessage}")
        return responseMessage
    
    @grpc_error_handler()
    def HookLLMResponse(self, request, context) -> LLMResponseResponse:

        '''        
        '''

        # LOG().debug(f"recv llm response hook, request = {request}")

        nAgentID:int = request.agent_id

        strResponse:str = request.response
        strMessage:str = request.messages
        strLLMKey:str = request.llm_key
        nIteration:int = request.iteration
        bStream:bool = request.stream

        bAllowed:bool = True
        strModifiedResponse:str = ""

        #TODO: LLM Response에 대한 차단 로직.

        #DB 저장
        # self.__grpcProxyHelper.WriteLLMResponseToDB(request)
        strIndexNamePrefix:str = "llm-response"
        self.__grpcProxyHelper.GrpcLogWriteCustomHelper().AddLLMResponseData(nAgentID,
                                                                             strResponse,
                                                                             strMessage,
                                                                             strLLMKey,
                                                                             nIteration,
                                                                             bStream,
                                                                             bAllowed,
                                                                             strModifiedResponse,
                                                                             strIndexNamePrefix,
                                                                             self.__grpcLogWriteHandler)

        #응답 데이터 생성
        responseMessage = LLMResponseResponse(
            response_id = request.request_id,

            allowed = bAllowed,
            modified_response = strModifiedResponse
        )

        LOG().debug(f"response llm response, response = {responseMessage}")
        return responseMessage
    
    @grpc_error_handler()
    def HookMCPResponse(self, request, context) -> MCPResponseResponse:

        '''        
        '''

        # LOG().debug(f"recv mcp response hook, request = {request}")

        nAgentID:int = request.agent_id

        strServerName:str = request.server_name
        strToolName:str = request.tool_name
        strArgument:str = request.arguments
        strResponse:str = request.response

        bAllowed:bool = True
        strModifiedResponse:str = ""

        #DB 저장
        # self.__grpcProxyHelper.WriteMCPResponseToDB(request)
        strIndexNamePrefix:str = "mcp-response"
        self.__grpcProxyHelper.GrpcLogWriteCustomHelper().AddMCPResponseData(nAgentID,
                                                                             strServerName,
                                                                             strToolName,
                                                                             strArgument,
                                                                             strResponse,
                                                                             bAllowed,
                                                                             strModifiedResponse,
                                                                             strIndexNamePrefix,
                                                                             self.__grpcLogWriteHandler)

        responseMessage = MCPResponseResponse(
            response_id = request.request_id,
            
            allowed = bAllowed,
            modified_response = strModifiedResponse
        )

        LOG().debug(f"response mcp response, response = {responseMessage}")

        return responseMessage
        

