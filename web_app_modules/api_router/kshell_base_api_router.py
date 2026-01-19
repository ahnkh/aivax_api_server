
#외부 라이브러리
from lib_include import *

#local common
from web_app_modules.local_etc_common.api_router_generator import ApiRouterGenerator

#help modules
# from web_app_modules.api_action_help_modules.route_action_helper import RouteActionHelper
from web_app_modules.api_router.help_modules.kshell_execute_helper import KhsellExecuteHelper

'''
kshell 기본 router
kshell 상태, 기본 공통 라우터등 관리를 계획
TODO: 이름은 중요하지 않다. 우선 제외.
'''

class KshellBaseApiRouter:
    
    def __init__(self):
        
        self.__kshellExecuteHelper: KhsellExecuteHelper = None        
        pass
    
    #지정된 config 대로 rotuer 초기화
    def InitializeRouter(self, webMainApp:Any, dictLocalConfig: dict) -> APIRouter:
        
        '''
        TODO: WebMainApp의 순환참조 조심.
        TODO: webMainApp 에서 데이터를 관리하며, local config로 전달한다.
        local config 안에 kshell Main App도 포함되어 있다.
        '''
        
        #TODO: 순환 참조 방지
        from web_app_modules.web_api_mainapp import WebApiMainApp
        from mainapp.kshell_mainapp import KShellMainApp
         
        webMainAppRef:WebApiMainApp = webMainApp
        kshellMainApp:KShellMainApp = webMainAppRef.GetKShellApp()
        
        # kshell로 전달하면,webMainApp와의 연결 고리는 없다. 제거.
        self.__kshellExecuteHelper = KhsellExecuteHelper()
        self.__kshellExecuteHelper.Initialize(kshellMainApp)
        
        #TODO: 이름 변경
        routerGenerator = ApiRouterGenerator()
        router = routerGenerator.CreateApiRouter(dictLocalConfig)

        #route 추가, 프로그래밍 패턴화, 로깅등 편의성
        route_list = dictLocalConfig.get("route_list")

        routeImpl = self
        routerGenerator.AddRouteEndPointFromConfig(route_list, routeImpl, router)
        
        #TODO: 이게 반환되어야, openapi 에 추가된다.
        return router
    
    ################################ router endpoint 정의
    
    #임의의 데이터 전송, dictionary안에 명령어를 추가해서 tpshell 호출
    async def runKShell(self, request: Request):

        byteRawBody = await request.body()
        return self.__runKShellWebApi(byteRawBody)
    
    
    ################################################### private
    
    #실제 kshell 실행, 이것만 별도로 개발
    def __runKShellWebApi(self, byteRawBody: bytes):

        #json 변환, string, byte 모두 지원, 오류나면, 그대로 반환
        dictItemModel = {}
        JsonHelper.LoadToDictionary(byteRawBody, dictItemModel)

        #기본 모듈의 호출, dictHttpRequest => dictOpt
        
        #TODO: 이름 주의
        return self.__runKShell(dictItemModel)
    
    def __runKShell(self, dictItemModel: dict):
        self.__kshellExecuteHelper.ExecuteCommand(dictItemModel)        
        return {}
        
        
        

