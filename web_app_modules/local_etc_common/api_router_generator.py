
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

'''
ApiRouter, 생성 모듈, router와 같이 움직인다.
'''

class ApiRouterGenerator:

    def __init__(self):
        pass
    
    #router, 공통 설정 부분. => 그냥 유지하자.
    def CreateApiRouter(self, dictLocalConfig: dict) -> APIRouter:

        '''
        API Router, 공통화
        '''

        prefix = dictLocalConfig.get("prefix")

        if None == prefix:
            prefix = ""

        router = APIRouter(prefix=prefix)
        return router
    
    #ApiRouter, reflection으로 리스트를 만들어서, 전달하는 방안의 검토
    def IncludeApiRouter(self, tmsWebMainApp: Any, dictJsonLocalConfigRoot:dict, apiKeyDependMethod: Any = None):

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

    #route 정보, config에서 추가    
    def AddRouteEndPointFromConfig(self, lstRouteLocalConfig: list, routeImpl: Any, router:APIRouter, apiKeyCheckMethod: Any = None):

        '''
        설정 config에서 route를 읽어서, 추가한다.
        약간의 custom 로직이 존재한다. GlobalCommonModule과 연계한다.
        {
            "path" : "/security_policy/distribute_sbl",
            "endpoint" : "distributeToSBL",
            "methods" : ["POST"],
            "include_in_schema" : 1,
            "tags" : ["one 보안정책"],
            "summary" : "ONE 영구차단 배포"
        }
        '''

        LOG().debug("add route info from config")

        #router, 없을수 있다.
        if None == lstRouteLocalConfig:
            LOG().info("skip add router from local config")
            return ERR_OK

        for dictRouteInfo in lstRouteLocalConfig:

            '''            
            {
				"use":1, 
				"path" : "/wshell",
				"endpoint" : "runKshell",
				"methods" : ["POST"],
				"include_in_schema" : 1,
				"tags" : ["kshell web cli"],
				"summary" : "kshell 명령 콘솔 web cli",
				"description" : "",
				"description_alt_text" : ""
			}
            '''

            use = dictRouteInfo.get("use")
            path = dictRouteInfo.get("path")
            endpoint = dictRouteInfo.get("endpoint")
            methods = dictRouteInfo.get("methods")
            
            include_in_schema = dictRouteInfo.get("include_in_schema")
            tags = dictRouteInfo.get("tags")
            summary = dictRouteInfo.get("summary")

            #설정 config, 미사용 옵션 추가, 향후 개발시 사용.
            if CONFIG_OPT_DISABLE == use:
                LOG().debug(f"skip add api route, path = {path}, endpoint = {endpoint}")
                continue

            #true/false 변환
            bIncludeInSchema = False
            if CONFIG_OPT_ENABLE == include_in_schema:
                bIncludeInSchema = True

            #TODO: description

            description = dictRouteInfo.get("description")
            description_alt_text = dictRouteInfo.get("description_alt_text")

            strDescription = ""

            #description 이 없으면 alt_text 출력
            if None == description or 0 == len(description):
                strDescription = description_alt_text

            else:
                #TODO: 파일을 읽어서 출력 => 경로에 대한 임의로직 말고, 그대로 추가하자.
                # strDescriptionFullPath = f"{os.getcwd()}/{WebApiDefine.PATH_API_DESCRIPTION_ROOT}{router.prefix}/{description}"
                strDescription = FileIOHelper.OpenFileAsUTFToStream(description)

            #test
#             description = '''
#             <h2>기본 정보</h2>
# - API Header
#     <table border=2>
#         <tr>
#         <th align=center>Header</th>
#         <th align=center>Description</th>
#         </tr>
#         <tr>
#         <td> x-ngfw-openapi-timestamp</td>
#         <td> Unix Time Stamp <br/>
#         서버와의 시간차가 5분 이상 나는 경우 인증 실패 </td>
#         </tr>
#         <tr>
#         <td> x-ngfw-openapi-access-key</td>
#         <td> NGFW에서 발급한 Access key ID</td>
#         </tr>
#         <tr>
#         <td> x-ngfw-openapi-signature</td>
#         <td> StringToSign을 Access Key ID와 맵핑되는 Secret Key로 암호화한 서명 <br/>
#         HMAC 암호화 알고리즘은 HmacSHA256 사용</td>
#         </tr>
#     </table>
# - Signature 생성
#   - StringToSign: HTTP Method + " " + uri + "\n" + timestamp + "\n" + access_key
#   - SecretKey로 HmacSHA256 알고리즘으로 암호화한 후 Base64로 인코딩
# - 호출 예시

#   ```
#     curl -k -X 'POST'
#       'https://172.17.3.22:8443/api/policy/v1/blacklist-policy'
#       -H 'x-ngfw-openapi-timestamp: 1624519022'
#       -H 'x-ngfw-openapi-access-key: 74cd9c4cc37d6e55815bbc5ce5631501'
#       -H 'x-ngfw-openapi-signature: ZkupsgZjzjjrb6BGI1phgZWwvimDLFCsId16yQp21eM='
#       -H 'Content-Type: application/json'
#       -d '[
#         {
#           "ip": "10.10.10.10",
#           "type": "black",
#           "description": ""
#         }
#       ]'
#   ```
#             '''

            #실제 router에 추가, 우선 dependencies 는 제외
            router.add_api_route(path = path, endpoint = getattr(routeImpl, endpoint)
                                 , methods=methods
                                 , include_in_schema=bIncludeInSchema
                                 , tags=tags, summary=summary
                                 , description = strDescription
                                #  , dependencies=[Depends(apiKeyCheckMethod)]
                                 )

            LOG().debug(f"add api route, path = {path}, endpoint = {endpoint}")

        return ERR_OK
    
    ############################################ TODO: 이 기능은 별도로 분리했어야 했다.
    
    #local config의 지정된 설정 파일에서 router를 include 하도록 구현
    def __includeRouterFromConfig(self, tmsWebMainApp: Any, dictJsonLocalConfigRoot:dict):
        
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
    def __includeEachRouterConfigAt(self, strRouterConfigFilePath:str, webMainApp: Any):
        
        '''
        TODO: 더 추가해야 할 파라미터 존재, 우선 만들고 나서, depth가 3 depth 정도.
        
        TODO: router 클래스 정보로 router 클래스 를 생성하고
        route_list config 정보로 endpoint를 생성한다. endpoint 에 대해서는 각 router 안으로 위임한다.
        router 파일별로 config를 관리하는 방향 - 여기가 router를 만드는 포인트 이다.
        '''
        
        #개발 편의성, 재정의
        from web_app_modules.web_api_mainapp import WebApiMainApp
        webMainAppRef:WebApiMainApp = webMainApp
        
        #file to json
        dictRouterConfig = {}        
        nErrLoadRouterConfig = JsonHelper.JsonFileToDictionary(strRouterConfigFilePath, dictRouterConfig)
        
        if ERR_FAIL == nErrLoadRouterConfig:
            #TODO: exception 처리 => 최초 설정 오류
            GlobalCommonModule.RaiseException(ErrorDefine.API_ROUTER_INIT_ERROR, ErrorDefine.API_ROUTER_INIT_ERROR_MSG, f"invalid router config, path = {strRouterConfigFilePath}")
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
        
        apiRouter = method(webMainAppRef, local_config)

        #router 추가
        LOG().info(f"add router module = {module_path}, method = {method_name}")
        # tmsWebMainApp.include_router(apiRouter, dependencies=[Depends(apiKeyDependMethod)])
        webMainAppRef.include_router(apiRouter)
        
        return ERR_OK
    
    
    ############################################ 향후, 별도 모듈로, 공통모듈, 입력 처리는 가능한 kshell로 이동하여 공통화 한다.
    
    # #일부 router 공용 모듈, list 형식을 tpshell 명령 형식으로 변환
    # @staticmethod
    # def ConvertToShellArray(lstIP: list) -> str:

    #     # ip_list = modelItem.ip_list #ip목록, , 로 변환        
    #     strIPList = ','.join(lstIP)

    #     return strIPList
    
    # #정수형 리스트, 조건문 없이 함수를 아예 분류
    # @staticmethod
    # def ConvertIntListToShellArray(lstIP: list) -> str:

    #     # ip_list = modelItem.ip_list #ip목록, , 로 변환        
    #     strIPList = ','.join(map(str, lstIP))

    #     return strIPList
    
    # #단순 문자열 검사, 값의 포함 여부
    # @staticmethod
    # def VerfiySimpleStringInclude(strApiParameter: str, lstOptionRange: list):

    #     '''
    #     parameter, 값에 포함되지 않으면 Exception 발생
    #     '''

    #     if strApiParameter not in lstOptionRange:
    #         ApiResponseHandler.RaiseHttpException(HTTP_RESPONSE_STATUS_INTERNAL_ERROR, f"invalid parameter {strApiParameter}, use {lstOptionRange}")

    #     return ERR_OK
    
    # #숫자 검사, 시작~종료 범위 포함 여부
    # @staticmethod
    # def VerifySimpleCheckMinMax(nApiParameter: int, nMin: int, nMax: int):

    #     '''
    #     parameter, 최소값 미만, 최대값 초과시 Exception 발생
    #     '''

    #     if nMin > nApiParameter  or nMax < nApiParameter:
    #         ApiResponseHandler.RaiseHttpException(HTTP_RESPONSE_STATUS_INTERNAL_ERROR, f"invalid parameter {nApiParameter}, use {nMin} ~ {nMax}")

    #     return ERR_OK
    
    





