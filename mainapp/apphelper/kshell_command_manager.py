
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

'''
kshell 명령의 실행 관리, 별도 모듈로 분리
'''

class KShellCommandManager:
    
    def __init__(self):
        pass
    
    # 함수 호출 => 이곳으로 이관한다.
    def RunCLICommand(self, mainApp, dictOpt:dict):
        
        #TODO: 명령이 여러개 일수 있다. 이경우에도 응답은 하나로 모은다.
        #TODO: 파라미터가 없어도 응답 처리로 제공한다. (통일성)
        apiResponseHandler = ApiResponseHandlerX()
        
        #기본 응답값, 성공으로
        apiResponseHandler.attachSuccessCode()
        
        #명령 모음 실행
        self.__runCommandList(mainApp, dictOpt, apiResponseHandler)
        
        #TODO: 응답 결과에 대한 처리. 예외처리는 안에서 수행한다.
        #TODO: 이건 공통화 필요
        #응답 결과.
        dictResponse = apiResponseHandler.outResponse()
        self.__writeOutputResponse(dictOpt, dictResponse)
        
        return dictResponse
    
    def RunMultiCommand(self, mainApp, lstMultiCommand:list):
        
        apiResponseHandler = ApiResponseHandlerX()
        
        
        for dictOpt in lstMultiCommand:
            
            enable_command:bool = dictOpt.get(KShellParameterDefine.SCRIPT_MODULE.ENABLE_COMMAND)
            
            if None != enable_command and CONFIG_OPT_DISABLE == enable_command:
                continue
            
            self.__runCommandList(mainApp, dictOpt, apiResponseHandler)
            
        dictResponse = apiResponseHandler.outResponse()
        self.__writeOutputResponse(dictOpt, dictResponse)
        
        return dictResponse
    
    ################################################### private
    
    def __runCommandList(self, mainApp, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        
        lstMethod = dictOpt.get(KShellParameterDefine.METHOD)
        
        
        if None == lstMethod or 0 == len(lstMethod):
            return ERR_OK
        
        for strMethod in lstMethod:
            
            self.__runCommandAt(mainApp, dictOpt, strMethod, apiResponseHandler)
        
        return ERR_OK
    
    def __runCommandAt(self, mainApp, dictOpt:dict, strMethod:str, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        strMethod = str(strMethod).strip()

        method = getattr(mainApp, strMethod)

        method(dictOpt, apiResponseHandler)
        
        return ERR_OK
    
    # 응답 결과의 처리 (Write 옵션)
    def __writeOutputResponse(self, dictOpt:dict, dictResponse:dict):
        
        '''
        apiResponseHandler의 내용을 출력한다.
        출력 옵션은 dictOpt에 있다.
        TODO: 두번 사용해야 하는 문제 => custom 공통화 대상.
        '''
        
        #응답 결과.
        # dictResponse = apiResponseHandler.outResponse()
        
        #응답 값이 없으면 skip
        if None == dictResponse:            
            return ERR_OK
        
        #출력 경로 지정, 이 값이 있으면 출력한다.
        api_out_reponse = dictOpt.get(KShellParameterDefine.API_OUT_RESPONSE)
        
        #TODO: 예외처리는 필요
        if None != api_out_reponse:        
            JsonHelperX.WriteMapToJsonFile(dictResponse, api_out_reponse)
        
        #화면 출력 옵션은 제공하자.
        api_print_console = dictOpt.get(KShellParameterDefine.API_PRINT_CONSOLE)
        
        #여기만은 화면에 그대로 출력
        if None != api_print_console and CONFIG_OPT_ENABLE == api_print_console:
            
            #TODO: print 합수 Wrapping, string만 지원
            GlobalCommonModule.PrintMessage(dictResponse)
        
        return ERR_OK
        
        