
import grpc

from lib_include import *

from common_modules.type_hint import *

import util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.hook_pb2 as hook_pb2
import util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_modules.hook_pb2_grpc as hook_pb2_grpc


'''
grpc 처리 공통모듈, 테스트 모듈
'''

#grpc exception 처리 decorator
def grpc_error_handler(timeout:int = 5, error_retry:int = 3):

    def decorator(func):

        def wrapper(self, strRPCUrl:str, strGrpcMethodName:str, grpcRequest:Any, *args, **kwargs):

            # last_exception = None

            # 처음부터 exception 추가
            for nTry in range(error_retry):

                try:
                    # return func(self, strRPCUrl, strGrpcMethodName, grpcRequest, *args, timeout=timeout, **kwargs)
                    return func(self, strRPCUrl, strGrpcMethodName, grpcRequest, *args, timeout=timeout, **kwargs)
                
                except grpc.RpcError as e:
                    # last_exception = e
                    LOG().error(traceback.format_exc())

            #여기까지 발생했으면, 재시도 오류로 신규 raise
            raise Exception('unknown grpc handller exception')
        
        return wrapper
    
    return decorator

class GrpcClient:

    def __init__(self):
        self.__channel = None
        pass

    #서버 접속
    def __Connect(self, strRPCUrl:str):

        '''
        TODO: 이것까지 넣어야 한다. 예외처리는 같이, 우선 연결세션은 미고려
        '''

        self.__channel = grpc.insecure_channel(strRPCUrl)
        # self.__stub = hook_pb2_grpc.HookProxyStub(self.__channel)
        stub = hook_pb2_grpc.HookProxyStub(self.__channel)

        #같은 의미이나, stub 반환 => 연결, 비연결 모두 고려
        return stub
    
    #서버 종료
    def __Close(self, ):

        self.__channel.close()


    #예외적으로, 모호한 의미로 call 사용, TODO: 상수관리, 여기서는 안한다.
    @grpc_error_handler(timeout = 5, error_retry = 3)
    def call(self, strRPCUrl:str, strGrpcMethodName:str, request:Any, *args, **kwargs) -> Any:

        '''
        '''

        stub = self.__Connect(strRPCUrl)

        #stub에서 이름을 꺼내서 request로 받고, response로 던진다.
        method = getattr(stub, strGrpcMethodName)

        #TODO: 예외처리는 decorator로 사용
        response:Any = method(request, **kwargs)

        #우선 비연결 세션
        self.__Close()

        return response