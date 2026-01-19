
#외부 라이브러리
from lib_include import *

from web_app_modules.web_lib_include import *

from web_app_modules.local_etc_common.api_router_generator import ApiRouterGenerator

from web_app_modules.api_router.help_modules.kshell_execute_helper import KhsellExecuteHelper

'''
wins api router
'''

class WinsApiRouter:

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
    
    #디노티시아, grpc 서버 수집 데몬 기동
    async def runGrpcServer(self, modelItem:GrpcServerItem):

        dictItemModel = WinsModelConvertHelper.runGrpcServer(modelItem)
        return self.__runKshell(dictItemModel)
    
    #디노티시아, 메시지 요청 client
    async def runGrpcClient(self, modelItem:GrpcClientItem):

        dictItemModel = WinsModelConvertHelper.runGrpcClient(modelItem)
        return self.__runKshell(dictItemModel)
    
    #사용자 로그인 요청
    async def authLogin(self, modelItem:LoginModelItem):

        dictItemModel = WinsModelConvertHelper.authLogin(modelItem)
        return self.__runKshell(dictItemModel)
    
    #사용자 계정 정보 추가,수정,삭제,조회
    async def getUserAccount(self, modelItem: UserAccountListItem):

        dictItemModel = WinsModelConvertHelper.getUserAccount(modelItem)
        return self.__runKshell(dictItemModel)
    
    #사용자 계정 추가 
    async def insertUserAccount(self, modelItem:UserAccountInsertItem):

        dictItemModel = WinsModelConvertHelper.insertUserAccount(modelItem)
        return self.__runKshell(dictItemModel)
    
    #사용자 계정 수정 
    async def editUserAccount(self, modelItem:UserAccountEditItem):

        dictItemModel = WinsModelConvertHelper.editUserAccount(modelItem)
        return self.__runKshell(dictItemModel)
    
    #사용자 계정 삭제
    async def deleteUserAccount(self, modelItem:UserAccountDeleteItem):

        dictItemModel = WinsModelConvertHelper.deleteUserAccount(modelItem)
        return self.__runKshell(dictItemModel)
    
    #사용자 그룹 - 추가,수정,삭제,조회
    async def getUserGroup(self, modelItem:UserGroupListItem):

        dictItemModel = WinsModelConvertHelper.getUserGroup(modelItem)
        return self.__runKshell(dictItemModel)
    
    async def insertUserGroup(self, modelItem:UserGroupInsertItem):

        dictItemModel = WinsModelConvertHelper.insertUserGroup(modelItem)
        return self.__runKshell(dictItemModel)
    
    async def editUserGroup(self, modelItem:UserGroupEditItem):

        dictItemModel = WinsModelConvertHelper.editUserGroup(modelItem)
        return self.__runKshell(dictItemModel)
    
    async def deleteUserGroup(self, modelItem:UserGroupDeleteItem):

        dictItemModel = WinsModelConvertHelper.deleteUserGroup(modelItem)
        return self.__runKshell(dictItemModel)
    
    #Filter view - 추가,수정,삭제,조회
    async def getFilterView(self, modelItem:UserAccountDeleteItem):

        dictItemModel = WinsModelConvertHelper.getFilterView(modelItem)
        return self.__runKshell(dictItemModel)
    
    async def insertFilterView(self, modelItem:UserAccountDeleteItem):

        dictItemModel = WinsModelConvertHelper.insertFilterView(modelItem)
        return self.__runKshell(dictItemModel)
    
    async def editFilterView(self, modelItem:UserAccountDeleteItem):

        dictItemModel = WinsModelConvertHelper.editFilterView(modelItem)
        return self.__runKshell(dictItemModel)
    
    async def deleteFilterView(self, modelItem:UserAccountDeleteItem):

        dictItemModel = WinsModelConvertHelper.deleteFilterView(modelItem)
        return self.__runKshell(dictItemModel)
    
    #차단정보 조회 - 프롬프트 차단, MCP server, 사용자 현황
    async def getPromptBlockInfo(self, modelItem:PromptBlockLogItem):

        dictItemModel = WinsModelConvertHelper.getPromptBlockInfo(modelItem)
        return self.__runKshell(dictItemModel)
    
    async def getMCPServerBlockInfo(self, modelItem:MCPServerBlockLogItem):

        dictItemModel = WinsModelConvertHelper.getMCPServerBlockInfo(modelItem)
        return self.__runKshell(dictItemModel)
    
    async def getUserMonitorStatus(self, modelItem:UserMonitorLogItem):

        dictItemModel = WinsModelConvertHelper.getUserMonitorStatus(modelItem)
        return self.__runKshell(dictItemModel)

    ##################################################### private

    def __runKshell(self, dictItemModel:dict):

        return self.__kshellExecuteHelper.ExecuteCommand(dictItemModel)

    

