
from fastapi.openapi.docs import (
    # get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from lib_include import *

'''
openapi 관련 router
이 router는 외부로 노출하지 않고 내부에서 작성한다.
'''

class OpenAPIRouter:
    
    def __init__(self):

        self.__webMainApp = None
        pass

    #OpenAPI, 기본 Api 자동 추가
    def InitializeRouter(self, webMainApp:Any, dictLocalConfig: dict) -> APIRouter:

        '''
        open api router는 router를 설정하지 않고, 소스에서 추가한다.
        '''

        from web_app_modules.web_api_mainapp import WebApiMainApp
        webMainAppRef:WebApiMainApp = webMainApp

        self.__webMainApp = webMainAppRef 

        router = APIRouter(prefix="")

        # #TODO: fastapi를 통한 전역 변수 교환 테스트
        router.add_api_route(path = "/docs", endpoint = self.custom_swagger_ui_html, methods=["GET"], include_in_schema=False)

        router.add_api_route(path = webMainAppRef.swagger_ui_oauth2_redirect_url, endpoint = self.swagger_ui_redirect, methods=["GET"], include_in_schema=False)

        #redoc은 openapi 에 노출 => 필요는 없다. 기본만 사용
        # router.add_api_route(path = "/redoc", endpoint = self.redoc_html, methods=["GET"], tags=["tms+"], include_in_schema=False, summary = "tms+ openapi 문서제공")

        return router

    #TODO: 이름을 기존 swagger, redoc 함수 그대로 사용
    async def custom_swagger_ui_html(self):

        '''
        '''

        from web_app_modules.web_api_mainapp import WebApiMainApp
        webMainApp = self.__webMainApp
        webMainAppRef:WebApiMainApp = webMainApp

        return get_swagger_ui_html(
            openapi_url = "/openapi.json",
            title = webMainAppRef.title,
            oauth2_redirect_url = webMainAppRef.swagger_ui_oauth2_redirect_url,
            swagger_js_url="/openapi/static/swagger-ui-bundle.js",
            swagger_css_url="/openapi/static/swagger-ui.css",
        )
    
    async def swagger_ui_redirect(self):
        return get_swagger_ui_oauth2_redirect_html()
    

    # async def redoc_html(self):

    #     '''
    #     **TMS+ OpenAPI 문서 (redoc)**
    #     - * 제공되는 API의 문서 가이드를 제공합니다.
    #     '''

    #     webApp = self.__webMainApp

    #     return get_redoc_html(
    #         openapi_url="/openapi.json",
    #         #전역변수 테스트
    #         title = webApp.title,            
    #         redoc_js_url = "/openapi/static/redoc.standalone.js",
    #     )

