
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
    
    # LT 명령 관리
    def ManageLTModules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        
        LOG().debug("manage lt modules")
        
        from util_modules.lt_manage_modules.lt_manage_module import LTManageModule
        
        dbHelperFactory:DBHelperFactory = GlobalCommonModule.GetDBHelperFactory()
        
        utilModule = LTManageModule()
        utilModule.RunModule(dictOpt, self.__dictJsonLocalConfigRoot, apiResponseHandler, dbHelperFactory)        
        return ERR_OK
    
    # Stock 명령 관리
    def ManageStockModules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''        
        TODO: 최초 명령, db처리, api에 대한 대응, 어떻게 할지.
        전역 리소스 전달 부분 vs 영향도/종속성 최소화 필수.
        '''
        
        LOG().debug("manage stock modules")
        
        from util_modules.stock_manage_modules.stock_manage_module import StockManageModule
                
        dbHelperFactory:DBHelperFactory = GlobalCommonModule.GetDBHelperFactory()
                
        utilModule = StockManageModule()
        utilModule.RunModule(dictOpt, self.__dictJsonLocalConfigRoot, apiResponseHandler, dbHelperFactory)        
        return ERR_OK
    
    #wins 명령 관리
    def ManageWinsModules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        from util_modules.wins_manage_modules.wins_manage_module import WinsManageModule

        utilModule = WinsManageModule()
        utilModule.RunModule(dictOpt, self.__dictJsonLocalConfigRoot, apiResponseHandler)
        return ERR_OK
    
    # operation util 명령 관리
    def ManageOperationUtilModules(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        from util_modules.operation_util_manage_modules.operation_util_manage_module import OperationUtilManageModule

        utilModule = OperationUtilManageModule()
        utilModule.RunModule(dictOpt, self.__dictJsonLocalConfigRoot, apiResponseHandler)
        return ERR_OK
    
    #최초 테스트, MainApp 모듈, 설정값 점검
    def TestKshellMainApp(self, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        초기화 로직에 대한 점검, 디버깅으로 가능하나, 초기값이 많을때는 한개 함수로 호출
        TODO: 여기까지는 고려하지 않았다. 더 고민후 결정 인터페이스만 개발
        
        어떤 명령 모듈을 사용할지 고민후 개발.      
        '''
        
        LOG().debug("test kshell")
        
        return ERR_OK