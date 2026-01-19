
#외부 라이브러리
from lib_include import *

from web_app_modules.web_lib_include import *

from web_app_modules.local_etc_common.api_router_generator import ApiRouterGenerator

from web_app_modules.api_router.help_modules.kshell_execute_helper import KhsellExecuteHelper

'''
util api router
'''

class OperationUtilApiRouter:

    def __init__(self):

        self.__kshellExecuteHelper: KhsellExecuteHelper = None        
        pass

    def InitializeRouter(self, webMainApp:Any, dictLocalConfig:dict) -> APIRouter:

        '''
        '''

        from web_app_modules.web_api_mainapp import WebApiMainApp

        webMainAppRef:WebApiMainApp = webMainApp
        kshellMainApp = webMainAppRef.GetKShellApp()

        self.__kshellExecuteHelper = KhsellExecuteHelper()
        self.__kshellExecuteHelper.Initialize(kshellMainApp)
        
        routerGenerator = ApiRouterGenerator()
        router = routerGenerator.CreateApiRouter(dictLocalConfig)
        
        route_list = dictLocalConfig.get("route_list")
        routerGenerator.AddRouteEndPointFromConfig(route_list, self, router)

        return router
    
    #sqlmap, 범용 sql 요청 api
    async def executeSQLApi(self, request: Request):

        byteRawBody = await request.body()
        dictItemModel = OperationUtilModelConvertHelper.executeSQLApi(byteRawBody)
        return self.__runKshell(dictItemModel)
    
    ##################################################### private

    def __runKshell(self, dictItemModel:dict):

        return self.__kshellExecuteHelper.ExecuteCommand(dictItemModel)
