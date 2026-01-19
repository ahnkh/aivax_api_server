
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

#TODO: 한번만 사용한다는 가정하에 webMainApp import 추가
from web_app_modules.web_api_mainapp import WebApiMainApp

class ApiRouterUpdateModule:

    def __init__(self):
        pass

    #ApiRouter, reflection으로 리스트를 만들어서, 전달하는 방안의 검토
    def AddApiRouter(self, tmsWebMainApp: WebApiMainApp, dictJsonLocalConfigRoot:dict, apiKeyDependMethod: Any = None):

        '''
        설정 config, router를 동적으로 만든다.
        전역객체로, mainApp를 전달해서 공유한다.
        
        TODO: app 두개를 전달해야 하는 문제, 구조상으로 webmainapp를 전달하고, shellMainApp를 반환해야 하는데.. => 여기 다시 검토.
        TODO: apiKeyDependMethod 는 함수 포인터이다, 최초 구현시에는 사용안하나, 향후 사용할 가능성. => 우선 사용하지 않는다.
        '''

        LOG().info("add api router")

        #TODO: 구조 변경, 외부 파일로 처리.
        self.__includeRouterFromConfig(tmsWebMainApp, dictJsonLocalConfigRoot)
        
        '''
        api_router_list : list = jsonLocalConfigRoot.get("api_router_list")

        #설정 config에서 클래스명을 가져온다.
        for dictReflectConfig in api_router_list:
            
            module_path = dictReflectConfig.get("module_path")
            class_name = dictReflectConfig.get("class_name")

            use = dictReflectConfig.get("use")

            if CONFIG_OPT_DISABLE == use:
                LOG().debug(f"skip api router, module = {module_path}")
                continue
            
            # routeModule = ModuleImportUtil.CreateInstance(module_path, class_name)
            routeModule = GlobalCommonModule.CreateNewInstance(module_path, class_name)

            method_name = dictReflectConfig.get("method_name")

            #메소드로 전달할 옵션, None일수도 있다. => None은 안되는 것으로 규정. 예외처리 최소화
            #TODO: 이 이름이 헷갈렸다. dictOpt -> local_config로 변경
            local_config = dictReflectConfig.get("local_config")

            #TODO: dictionary, 한개로 통일, 에약어 추가
            #약간의 메모리 부담이 있지만, 편의성 차원에서 전달

            #TODO: 단발성, 상태를 유지하면 안되는 구조여야 한다.
            #기본적으로 가지는 상태는 불변값이다.
            local_config[WebApiDefine.ROUTER_OPT_WEB_MAIN_APP] = tmsWebMainApp
            local_config[WebApiDefine.ROUTER_OPT_SHELL_MAIN_APP] = kshellMainApp
            
            #TODO: 이건 사용하지 않는 방향 => depends 옵션은 우선 제외한다.
            # dictOpt[WebApiDefine.ROUTER_OPT_API_KEY_MANAGE_METHOD] = apiKeyDependMethod

            #TODO: 이건 customize 해야 한다.
            apiRouter = self.__runMethod(routeModule, method_name, local_config)

            #router 추가
            LOG().info(f"add router module = {module_path}, method = {method_name}")
            # tmsWebMainApp.include_router(apiRouter, dependencies=[Depends(apiKeyDependMethod)])
            kshellMainApp.include_router(apiRouter)


        #외부 router, DB를 읽어서 추가하는 로직 추가
        #4.1.3.11 로직 변경, 외부에서 DB 읽을지 여부 제어
        # self.__addApiRouterFromDB(tmsWebMainApp, tmsShellMainApp, apiKeyDependMethod)
        '''

        return ERR_OK
    
    ########################################################### private
    
    #local config의 지정된 설정 파일에서 router를 include 하도록 구현
    def __includeRouterFromConfig(self, tmsWebMainApp: WebApiMainApp, dictJsonLocalConfigRoot:dict):
        
        '''
        '''
        
        #TODO: 상수 처리
        fast_api_server_config : dict = dictJsonLocalConfigRoot.get("fast_api_server_config")
        
        #router config 의 설정 파일을 읽어서 router 추가.
        router_config:dict = fast_api_server_config.get("router_config")
        
        router_config_list:list = router_config.get("router_config_list")
        
        for dictRouterConfig in router_config_list:
            
            #사용 옵션
            use = dictRouterConfig.get("use")
            
            #router 파일 path, 여기서부터 별도 파일
            path = dictRouterConfig.get("path")
            
            if CONFIG_OPT_DISABLE == use:                
                LOG().info(f"skip api router config, path = {path}")
                continue

            #각 파일별 router 추가, TODO: 추가적인 파라미터 필요                
            self.__includeEachRouterConfigAt(path, tmsWebMainApp)
        
        return ERR_OK
    
    #개별 rotuer config 파일의 include
    def __includeEachRouterConfigAt(self, strRouterConfigFilePath:str, webMainApp: WebApiMainApp):
        
        '''
        TODO: 더 추가해야 할 파라미터 존재, 우선 만들고 나서, depth가 3 depth 정도.
        
        TODO: router 클래스 정보로 router 클래스 를 생성하고
        route_list config 정보로 endpoint를 생성한다. endpoint 에 대해서는 각 router 안으로 위임한다.
        router 파일별로 config를 관리하는 방향 - 여기가 router를 만드는 포인트 이다.
        '''
        
        #file to json
        dictRouterConfig = {}        
        nErrLoadRouterConfig = JsonHelper.JsonFileToDictionary(strRouterConfigFilePath, dictRouterConfig)
        
        if ERR_FAIL == nErrLoadRouterConfig:
            #TODO: exception 처리 => 최초 설정 오류
            GlobalCommonModule.RaiseHttpException(ErrorDefine.API_ROUTER_INIT_ERROR, ErrorDefine.API_ROUTER_INIT_ERROR_MSG, f"invalid router config, path = {strRouterConfigFilePath}")
            return ERR_FAIL
        
        #kshell 에서는, 하나의 파일은 하나의 module만 처리하도록 구현한다.
        #여러개의 router를 생성하는 문제는 다시 확인 => singleton 처리가 불필요? 소스 개발후 진행
        
        module_path = dictRouterConfig.get("module_path")
        class_name = dictRouterConfig.get("class_name")

        use = dictRouterConfig.get("use")

        if CONFIG_OPT_DISABLE == use:
            LOG().info(f"skip api router, module = {module_path}")
            return ERR_OK
        
        # routeModule = ModuleImportUtil.CreateInstance(module_path, class_name)
        # TODO: singleton 검토 : 모듈에 대한 router를 나눌수 있다.
        routeModule = GlobalCommonModule.CreateNewInstance(module_path, class_name)

        method_name = dictRouterConfig.get("method_name")

        #메소드로 전달할 옵션, None일수도 있다. => None은 안되는 것으로 규정. 예외처리 최소화
        #TODO: 이 이름이 헷갈렸다. dictOpt -> local_config로 변경
        local_config = dictRouterConfig.get("local_config")

        #TODO: dictionary, 한개로 통일, 에약어 추가
        #약간의 메모리 부담이 있지만, 편의성 차원에서 전달

        #TODO: 단발성, 상태를 유지하면 안되는 구조여야 한다.
        #기본적으로 가지는 상태는 불변값이다. TODO: routeImpr로 전달만 하면 된다. 메소드에 담아서 전달
        # local_config[WebApiDefine.ROUTER_OPT_WEB_MAIN_APP] = tmsWebMainApp
        
        #TODO: webMainApp 에서 kshell을 가져올수 있는 방안으로 검토하자. => 우선 소스를 전반적으로 보고 결정
        # local_config[WebApiDefine.ROUTER_OPT_SHELL_MAIN_APP] = kshellMainApp
        
        #TODO: 이건 사용하지 않는 방향 => depends 옵션은 우선 제외한다.
        # dictOpt[WebApiDefine.ROUTER_OPT_API_KEY_MANAGE_METHOD] = apiKeyDependMethod

        #TODO: 이건 customize 해야 한다. 
        #TODO: 더 헷갈린다. 함수 제외
        # apiRouter = self.__runMethod(routeModule, method_name, local_config)
        
        # 초기화 함수 호출, reflection 으로 처리 => 다만 거의 InitializeRouter 함수 이다.
        strMethod = str(method_name).strip() #공백 제거, 기본 예외처리
        method = getattr(routeModule, strMethod)        
        apiRouter = method(webMainApp, local_config)

        #router 추가
        LOG().info(f"add router module = {module_path}, method = {method_name}")
        # tmsWebMainApp.include_router(apiRouter, dependencies=[Depends(apiKeyDependMethod)])
        webMainApp.include_router(apiRouter)
        
        return ERR_OK
    
    # #동적 메소드 실행 - 메소드 실행인자가 달라서 각각 실행 필요.
    # def __runMethod(self, instanceClass: Any, strMethod: str, dictLocalConfig: dict = None) -> Any:

    #     #함수 이름 앞뒤 공백 제거
    #     strMethod = str(strMethod).strip()

    #     method = getattr(instanceClass, strMethod)

    #     #TODO: 인자가 필요할수도 있다. 이 경우에 대해서는 향후 고려
    #     #응답 결과는 불필요. 예외가 발생하면, exception에서 걸림.
    #     return method(dictLocalConfig)
    