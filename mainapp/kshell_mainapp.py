
import os

#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

#main app 관리 helper
from mainapp.apphelper.kshell_app_helper import KShellAppHelper

#전역 데이터 관리
from mainapp.global_resource.kshell_global_resource_manager import KShellGlobalResourceManager

#명령 실행 helper
from mainapp.apphelper.kshell_command_manager import KShellCommandManager

'''
kshell main app
'''

class KShellMainApp:
    
    def __init__(self):
        
        #TODO: json 설정 config 필요, 전역 관리
        #TODO: OpenAPI 와 연동도 기본으로 깔고 간다.
        
        #Helper 클래스, 무상태 패턴 (shell에서 접근)
        self.__appHelper = None
        
        #전역 데이터 관리 모듈 추가
        self.__globalResourceManager = None
        
        #명령의 호출 모듈
        self.__commandManager = None
        pass
    
    #local 설정 config Root 반환
    def GetLocalConfigRoot(self):        
        return self.__globalResourceManager.GetLocalConfigRoot()
    
    #초기화, 지연된 초기화
    def Initialize(self, dictOpt:dict):
        
        '''
        초기 디렉토리, 설정, 전역변수의 초기화를 설정한다.
        TODO: 함수가 길어지면, 기능별로 분리해야 한다.
        TODO: 초기화 시점의 오류는, 예외로 한정하지 않는다. exception 처리.
        '''
                
        #전역 초기 모듈, TODO: 초기 설정은 GlobalInitManager에서 관리한다.
        #전역값 관리, 여러개 일경우에 대한 대비, GlobalInitManager 에서 관리, 반환하는 방향의 검토.
        self.__globalResourceManager = KShellGlobalResourceManager()
        self.__globalResourceManager.InitializeResource(dictOpt) 

        #TODO: Initialize의 예외처리는 exception 으로 관리한다.
        # nErrInitializeResource = self.__GlobalResourceManager.InitializeResource(dictOpt)
        
        # if ERR_FAIL == nErrInitializeResource:
        #     LOG().error("fail intialize resource")
        #     return ERR_FAIL
        
        #App Helper, 초기화, MainApp 는 최대한 가볍게 관리한다.
        #TODO: GlobalResource의 복사 - 강결함은 있으나, 소스의 간편성쪽이 나을듯 하다.

        self.__appHelper = KShellAppHelper()       
        self.__appHelper.Initialize(self.__globalResourceManager)
        
        #명령의 실행 관리, 최대한 무상태 패턴
        #TODO: MainApp 가 API 형식으로 실행되면, 여러 번 호출될수 있다.
        self.__commandManager = KShellCommandManager()
        
        return ERR_OK
    
    # 함수 호출 => 이곳으로 이관한다.
    def RunCLICommand(self, dictOpt:dict):
        
        '''
        호출구조 
        dictOpt에서 method를 꺼내서, 호출한다.
        요청및 응답, 사실상 메인의 처리를 여기서 수행한다.
        '''

        LOG().debug(f"run cli command, opt = {dictOpt}")
        
        #TODO: Helper로 이관하자.
        return self.__commandManager.RunCLICommand(self, dictOpt)
        
    
    #모듈의 종료 처리
    def DisposeApplication(self, strDisposeMethodName:str):

        '''
        '''

        if None == self.__globalResourceManager:
            LOG().error("kshell main is not initialize, cancel dispose application")
            return ERR_FAIL

        self.__globalResourceManager.DisposeGlobalResource(strDisposeMethodName)

        return ERR_OK
    
    ################################################# 외부 실행 메소드 (reflection)
    
    #최초 메소드, test, TODO: 알파벳 순서 철저히
    #TODO: 미구현 명령, 미구현 명령은 제일 상단에. TODO: Api 출력 파라미터, 처음부터 강제하자.
    def test(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        self.__appHelper.TestKshellMainApp(dictOpt, apiResponseHandler)        
        pass
    
    # LT 관리 명령
    def manage_lt_modules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        self.__appHelper.ManageLTModules(dictOpt, apiResponseHandler)        
        pass
    
    # stock 관리 명령
    def manage_stock_modules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        self.__appHelper.ManageStockModules(dictOpt, apiResponseHandler)        
        pass

    # wins cli
    def manage_wins_modules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        self.__appHelper.ManageWinsModules(dictOpt, apiResponseHandler)
        pass

    # util cli modules
    def manage_operation_util_modules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):

        self.__appHelper.ManageOperationUtilModules(dictOpt, apiResponseHandler)

        pass

