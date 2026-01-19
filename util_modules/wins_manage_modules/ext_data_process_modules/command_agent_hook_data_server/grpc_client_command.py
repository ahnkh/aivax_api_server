import grpc

from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

import util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.hook_pb2 as hook_pb2
import util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.hook_pb2_grpc as hook_pb2_grpc

from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.grpc_client import GrpcClient

# from hook_pb2_grpc import HookProxyStub

'''
grpc client 테스트 모듈
단순 요청, 외부에서 실행 제어
'''

class GrpcClientCommand:

    def __init__(self):

        self.__grpcClient = GrpcClient()
        pass

    def RequestToGrpcServer(self, dictOpt:dict, dictWinsDataProcessModule:dict, apiResponseHandler:ApiResponseHandlerX):
        '''
        실행 옵션 getattr로 접근
        parameter는 1차 임의로, 필요한 데이터만 빼내거나, script config로 호출
        접근 서버 IP, Port 정보 입력 (향후 요청 테스트 부하용도로도 필요)
        '''

        # strServerHost = dictOpt.get(KShellParameterDefine.HOST)
        # nPort = int(dictOpt.get(KShellParameterDefine.PORT))

        #grpc 요청 command        
        request = dictOpt.get(KShellParameterDefine.REQUEST)

        apiResponseHandler.attachApiCommandCode("grpc agent client command")

        methodFunction = getattr(self, request)
        response = methodFunction(dictOpt, apiResponseHandler)

        apiResponseHandler.attachSuccessCode(f"request to grpc server, request = {request}, response = {response}")

        return ERR_OK

    ######################################################## private

    #실제 구현된 grpc 메시지, 우선 계속 추가한다.
    #TOOD: grpc 서버는 현재는 특화 기능이고, 향후 공용 grpc interface를 설계한다.
    def on_browser_message(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX) -> Any:

        '''
        TODO: 중복된 코드가 있어도 우선 무시한다.
        '''

        strServerHost = dictOpt.get(KShellParameterDefine.HOST, "127.0.0.1")
        nPort = int(dictOpt.get(KShellParameterDefine.PORT, 50000))

        strRpcUrl = f"{strServerHost}:{nPort}"

        strQuery = dictOpt.get(KShellParameterDefine.QUERY, "")

        #Request 객체, stub에서 호출시 선언을 분리하여 구현
        request = hook_pb2.BrowserHookRequest(
            request_id = "0",
            agent_id = 0,
            query = strQuery,
            session_id = "session_id",
            user_role = "user_role"         
        )

        response = self.__grpcClient.call(strRpcUrl, "HookBrowserMessage", request)

        LOG().info(f"request on browser message, host = {strServerHost}:{nPort}, query = {strQuery}, response = {response}")

        return response

        # #grpc 채널 생성
        # with grpc.insecure_channel(f"{strServerHost}:{nPort}") as channel:
            
        #     stub = hook_pb2_grpc.HookProxyStub(channel)

        #     #Request 객체, stub에서 호출시 선언을 분리하여 구현
        #     request = hook_pb2.BrowserHookRequest(
        #         request_id = "0",
        #         agent_id = 0,
        #         query = strQuery,
        #         session_id = "",
        #         user_role = ""
        #     )

        #     #서비스 요청 (Request 요청, Response 수신)
        #     response = stub.HookBrowserMessage(request)

            # #테스트, 결과 출력
            # LOG().info(f"request on browser message, host = {strServerHost}:{nPort}, query = {strQuery}, response = {response}")
        pass

    def on_llm_request(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX) -> Any:

        '''
        '''

        strServerHost = dictOpt.get(KShellParameterDefine.HOST, "127.0.0.1")
        nPort = int(dictOpt.get(KShellParameterDefine.PORT, 50000))

        strQuery = dictOpt.get(KShellParameterDefine.QUERY, "")

        # #grpc 채널 생성
        # with grpc.insecure_channel(f"{strServerHost}:{nPort}") as channel:
            
        #     stub = hook_pb2_grpc.HookProxyStub(channel)

        #     #Request 객체, stub에서 호출시 선언을 분리하여 구현
        #     request = hook_pb2.LLMRequest(
        #         request_id = "0",
        #         agent_id = 0,
        #         messages = strQuery,
        #         llm_key = "llm_key",
        #         iteration = 0,
        #         stream = True
        #     )

        #     #서비스 요청 (Request 요청, Response 수신)
        #     response = stub.HookLLMRequest(request)

        #     #테스트, 결과 출력
        #     LOG().info(f"request on llm request, host = {strServerHost}:{nPort}, query = {strQuery}, response = {response}")

        request = hook_pb2.LLMRequest(
            request_id = "0",
            agent_id = 0,
            messages = strQuery,
            llm_key = "llm_key",
            iteration = 0,
            stream = True
        )

        strRpcUrl = f"{strServerHost}:{nPort}"
        response = self.__grpcClient.call(strRpcUrl, "HookLLMRequest", request)
        LOG().info(f"request on llm request, host = {strServerHost}:{nPort}, message = {strQuery}, response = {response}")

        return response

    def on_mcp_call(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX) -> Any:

        '''
        '''

        # LOG().info(f"request on mcp call, host = {strServerHost}:{nPort}, query = {strQuery}, allowed = {response.allowed}")
        LOG().info(f"request on mcp call")

        strServerHost = dictOpt.get(KShellParameterDefine.HOST, "127.0.0.1")
        nPort = int(dictOpt.get(KShellParameterDefine.PORT, 50000))
        # strQuery = dictOpt.get(KShellParameterDefine.QUERY, "")


        strRpcUrl = f"{strServerHost}:{nPort}"
        #Request 객체, stub에서 호출시 선언을 분리하여 구현
        request = hook_pb2.MCPCallRequest(
            request_id = "0",
            agent_id = 0,
            server_name = "server_name",                
            tool_name = "tool_name",
            arguments = "arguments"
        )

        response = self.__grpcClient.call(strRpcUrl, "HookMCPCall", request)
        LOG().info(f"request on llm request, host = {strServerHost}:{nPort}, response = {response}")

        return response

    def on_llm_sream_chunk(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX) -> Any:

        '''
        '''

        strServerHost = dictOpt.get(KShellParameterDefine.HOST, "127.0.0.1")
        nPort = int(dictOpt.get(KShellParameterDefine.PORT, 50000))
        # strQuery = dictOpt.get(KShellParameterDefine.QUERY, "")


        strRpcUrl = f"{strServerHost}:{nPort}"
        #Request 객체, stub에서 호출시 선언을 분리하여 구현
        request = hook_pb2.LLMStreamChunkRequest(
            request_id = "0",
            agent_id = 0,
            chunk = "chunk",                
            accumulated_response = "accumulated_response",
            message = "message",
            llm_key = "llm_key",
            iteration = 100,
        )

        response = self.__grpcClient.call(strRpcUrl, "HookLLMStreamChunk", request)
        LOG().info(f"request on llm stream chunk, host = {strServerHost}:{nPort}, response = {response}")

        return response

    def on_llm_response(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX) -> Any:

        '''
        '''

        strServerHost = dictOpt.get(KShellParameterDefine.HOST, "127.0.0.1")
        nPort = int(dictOpt.get(KShellParameterDefine.PORT, 50000))
        strQuery = dictOpt.get(KShellParameterDefine.QUERY, "")


        strRpcUrl = f"{strServerHost}:{nPort}"
        #Request 객체, stub에서 호출시 선언을 분리하여 구현
        request = hook_pb2.LLMResponseRequest(
            request_id = "0",
            agent_id = 0,
            response = "response",                
            message = strQuery,
            llm_key = "llm_key",
            iteration = 1,
            stream = True,
        )

        response = self.__grpcClient.call(strRpcUrl, "HookLLMResponse", request)
        LOG().info(f"request on llm response, host = {strServerHost}:{nPort}, response = {response}")

        return response

    def on_mcp_response(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX) -> Any:

        '''
        '''

        strServerHost = dictOpt.get(KShellParameterDefine.HOST, "127.0.0.1")
        nPort = int(dictOpt.get(KShellParameterDefine.PORT, 50000))
        strQuery = dictOpt.get(KShellParameterDefine.QUERY, "")


        strRpcUrl = f"{strServerHost}:{nPort}"
        #Request 객체, stub에서 호출시 선언을 분리하여 구현
        request = hook_pb2.MCPResponseRequest(
            request_id = "0",
            agent_id = 0,
            server_name = "server_name",                
            tool_name = "tool_name",
            arguments = "arguments",
            response = "response"
        )

        response = self.__grpcClient.call(strRpcUrl, "HookMCPResponse", request)
        LOG().info(f"request on llm response, host = {strServerHost}:{nPort}, response = {response}")

        return response