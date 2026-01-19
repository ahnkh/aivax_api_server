
import logging
import uvicorn
import socket

from lib_include import *

'''
Web App 실행 관리
인자가 늘어날수 있다.
'''

class WebAppRunner:

    def RunWebApiServer(self, apiServer : FastAPI, dictWebServerConfig: dict):

        '''
        TODO: 다중실행, 스레드 등도 고민 해야 함.
        '''

        # strApiPath = dictWebServerConfig.get(WebApiDefine.CONFIG_API_PATH)
        # bReload = bool(dictWebServerConfig.get(WebApiDefine.CONFIG_RELOAD))

        strSSLKeyFilePath = dictWebServerConfig.get(KShellParameterDefine.SSL_KEY_FILE_PATH)
        strSSLCertFilePath = dictWebServerConfig.get(KShellParameterDefine.SSL_CERT_FILE_PATH) 

        strFastApiHost = dictWebServerConfig.get(KShellParameterDefine.HOST)
        nFastApiPort = dictWebServerConfig.get(KShellParameterDefine.PORT)

        #로그 출력 옵션, 기본 미출력 => 여기는 작위적인데, 넘어가자.
        logLevel = logging.WARNING

        bPrintLog = dictWebServerConfig.get(KShellParameterDefine.PRINT_LOG)

        if None != bPrintLog and True == bPrintLog:
            LOG().info("use print log")
            logLevel = logging.INFO

        #TODO: 실제 사용하는 별도의 모듈과 전역 관리 객체가 필요.
        #결과적으로 app는 공유해야 하지 않을지 + 여러개 서버를 만들어야 할지. => 포트별로 한개이다.

        #포트를 체크, 기존에 존재하는 서버이면 실행 무시
        #TODO: 동일한 포트이면 port 바인드 오류가 떨어진다. 
        #다만, 지속적으로 체크는 문제.

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # nError = sock.connect_ex((WebApiLocalDefine.OPT_WEB_API_LOCAL_HOST,nWebApiPort))
        nError = sock.connect_ex((strFastApiHost,nFastApiPort))

        #반환값, 성공하면 0 아니면 error_no

        if 0 == nError:
            LOG().error(f"bind error, already use host = {strFastApiHost}, port = {nFastApiPort}")
            raise Exception(f"bind error, already use host = {strFastApiHost}, port = {nFastApiPort}")
            # return ERR_FAIL

        #137068, RockyLinux Swagger 관련 openapi 버전 고정
        openapi_schema = apiServer.openapi()
        openapi_schema["openapi"] = "3.0.2" 
        apiServer.openapi_schema = openapi_schema

        LOG().info(f"run uvicorn api server, host = {strFastApiHost}, port = {nFastApiPort}")

        uvicorn.run(    
            # strApiPath                    
            apiServer,
            port=nFastApiPort,
            host=strFastApiHost,
            # reload=bReload,
            ssl_keyfile=strSSLKeyFilePath,
            ssl_certfile=strSSLCertFilePath,
            log_level=logLevel, #2024.06.02 출력 옵션 추가
            root_path = ".", #nginx 테스트, root-path 추가
            loop="uvloop", 
            http="httptools",           
        )

        return ERR_OK

