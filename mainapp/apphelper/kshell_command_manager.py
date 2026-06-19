
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
        
        '''
        TODO: 순환 참조 문제, mainApp는 Any로 전달한다.
        호출구조 
        dictOpt에서 method를 꺼내서, 호출한다.
        요청및 응답, 사실상 메인의 처리를 여기서 수행한다.
        TODO: API 호출시와 CLI 호출시는 분기한다. -> ApiResponseHandler등 문제
        대신 API 호출시, 명시적으로 RunAPICommand를 호출하도록 수정한다.
        TODO: API 호출시점에 공통화 + 리펙토링을 생각한다.
        호출시, method 호출 구조가 다르다. method를 여러번 호출할수 있다. 개발 확장 시점에 고려
        확장을 위해서, 함수 안으로 은닉시킨다.
        '''
        
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
    
    def RunMultiCommand(self, mainApp, lstMultiCommand:list, dictOpt:dict):
        
        '''
        lstMultiCommand 에서 독립적인 dictOpt를 제공
        dictOpt별로 실행한다. 실행 결과 값은 apiResponseHandler로 관리
        반환값, 옵션이 있으면 parameter로 반환. 각 API별로 응답 파라미터의 관리가 필요하다.
        '''
        
        apiResponseHandler = ApiResponseHandlerX()
        
        #TODO: multicommand에서의 응답값은 개별로 처리, 여기는 개선 필요
        #실행결과 별로 연관성을 최소화 해야 한다.
        
        for dictCommand in lstMultiCommand:
            
            #TODO: custom옵션, use_command, 비활성화 옵션만 추가.            
            enable_command:bool = dictOpt.get(KShellParameterDefine.SCRIPT_MODULE.ENABLE_COMMAND)
            
            if None != enable_command and CONFIG_OPT_DISABLE == enable_command:
                continue
            
            #TODO: 옵션, 복사되어야 한다.
            for key in dictOpt.keys():
                
                value:Any = dictOpt.get(key)
                
                #없는건만 추가, command가 우선
                if key in dictCommand:
                    continue
                
                dictCommand[key] = value #TODO: 수정이 안된다는 전제하에서의 복사
            
            self.__runCommandList(mainApp, dictCommand, apiResponseHandler)
            
            #TODO: 개별 호출이 되어야 한다.
            dictResponse = apiResponseHandler.outResponse()
            self.__writeOutputResponse(dictOpt, dictResponse)
            
        # dictResponse = apiResponseHandler.outResponse()
        # self.__writeOutputResponse(dictOpt, dictResponse)
        
        return dictResponse
    
    ################################################### private
    
    #Kshell 명령 모음, 묶음 실행
    def __runCommandList(self, mainApp, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        TODO: 개발이 잘못된 부분 존재, dictOpt 위에 list가 제공되어야 했다..
        '''
        
        #파라미터로 받은 메소드 목록, 여기는 그냥 유지하자.
        lstMethod = dictOpt.get(KShellParameterDefine.METHOD)
        
        #없으면 skip => TODO: 이 경우에도, Api 응답 처리는 필요
        
        if None == lstMethod or 0 == len(lstMethod):
            #log 불필요, 그냥 넘어가자.
            # LOG().error("invalid method list, no data")
            return ERR_OK
        
        #명령별 실행 => 함수화, TODO: list가 없으면, 안에서 예외처리 한다.
        for strMethod in lstMethod:
            
            # #함수 이름 앞뒤 공백 제거
            # strMethod = str(strMethod).strip()

            # #메소드 호출, TODO: 가장 메인 선언부라, 예외처리는 하지 않는다.
            # method = getattr(mainApp, strMethod)

            # #TODO: 인자가 필요할수도 있다. 이 경우에 대해서는 향후 고려
            # #응답 결과는 불필요. 예외가 발생하면, exception에서 걸림.            
            # method(dictOpt, apiResponseHandler)
            
            #TODO: 응답, 적층식 구조 - 일단 Api 코드로, 개별 메시지 결과로 대체 => 다시 고민.
            self.__runCommandAt(mainApp, dictOpt, strMethod, apiResponseHandler)
            #pass
        
        return ERR_OK
    
    # 각 명령의 실행
    def __runCommandAt(self, mainApp, dictOpt:dict, strMethod:str, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        #함수 이름 앞뒤 공백 제거
        strMethod = str(strMethod).strip()

        #메소드 호출, TODO: 가장 메인 선언부라, 예외처리는 하지 않는다.
        method = getattr(mainApp, strMethod)

        #TODO: 인자가 필요할수도 있다. 이 경우에 대해서는 향후 고려
        #응답 결과는 불필요. 예외가 발생하면, exception에서 걸림.            
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
        api_print_console = int(dictOpt.get(KShellParameterDefine.API_PRINT_CONSOLE, CONFIG_OPT_DISABLE))
        
        #여기만은 화면에 그대로 출력
        if None != api_print_console and CONFIG_OPT_ENABLE == api_print_console:
            
            #TODO: print 합수 Wrapping, string만 지원
            # GlobalCommonModule.PrintMessage(dictResponse)
            print(json.dumps(dictResponse, indent=4, ensure_ascii=False))
        
        return ERR_OK
        
        