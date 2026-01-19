
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

from mainapp.kshell_mainapp import KShellMainApp

'''
각 router의 kshell 호출 공통화
모든 router 호출은 kshell로 공통화 한다.
kshell 실행 파타미터에서 입력값에 대한 생성 무결성 처리를 담당한다.
'''

class KhsellExecuteHelper:
    
    def __init__(self):
        
        self.__kshellMainApp: KShellMainApp = None
        pass
    
    def Initialize(self, kshellMainApp: KShellMainApp):
        
        #한개만 생성, 미리 복사.
        self.__kshellMainApp = kshellMainApp
        return ERR_OK
    
    #kshell 모듈의 호출, 창구 단일화
    # def DoModule(self, strModuleName:str, args:Any = None) -> dict:
    def ExecuteCommand(self, dictOpt:dict = None) -> dict:
        
        '''
        '''
        
        try:

            #TODO: 구조 개선, RunCLICommand 안에서 다 처리한다. , api 중복도, 이 안에서 처리하도록 개선            
            return self.__kshellMainApp.RunCLICommand(dictOpt)
            
            #TODO: 다만, 향후를 위해서 모듈 분리는 유지한다. (kshell execute helper에 기능 위임)

        except HTTPException as err:

            LOG().error(traceback.format_exc()) 

            dictOutput:dict = err.detail

            # err.status_code 

            return dictOutput

        except Exception as err:
            
            # LOG().error(str(err))        
            LOG().error(traceback.format_exc())  

            #예외처리 로직 통일
            #TODO: 에러 코드는 향후 정의

            # GlobalCommonModule.RaiseHttpException(ApiResponseDefine.API_CODE_FAIL_ERROR, str(err), apiResponseHandler)
            # return ERR_FAIL
            
            apiResponseHandler = ApiResponseHandlerX()
            apiResponseHandler.attachFailCode(ErrorDefine.API_UNKNOWN_ERROR, ErrorDefine.API_UNKNOWN_ERROR_MSG, str(err))

            return apiResponseHandler.outResponse()

            
        
        
    ########################################################### private
        
    
    