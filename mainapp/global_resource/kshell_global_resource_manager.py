
from lib_include import *

from common_modules.type_hint import *

#local config 관리
from mainapp.global_resource.help_modules.local_json_config_helper import LocalJsonConfigHelper

from mainapp.global_resource.help_modules.local_resource_init_helper import LocalResourceInitHelper

'''
'''

class KShellGlobalResourceManager:
    
    def __init__(self):
        
        self.__dictJsonLocalConfigRoot = {}
        
        pass
    
    def InitializeResource(self, dictOpt:dict):
        
        self.__initializeLocalConfigRoot(dictOpt)
        
        dictJsonLocalConfigRoot = self.__dictJsonLocalConfigRoot
        
        self.__initializeFactoryInstance(dictJsonLocalConfigRoot)
        
        self.__initializeGlobalLocalResource(dictJsonLocalConfigRoot)

        self.__initializeDBModule(dictOpt, dictJsonLocalConfigRoot)
        
        self.__initializeHttpRequest(dictOpt, dictJsonLocalConfigRoot)
                
        return ERR_OK
    
    def DisposeGlobalResource(self, strDisposeMethodName:str):

        '''
        '''

        instanceFactory:GlobalInstanceFactory = GlobalInstanceFactory.singletonInstance()
        instanceFactory.DisposeInstance(strDisposeMethodName)

        return ERR_OK
    
    ######################################################### resource getter/setter
    
    def GetLocalConfigRoot(self) -> dict:
        return self.__dictJsonLocalConfigRoot
    
    ######################################################### private
    
    def __initializeLocalConfigRoot(self, dictOpt:dict) -> int:
        
        '''
        '''
        
        LOG().debug("initialize local config root")
        
        strConfigBasePath:str = dictOpt.get(KShellParameterDefine.CONFIG_BASE_PATH)
        
        localJsonConfigHelper = LocalJsonConfigHelper()
        localJsonConfigHelper.InitializeLocalConfig(strConfigBasePath, self.__dictJsonLocalConfigRoot)
        
        return ERR_OK
    
    def __initializeGlobalLocalResource(self, dictJsonLocalConfigRoot:dict):
        
        '''
        '''
        
        localResourceHelper = LocalResourceInitHelper()
        localResourceHelper.InitializeResource(dictJsonLocalConfigRoot)
        
        return ERR_OK
    
    def __initializeFactoryInstance(self, dictJsonLocalConfigRoot:dict):
        
        '''
        '''
        
        LOG().debug("initialize factory instance")
        
        GlobalInstanceFactory.createFactoryInstance(dictJsonLocalConfigRoot)
        
        return ERR_OK

    def __initializeDBModule(self, dictOpt:dict, dictJsonLocalConfigRoot:dict) -> int:

        '''
        '''
        
        sqlClientInterface:SQLClientInterface = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_SQL_CLIENT_INTERFACE)
        
        sqlClientInterface.Initialize(dictOpt, dictJsonLocalConfigRoot)
        
        self.__customIntializeOpensearchService(dictJsonLocalConfigRoot)

        return ERR_OK
    
    def __initializeHttpRequest(self, dictOpt:dict, dictJsonLocalConfigRoot:dict):
        
        '''
        '''
        
        LOG().debug("initialize http request")
        
        http_query_map:dict = dictJsonLocalConfigRoot.get("http_query_map")
        
        http_query_map_list:list = http_query_map.get("http_query_map_list")
        
        httpRequest:HttpRequestInterface = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_HTTP_REQUEST_INTERFACE)
        
        httpRequest.Initialize(http_query_map_list)
        
        return ERR_OK
    
    def __customIntializeOpensearchService(self, dictJsonLocalConfigRoot:dict):
        
        from service_modules.db_service.opensearch_api_service import OpensearchApiService
        
        opensearchAPIService:OpensearchApiService = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_OPENSEARCH_API_SERVICE)
        
        db_connector:dict = dictJsonLocalConfigRoot.get("db_connector")
        
        opensearch_connector:str = db_connector.get("opensearch_connector")
        
        dictOpenSearchConnector:dict = {}
        JsonHelperX.JsonFileToDictionary(opensearch_connector, dictOpenSearchConnector)
        
        host:str = dictOpenSearchConnector.get("host")
        port:int = dictOpenSearchConnector.get("port")
        id:str = dictOpenSearchConnector.get("id")
        passwd:str = dictOpenSearchConnector.get("passwd")
                         
        opensearchAPIService.Initliaze(host, port, id, passwd)
        
        return ERR_OK