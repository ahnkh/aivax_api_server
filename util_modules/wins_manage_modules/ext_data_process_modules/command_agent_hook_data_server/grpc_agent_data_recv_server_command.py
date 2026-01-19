
import multiprocessing
# import threading

import grpc
from concurrent import futures

from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *


#TODO: 이 코드는 남겨 두자.
# from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.hook_pb2 import BrowserHookResponse
from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.hook_pb2_grpc import add_HookProxyServicer_to_server

#grpc 요청의 서버 처리 모듈
from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.grpc_proxy import GrpcProxy

#grpc 결과의 로그 저장 => GrpcProxy로 전달
from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.log_write_submodules.grpc_log_write_handler import GrpcLogWriteHandler


'''
디노티시아, grpc 기반 데이터 수집 및 저장 서버 제공
1차, python 기반의 데몬으로 개발한다. kshell로 별도 프로세스 기동.
TOOD: filter기반 응답 처리도 고려되어야 하며 filter는 외부 프로세스와 API 통신을 한다. (IPC등 고려)
'''


class GRPCAgentDataRecvServerCommand:

    def __init__(self):
        pass

    # 별도의 독립된 프로세스를 실행한다.
    def RunExtProcess(self, dictOpt:dict, dictWinsDataProcessModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        API에서 호출.
        '''

        LOG().info("run grpc process")

        port:int = int(dictOpt.get(KShellParameterDefine.PORT, 50000))

        apiResponseHandler.attachApiCommandCode("grpc agent server command")

        multiprocessing.set_start_method("spawn")
        p = multiprocessing.Process(target=self.RunDaemon, args=(dictOpt, dictWinsDataProcessModuleLocalConfig, apiResponseHandler), daemon=False)
        p.start()

        apiResponseHandler.attachSuccessCode(f"run process, port = {port}")

        # #호출후, 스레드 무한 대기
        # stopEvent = threading.Event()

        # try:
        #     # print("무한 대기중... (Ctrl+C로 종료)")
        #     stopEvent.wait()  # timeout 없이 무한 대기
        # except KeyboardInterrupt:
        #     # print("사용자에 의해 종료 요청(KeyboardInterrupt)")
        #     GlobalCommonModule.RaiseException("keyboard interrupt exception")
        #     return ERR_FAIL

        return ERR_OK

    # grpc 수신 서버의 실행 (thread, 비동기 실행 주의)
    def RunDaemon(self, dictOpt:dict, dictWinsDataProcessModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        grpc 서버를 실행한다. 데몬형태로 실행, proxy 호출
        
        mariadb에 저장하는 기능이 필요하다. => helper를 활용, SQL은 동기, json은 스레드 구조. API만 비동기
        응답의 전달 시점에 filter, 판정 기능이 제공되어야 한다. (최종 sLLM을 고려중이면 프로세스간 API 통신)        
        '''

        LOG().info("run grpc agent data recv server daemon")

        grpc_recv_server_command = dictWinsDataProcessModuleLocalConfig.get("grpc_recv_server_command")

        #TODO: bulk 등 다른 스레드도 필요, 스레드 처리 기능 추가
        #grpc 데몬의 생성전에 먼저 실행한다.
        #생성 이후의 호출측과의 통신은 고려하지 않는다.
        gprcLogWriteHandler = GrpcLogWriteHandler()
        gprcLogWriteHandler.Initialize(dictOpt, grpc_recv_server_command)

        #RPC 시작지점, 생성된 서비스를 정의한다.
        #TODO: 스레드, 세션관련 데이터 동기화 이슈가 있다. 여기서 gRPC의 통신 모듈과, Application 로직이 분리되어야 할 필요가 있다.
        grpcProxy = GrpcProxy()
        grpcProxy.Initialize(gprcLogWriteHandler, grpc_recv_server_command)

        self.__runGRPCServer(dictOpt, grpcProxy, grpc_recv_server_command, apiResponseHandler)

        return ERR_OK

    ############################################# private

    #grpc 서버의 실행
    def __runGRPCServer(self, dictOpt:dict, grpcProxy:GrpcProxy, dictGrpcRecvServerCommandLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        #TODO: 기본값 지정, 입력값 예외처리 모듈 추가 (향후 추가)
        port:int = int(dictOpt.get(KShellParameterDefine.PORT, 50000))

        # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[ExceptionInterceptor()])
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

        add_HookProxyServicer_to_server(grpcProxy, server)
        
        strServerUrl = f"[::]:{port}"
        server.add_insecure_port(strServerUrl)
        server.start()

        LOG().info(f"Server started on port {strServerUrl}")
        
        server.wait_for_termination() 

        return ERR_OK


#주석, 다른 concurrent.future에서 interceptor 추가.
#concurrent.future 예외처리 클래스
# class ExceptionInterceptor(grpc.ServerInterceptor):

#     def intercept_service(self, continuation, handler_call_details):

#         def exception_wrapper(request, context):
#             try:
#                 return continuation(handler_call_details)(request, context)
#             except Exception as e:
#                 # import traceback
#                 # traceback.print_exc()
#                 LOG().error(traceback.format_exc())

#                 context.abort(grpc.StatusCode.INTERNAL, f"Server error: {e}")

#         return exception_wrapper

# class ExceptionInterceptor(grpc.ServerInterceptor):
#     def intercept_service(self, continuation, handler_call_details):
#         handler = continuation(handler_call_details)

#         if handler is None:
#             return None

#         # UnaryUnary RPC (일반적인 case)
#         if handler.unary_unary:
#             def new_unary_unary(request, context):
#                 try:
#                     return handler.unary_unary(request, context)
#                 except Exception as e:
#                     traceback.print_exc()
#                     context.abort(grpc.StatusCode.INTERNAL, f"Unhandled Server Error: {e}")
#             return grpc.unary_unary_rpc_method_handler(
#                 new_unary_unary,
#                 request_deserializer=handler.request_deserializer,
#                 response_serializer=handler.response_serializer,
#             )

#         # UnaryStream RPC
#         if handler.unary_stream:
#             def new_unary_stream(request, context):
#                 try:
#                     yield from handler.unary_stream(request, context)
#                 except Exception as e:
#                     traceback.print_exc()
#                     context.abort(grpc.StatusCode.INTERNAL, f"Unhandled Server Error: {e}")
#             return grpc.unary_stream_rpc_method_handler(
#                 new_unary_stream,
#                 request_deserializer=handler.request_deserializer,
#                 response_serializer=handler.response_serializer,
#             )

#         # StreamUnary RPC
#         if handler.stream_unary:
#             def new_stream_unary(request_iterator, context):
#                 try:
#                     return handler.stream_unary(request_iterator, context)
#                 except Exception as e:
#                     traceback.print_exc()
#                     context.abort(grpc.StatusCode.INTERNAL, f"Unhandled Server Error: {e}")
#             return grpc.stream_unary_rpc_method_handler(
#                 new_stream_unary,
#                 request_deserializer=handler.request_deserializer,
#                 response_serializer=handler.response_serializer,
#             )

#         # StreamStream RPC
#         if handler.stream_stream:
#             def new_stream_stream(request_iterator, context):
#                 try:
#                     yield from handler.stream_stream(request_iterator, context)
#                 except Exception as e:
#                     traceback.print_exc()
#                     context.abort(grpc.StatusCode.INTERNAL, f"Unhandled Server Error: {e}")
#             return grpc.stream_stream_rpc_method_handler(
#                 new_stream_stream,
#                 request_deserializer=handler.request_deserializer,
#                 response_serializer=handler.response_serializer,
#             )

#         return handler    