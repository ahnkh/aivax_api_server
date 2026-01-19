
#외부 라이브러리
from lib_include import *

'''
ApiRouter, 생성 모듈, router와 같이 움직인다.
'''

class ApiRouterGenerator:

    def __init__(self):
        pass
    
    #router, 공통 설정 부분. => 그냥 유지하자.
    def CreateApiRouter(dictLocalConfig: dict) -> APIRouter:

        '''
        API Router, 공통화
        '''

        prefix = dictLocalConfig.get("prefix")

        if None == prefix:
            prefix = ""

        router = APIRouter(prefix=prefix)
        return router

    #route 정보, config에서 추가    
    def AddRouteInfoFromConfig(lstRouteLocalConfig: list, routeImpl: Any, router:APIRouter, apiKeyCheckMethod: Any = None):

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
    
    





