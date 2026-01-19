
import threading
import time
# from collections import deque

from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.log_write_submodules.byte_buffer_fast_writer import ByteBufferFastWriter

'''
grpc등 수집된 로그를 저장하는 스레드를 개발한다.
로그는 문자열로 정규화 하며, 문자열에 대해서 정해진 제한값, 주기에 따라 파일로 저장한다.
파일로의 저장은 기존의 string bulkwriter를 활용한다.
로그의 저장 포맷은 호출 측에서 관리한다.
'''

class GrpcLogWriteHandler:

    #각 로그 메시지의 타입 정의
    TYPE_BROWSER_MESSAGE = "bwmsg"
    TYPE_LLM_REQUEST = "llmreq"
    TYPE_MCP_CALL = "mcpcall"

    TYPE_LLM_STREAM_CHUNK = "strchk"
    TYPE_LLM_RESPONSE = "llmres"
    TYPE_MCP_RESPONSE = "mcpres"

    LAST_FLUSH_TIME = "last_flush_time"

    MAX_WAIT_TIME_OUT = 5
    THREAD_TIME_OUT = 1

    def __init__(self):

        self.__lock = threading.Lock()
        # self.__condition = threading.Condition(self.__lock)

        #string buffer write queue
        self.__dictBufferWriteQueue = {}

        # self.__thread = None
        pass

    ################################################## public

    # 로그 데이터 추가
    # def AddData(self, strDataType:str, strDataLog:str):byteLogData:bytes
    def AddData(self, strDataType:str, byteLogData:bytes):

        '''
        StringBuffer에 추가한다. 이후 저장 조건, Flush 처리는
        StringBuffer에서 담당한다.        
        '''
        
        byteBufferFastWriter:ByteBufferFastWriter = self.__dictBufferWriteQueue.get(strDataType)

        # stringBufferWriter:StringBufferBulkWriterHelper = self.__dictBufferWriteQueue.get(strDataType)

        if None == byteBufferFastWriter:
            LOG().error(f"invalid data type {strDataType}")
            return ERR_FAIL
        
        byteBufferFastWriter.WriteLog(byteLogData)

        return ERR_OK

    def Initialize(self, dictOpt:dict, dictGrpcRecvServerCommandLocalConfig:dict):

        '''
        '''

        #TODO: 초기화 시점, 예외 발생사 Raize 처리.

        #strinbfuffer, 미리 추가.
        #stringbuffer writer, 이름을 지어서, 미리 추가, Initialize

        log_write_thread:dict = dictGrpcRecvServerCommandLocalConfig.get("log_write_thread")
        self.__initializeBufferWriter(self.__dictBufferWriteQueue, log_write_thread)

        # self.__thread = threading.Thread(target=self.ThreadHandlerProc, daemon=True)
        # self.__thread.start()

        thread = threading.Thread(target=self.ThreadHandlerProc, daemon=True)
        thread.start()

        return ERR_OK

    # 스레드 생성.
    def ThreadHandlerProc(self, ):

        '''
        데몬이 종료될때까지는 계속 수행된다. 
        TODO: 스레드가 종료되었으면, 재기동등 예외처리 로직을 추가한다.
        '''
        
        nMaxWaitTimeout:int = GrpcLogWriteHandler.MAX_WAIT_TIME_OUT
        # nThreadSleep:int = 1

        while True:

            time.sleep(GrpcLogWriteHandler.THREAD_TIME_OUT) #시작후 대기한다. (바로 저장이 되지는 않을 것으로 예상)

            #각 Buffer별로 다르게 계산한다.
            self.__lock.acquire()
            
            for strDataType in self.__dictBufferWriteQueue.keys():

                # stringBufferBulkWriter:StringBufferBulkWriterHelper = self.__dictBufferWriteQueue.get(strKey)
                byteBufferFastWriter:ByteBufferFastWriter = self.__dictBufferWriteQueue.get(strDataType)

                #TODO: size 체크는 불필요. 

                if None != byteBufferFastWriter:

                    #각 buffer별 flush 체크.                    
                    self.__flushBufferWriterAt(byteBufferFastWriter, nMaxWaitTimeout)
                    
            self.__lock.release()

        # return ERR_OK


    ################################################## protected


    ################################################## private

    #buffer writer의 초기화
    def __initializeBufferWriter(self, dictBufferWriteQueue:dict, dictLogWriteThreadLocalConfig:dict):

        '''
        '''

        string_buffer_config_list:list = dictLogWriteThreadLocalConfig.get("string_buffer_config_list")

        for dictBulkConfig in string_buffer_config_list:

            strQueueId:str = dictBulkConfig.get("queue_id")
            
            LOG().debug(f"initialize buffer writer, queue id {strQueueId}")

            # stringBufferBulkWriter = StringBufferBulkWriterHelper()
            # stringBufferBulkWriter.Initialize(dictBulkConfig)

            # #마지막 수집시간 설정.
            # stringBufferBulkWriter.UpdateEtcValue(GrpcLogWriteHandler.LAST_FLUSH_TIME, time.time())

            # dictBufferWriteQueue[strQueueId] = stringBufferBulkWriter

            # self.__dictBufferWriteQueue= {
            #     GrpcLogWriteHandler.TYPE_BROWSER_MESSAGE : browserMessageWriter,
            #     GrpcLogWriteHandler.TYPE_LLM_REQUEST : llmRequestWriter,
            #     GrpcLogWriteHandler.TYPE_MCP_CALL : mcpCallWriter,

            #     GrpcLogWriteHandler.TYPE_LLM_STREAM_CHUNK : llmStreamChunkWriter,
            #     GrpcLogWriteHandler.TYPE_LLM_RESPONSE : llmResponseWriter,
            #     GrpcLogWriteHandler.TYPE_MCP_RESPONSE : mcpResponseWriter,
            # }
            
            byteBufferFastWriter:ByteBufferFastWriter = ByteBufferFastWriter()
            byteBufferFastWriter.Initialize(dictBulkConfig)
            
            #TODO: 사양 재검토
            # #마지막 수집시간 설정.
            byteBufferFastWriter.UpdateLastFlushTime(time.time())
            
            dictBufferWriteQueue[strQueueId] = byteBufferFastWriter

        return ERR_OK
    

    #각 log별 flush 요청
    # def __flushBufferWriterAt(self, stringBufferBulkWriter:StringBufferBulkWriterHelper, nMaxWaitTimeout:int):

    #     '''
    #     '''

    #     now:float = time.time()

    #     fLastFlushTime:float = stringBufferBulkWriter.GetEtcValue(GrpcLogWriteHandler.LAST_FLUSH_TIME)

    #     if (now - fLastFlushTime) >= nMaxWaitTimeout:

    #         stringBufferBulkWriter.FlushBuffer()
    #         stringBufferBulkWriter.UpdateEtcValue(GrpcLogWriteHandler.LAST_FLUSH_TIME, now)

    #     return ERR_OK
    
    # def __flushBufferWriterAt(self, byteBufferFastWriter:ByteBufferFastWriter, nMaxWaitTimeout:int, strDataType:str):
    def __flushBufferWriterAt(self, byteBufferFastWriter:ByteBufferFastWriter, nMaxWaitTimeout:int):

        '''
        '''

        now:float = time.time()

        fLastFlushTime:float = byteBufferFastWriter.GetLastFlushTIme()

        if (now - fLastFlushTime) >= nMaxWaitTimeout:
            
            # LOG().debug(f"flush buffer writer, last flush time {fLastFlushTime}, now {now}, diff {now - fLastFlushTime}, type = {strDataType}")

            byteBufferFastWriter.FlushBuffer()
            byteBufferFastWriter.UpdateLastFlushTime(now)

        return ERR_OK

