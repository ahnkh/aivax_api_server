
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

#전역 모듈 관리.
from mainapp.global_resource.kshell_global_resource_manager import KShellGlobalResourceManager

'''
Shell App Helper, wrapping
'''

class KShellAppHelper:
    
    def __init__(self):
        
        #shell local config
        self.__dictJsonLocalConfigRoot:dict = None
        pass
    
    def Initialize(self, globalResourceManager:KShellGlobalResourceManager):
        
        '''
        '''
                
        self.__dictJsonLocalConfigRoot = globalResourceManager.GetLocalConfigRoot()        
        return ERR_OK
    
    ################################################### helpper, wraping
    
    def ManageWinsModules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        from util_modules.wins_manage_modules.wins_manage_module import WinsManageModule

        utilModule = WinsManageModule()
        utilModule.RunModule(dictOpt, self.__dictJsonLocalConfigRoot, apiResponseHandler)
        return ERR_OK
    
    def ManageOperationUtilModules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        from util_modules.operation_util_manage_modules.operation_util_manage_module import OperationUtilManageModule

        utilModule = OperationUtilManageModule()
        utilModule.RunModule(dictOpt, self.__dictJsonLocalConfigRoot, apiResponseHandler)
        return ERR_OK
    