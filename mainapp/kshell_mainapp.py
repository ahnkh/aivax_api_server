
import os

from lib_include import *

from common_modules.type_hint import *

from common_modules.global_resource.kshell_global_resource_manager import KShellGlobalResourceManager

from mainapp.apphelper.kshell_app_helper import KShellAppHelper

from mainapp.apphelper.kshell_command_manager import KShellCommandManager


class KShellMainApp:
    
    def __init__(self):
        
        self.__appHelper = None
        
        self.__globalResourceManager = None
        
        self.__commandManager = None
        
        self.__bInitialize:bool = False
        
        pass
    
    def GetLocalConfigRoot(self) ->dict:        
        return self.__globalResourceManager.GetLocalConfigRoot()
    
    def IsInitialize(self) -> bool:        
        return self.__bInitialize
            
    def Initialize(self, dictOpt:dict):
                
        self.__globalResourceManager = KShellGlobalResourceManager()
        self.__globalResourceManager.InitializeResource(dictOpt) 

        self.__appHelper = KShellAppHelper()       
        self.__appHelper.Initialize(self.__globalResourceManager)
        
        self.__commandManager = KShellCommandManager()
        
        self.__bInitialize = True
        return ERR_OK
        
    def RunCLICommand(self, dictOpt:dict):
                
        return self.__commandManager.RunCLICommand(self, dictOpt)
        
    def RunMultiCommand(self, lstMultiCommand:list, dictOpt:dict):
        
        return self.__commandManager.RunMultiCommand(self, lstMultiCommand, dictOpt)
                
    def DisposeApplication(self, strDisposeMethodName:str):

        if None == self.__globalResourceManager:
            return ERR_FAIL

        self.__globalResourceManager.DisposeGlobalResource(strDisposeMethodName)

        return ERR_OK

    def manage_wins_modules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):        
        self.__appHelper.ManageWinsModules(dictOpt, apiResponseHandler)

    def manage_operation_util_modules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        self.__appHelper.ManageOperationUtilModules(dictOpt, apiResponseHandler)
