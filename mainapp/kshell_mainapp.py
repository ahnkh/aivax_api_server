
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
        
        self.__appHelper = None
        
        self.__globalResourceManager = None
        
        self.__commandManager = None
        
        self.__bInitialize:bool = False
        
        pass
    
    #local 설정 config Root 반환
    def GetLocalConfigRoot(self) ->dict:        
        return self.__globalResourceManager.GetLocalConfigRoot()
    
    def IsInitialize(self) -> bool:        
        return self.__bInitialize
    
    
    #초기화, 지연된 초기화
    def Initialize(self, dictOpt:dict):
                
        self.__globalResourceManager = KShellGlobalResourceManager()
        self.__globalResourceManager.InitializeResource(dictOpt) 

        self.__appHelper = KShellAppHelper()       
        self.__appHelper.Initialize(self.__globalResourceManager)
        
        self.__commandManager = KShellCommandManager()
        
        self.__bInitialize = True
        return ERR_OK
        
    def RunCLICommand(self, dictOpt:dict):

        LOG().debug(f"run cli command, opt = {dictOpt}")
                
        return self.__commandManager.RunCLICommand(self, dictOpt)
        
    def RunMultiCommand(self, lstMultiCommand:list, dictOpt:dict):
        
        LOG().debug(f"run multi command")
        
        return self.__commandManager.RunMultiCommand(self, lstMultiCommand, dictOpt)
                
    def DisposeApplication(self, strDisposeMethodName:str):

        if None == self.__globalResourceManager:
            LOG().error("kshell main is not initialize, cancel dispose application")
            return ERR_FAIL

        self.__globalResourceManager.DisposeGlobalResource(strDisposeMethodName)

        return ERR_OK

    def manage_wins_modules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):        
        self.__appHelper.ManageWinsModules(dictOpt, apiResponseHandler)
        pass

    def manage_operation_util_modules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        self.__appHelper.ManageOperationUtilModules(dictOpt, apiResponseHandler)

        pass
