
#외부 라이브러리
from lib_include import *

'''
외부 실행 옵션 관련
config, db, 외부 입력 인자를 가공하서, 실행 인자를 만든다.
추후 실행 관련 늘어날수 있다.
'''

class ConfigOptionParser:

    def __init__(self):        
        pass


    #설정값을 변환, 반환한다.
    def GatherWebConfigOption(self, dictWebServerConfig : dict, dictOpt:dict, dictJsonLocalConfigRoot: dict):

        '''
        설정값 적용 순서
        실행 파라미터 > DB 설정값 > 설정 config
        '''

        LOG().debug("gather web config option")

        #local 설정 config, db 또는 get opt 옵션이 없으면 config의 설정값을 읽는다.
        fast_api_server_config:dict = dictJsonLocalConfigRoot.get("fast_api_server_config")
        
        #ssl 설정 관련 => db로는 미설정, option으로는 설정
        #TODO: 거의 사용은 안하지만, ssl 설정도 option으로 가능하게 구조 변경
        strSSLKeyFilePath = fast_api_server_config.get(KShellParameterDefine.SSL_KEY_FILE_PATH)
        strSSLCertFilePath = fast_api_server_config.get(KShellParameterDefine.SSL_CERT_FILE_PATH)

        #host, port 같은 옵션 명으로 통일, 별도로 define을 생성하지 않는다.
        strFastApiHost = fast_api_server_config.get(KShellParameterDefine.HOST)
        nFastApiPort = int(fast_api_server_config.get(KShellParameterDefine.PORT))
        
        #최초, 설정 config로 가져온다.  => 설정 config를 기본값으로 사용하고, option이 있으면 덮어쓴다.
        strOptHost = dictOpt.get(KShellParameterDefine.HOST)
        nOptPort = dictOpt.get(KShellParameterDefine.PORT)
        
        strOptSSLCertFilePath = dictOpt.get(KShellParameterDefine.SSL_CERT_FILE_PATH)
        strOptSSLKeyFilePath = dictOpt.get(KShellParameterDefine.SSL_KEY_FILE_PATH)

        #log 출력 옵션, option으로만 제어, 기본 미사용
        bPrintLog = dictOpt.get(KShellParameterDefine.PRINT_LOG)

        if None != strOptHost:
            strFastApiHost = strOptHost
            LOG().info(f"update api parameter, host = {strFastApiHost}")

        if None != nOptPort:            
            nFastApiPort = int(nOptPort)
            LOG().info(f"update api parameter, port = {nFastApiPort}")
        
        if None != strOptSSLCertFilePath:
            strSSLCertFilePath = strOptSSLCertFilePath
            
        if None != strOptSSLKeyFilePath:
            strSSLKeyFilePath = strOptSSLKeyFilePath

        #설정 정보 업데이트, 거의 이 수준이 될것 같다.
        dictWebServerConfig[KShellParameterDefine.SSL_CERT_FILE_PATH] = strSSLCertFilePath
        dictWebServerConfig[KShellParameterDefine.SSL_KEY_FILE_PATH] = strSSLKeyFilePath

        dictWebServerConfig[KShellParameterDefine.HOST] = strFastApiHost
        dictWebServerConfig[KShellParameterDefine.PORT] = nFastApiPort

        #log 출력 옵션
        dictWebServerConfig[KShellParameterDefine.PRINT_LOG] = bPrintLog
        
        #시작시, 로그 출력은 필요
        #TODO: ssl은 기본으로 사용하자. => nginx도 ssl로 제공
        LOG().info(f"load web api config, host = {strFastApiHost}, port = {nFastApiPort}, ssl.cert = {strSSLCertFilePath}, ssl.key = {strSSLKeyFilePath}, print = {bPrintLog}")
        
        return ERR_OK