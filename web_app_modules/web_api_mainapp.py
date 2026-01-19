
from lib_include import *

from web_app_modules.web_lib_include import *

from mainapp.kshell_mainapp import KShellMainApp

#local common modules
from web_app_modules.local_etc_common.web_app_runner import WebAppRunner

#help modules
from web_app_modules.local_etc_common.api_router_generator import ApiRouterGenerator

'''
web api main 서버
web api 와 util의 분리 구현 => kshell을 내장하고, route 기능만 담당한다.
'''

class WebApiMainApp(FastAPI):
    
    def __init__(self, **extra: Any):

        super().__init__(**extra)

        self.__kshellMainApp: KShellMainApp = None

        #TODO: 향후 사용        
        # self.__keyHeaderManageModule:ApiKeyHeaderManageModule = None
        pass
    
    #kshell main 반환
    def GetKShellApp(self):
        
        '''
        파라미터 전달보다, 내장 app 반환쪽으로 가닥
        최초 1개만 생성된다. 동일한 동작으로 보아도 무방하다.
        '''        
        return self.__kshellMainApp
    
    #Web App Main 초기화
    def Initialize(self, dictOpt:dict, shellMainApp:KShellMainApp):
        
        '''        
        '''
        
        self.__kshellMainApp = shellMainApp
        
        return ERR_OK
    
    #Api Router 추가, config 추가만 지원하도록 사양화
    def AddApiRouter(self):
        '''
        '''
        
        #TODO: 이게 적절한 기능인지..
        webMainApp = self
        dictJsonLocalConfigRoot = self.__kshellMainApp.GetLocalConfigRoot()
        # kshellMainApp = self.__kshellMainApp #TODO: webMainApp 에 kshellMainApp가 내장되어 있다. 인자로 던질지, 반환할지 검토.
        # apiRouterUpdateModule.AddApiRouter(webMainApp, kshellMainApp, self.VerifyApiKeyHeader)
        
        apiRouterGenerator = ApiRouterGenerator()
        apiRouterGenerator.IncludeApiRouter(webMainApp, dictJsonLocalConfigRoot)
        return ERR_OK
    
    #dependency, key 인증 추가, TODO: 우선 사용하지 않는 방향
    # def VerifyApiKeyHeader(self, request : Request, x_api_access_key: Optional[str] = Header(None), x_api_signature: Optional[str] = Header(None)):
        
    #     '''
    #     TODO: 틀만 추가, Api 인증은 무시한다.
    #     '''

    #     # LOG().debug("verify api key header")

    #     #TODO: exception 검토
    #     # self.__keyHeaderManageModule.VerifyApiKeyHeader(x_api_access_key, x_api_signature, request)

    #     return ERR_OK


    #WebApi 서버, Initialize이름을 Run으로 변경 TODO: 한번 호출되면, 계속 상태가 지속되는 구조
    #외부에서 실행
    def RunWebApiServer(self, dictOpt : dict):

        '''
        tms web 서버, local 설정, 크로스 체크
        api 미사용이면, 바로 죽는다. 
        연동 포트, https 설정, 기타 정보를 통해서 초기화 한다.
        이후 실제 fast api 서버는 별도 분리

        TODO: fast api로 데이터를 전달하는 절차에 대해서 확인 필요.
        TODO: 별도의 관리 프로세스가 필요한지 추가 검토
        웹서버를 기동하는 스레드, 관리하는 스레드가 별도로 필요할수도 있음.
        '''

        LOG().debug("initialize web api main")

        dictLocalConfigRoot = self.__kshellMainApp.GetLocalConfigRoot()
        
        dictWebServerConfig = {}
        
        from web_app_modules.local_etc_common.config_option_parser import ConfigOptionParser
        
        #설정 config 관리, 웹서버 구조상 거의 이때만 사용 => 이건 그대로 사용, 변경될 일이 거의 없다.
        configOptionParser = ConfigOptionParser()                    
        configOptionParser.GatherWebConfigOption(dictWebServerConfig, dictOpt, dictLocalConfigRoot)

        #웹서버 설정값, dictOpt, db, localconfig에서 추출해서 반환한다.

        #API Web 서버 실행
        #TODO: 다중실행, 스레드 등을 고민해야 하는 형태도 향후 검토
        webAppRunner = WebAppRunner()
        apiServer = self
        webAppRunner.RunWebApiServer(apiServer, dictWebServerConfig)

        return ERR_OK