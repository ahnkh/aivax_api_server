
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

#local config 관리
from mainapp.global_resource.help_modules.local_json_config_helper import LocalJsonConfigHelper

from mainapp.global_resource.help_modules.local_resource_init_helper import LocalResourceInitHelper

'''
전역 리소스 관리 - 초기에 생성해야 할 리소스가 있으면
여기서 추가, 관리
'''

class KShellGlobalResourceManager:
    
    def __init__(self):
        
        #빠른 초기화가 좋으나, 이정도 초기화는 수행한다.
        self.__dictJsonLocalConfigRoot = {}
        
        #DB 관리, DB 쿼리맵은 공통으로 필요할 것 같다. 
        #DB 접속 인스턴스는 싱글턴 처리.        
        pass
    
    #Application 전역 초기화, 지연된 생성자 개념
    def InitializeResource(self, dictOpt:dict):
        
        '''Create
        초기 설정, config 초기화
        DB, SQLMap 초기화
        TODO: 예외처리에 대한 고민. => 여기는 반드시 생성되어야 하는 위치이다. 
        GlobalInstanceFactory와 더불어 raise exception 처리.
        다만 미래를 위해, 한줄이라도 함수로 분리.
        '''
        
        #디렉토리, 자원등 설정과 필요없는 필수 초기화 - 현재는 필요 없음.
        
        #내부 설정 config 초기화, 우선 틀을 잡자.
        # nErrInitializeLocalConfig = self.__initializeLocalConfigRoot(dictOpt)
        self.__initializeLocalConfigRoot(dictOpt)
        
        # if ERR_FAIL == nErrInitializeLocalConfig:
        #     LOG().error("fail initialize local config root")
        #     return ERR_FAIL
        
        #전역 인스턴스 관리, TODO: 로컬 설정에 대한 고려도 같이 한다.        
        #singleton + Factory 패턴으로 제공, static은 지양한다.
        #기본적인 예외처리수준, instance가 초기화 되지 않으면 초기화 실패.
        
        #local config, 설정 정보의 최초 시작값
        dictJsonLocalConfigRoot = self.__dictJsonLocalConfigRoot
        
        #Factory Module, 최초 생성해야 한다.
        #TODO: 순서가 중요한점을 잊지 말자.
        self.__initializeFactoryInstance(dictJsonLocalConfigRoot)
        
        #Global 모듈 생성, FactoryInstance 생성후 초기화
        #불필요 기능, 제거 => GlobalCommonModule은 상태가 존재하지 않게 설계.
        # self.__initializeGlobalCommonModule()
        
        # 전역 리소스 관리, 데이터 및 디렉토리 초기화
        self.__initializeGlobalLocalResource(dictJsonLocalConfigRoot)

        # DB 관리 모듈, 대표 모듈의 생성
        self.__initializeDBModule(dictOpt, dictJsonLocalConfigRoot)
        
        # 이후 전역 객체, 미리 생성 - SQLMap        
        # nErrInitializeSQLInterface = self.__initializeSQLInterface(dictOpt, self.__dictJsonLocalConfigRoot)
        # TODO: 아직 미구현, 추가 구현 필요
        # self.__initializeSQLInterface(dictOpt, dictJsonLocalConfigRoot)
        
        #http 객체의 초기화
        self.__initializeHttpRequest(dictOpt, dictJsonLocalConfigRoot)
                
        return ERR_OK
    
    #전역 리소스 해제.
    def DisposeGlobalResource(self, strDisposeMethodName:str):

        '''
        '''

        instanceFactory:GlobalInstanceFactory = GlobalInstanceFactory.singletonInstance()
        instanceFactory.DisposeInstance(strDisposeMethodName)

        return ERR_OK
    
    ######################################################### resource getter/setter
    
    #local config 반환
    def GetLocalConfigRoot(self) -> dict:
        return self.__dictJsonLocalConfigRoot
    
    ######################################################### private
    
    #각 항목별 초기화
    def __initializeLocalConfigRoot(self, dictOpt:dict) -> int:
        
        '''
        local config 의 초기화
        여기에 한해, jsonLocalConfig 인스턴스, 멤버 변수 종속성 허용.
        '''
        
        LOG().debug("initialize local config root")
        
        #설정 config path, TODO: path를 어떻게 잡아야 할지.
        #TODO: local 리소스는 어떻게 관리할지. => GlobalInitManager를 전달하는 방향도 고려
        #base config를 통해서 읽어 들인다. 이후 customize는 들어간다.nErrInitializeResource 다만 최소화.
        strConfigBasePath:str = dictOpt.get(KShellParameterDefine.CONFIG_BASE_PATH)
        
        #최초 설정값 관리, local config
        #TODO: 설정값을 dictionary로 하여서 참조 인자로 전달한다.
        localJsonConfigHelper = LocalJsonConfigHelper()
        #TODO: local config 부분은 우선 예외처리 제외, exception으로 처리.
        localJsonConfigHelper.InitializeLocalConfig(strConfigBasePath, self.__dictJsonLocalConfigRoot)
        
        return ERR_OK
    
    # 전역 리소스 (디스크, 변수 등) 초기화 기능 추가
    def __initializeGlobalLocalResource(self, dictJsonLocalConfigRoot:dict):
        
        '''
        기본적으로 생성해야 할 리소스의 초기화
        종속성은 최소화 해야 겠지만, 리소스 상태 점검을 위해서도 필요한 기능
        '''
        
        #초기 디렉토리 생성, 각 모듈 내에서 초기화를 해야 겠지만, 기본적인 초기화 설정은 필요
        #python 모듈을 활용, windows, linux 공통적으로 사용, 상대 경로 개념으로 접근
        
        localResourceHelper = LocalResourceInitHelper()
        localResourceHelper.InitializeResource(dictJsonLocalConfigRoot)
        
        return ERR_OK
    
    #Factory Instance, GlobalModule 통일해서 초기화, TODO: 에외처리는 없다.
    def __initializeFactoryInstance(self, dictJsonLocalConfigRoot:dict):
        
        '''
        반복 주석, 예외처리는 raise exception으로 처리한다.
        Global Resource Manager는 반드시 초기화가 성공해야 하고, 그게 아니면 예외를 발생시킨다.
        '''
        
        LOG().debug("initialize factory instance")
        
        # nErrInitializeInstanceFactory = GlobalInstanceFactory.createFactoryInstance(self.__dictJsonLocalConfigRoot)
        GlobalInstanceFactory.createFactoryInstance(dictJsonLocalConfigRoot)
        
        return ERR_OK

    #DB 처리 모듈, 관리 class의 생성
    def __initializeDBModule(self, dictOpt:dict, dictJsonLocalConfigRoot:dict) -> int:

        '''
        DB 생성 모듈의 초기화, SQLMap, DBHelper, SQLInterface를 관리하는 모듈의 생성
        TODO: SQLMap 모듈도, 해당 Instance에서 생성하도록 이관.
        '''
        
        sqlClientInterface:SQLClientInterface = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_SQL_CLIENT_INTERFACE)
        
        #모듈 초기화, 실패시 exception
        sqlClientInterface.Initialize(dictOpt, dictJsonLocalConfigRoot)

        return ERR_OK
    
    #http 모듈 객체의 초기화
    def __initializeHttpRequest(self, dictOpt:dict, dictJsonLocalConfigRoot:dict):
        
        '''
        TODO: library의 초기화 이다. 어디까지 오염될지 신중하게 초기화 한다.
        HttpRequest 모듈내에서 Factory로 전달되는게 맞을듯 한데, Global Module vs HttpRequest 
        각각 어디가 좋을지 선정해 보자.
        '''
        
        LOG().debug("initialize http request")
        
        #http query map, local config 내, 설정 정보를 가져온다.
        http_query_map:dict = dictJsonLocalConfigRoot.get("http_query_map")
        
        http_query_map_list:list = http_query_map.get("http_query_map_list")
        
        # http_request 모듈도 Instance Factory 에 추가.
        httpRequest:HttpRequestInterface = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_HTTP_REQUEST_INTERFACE)
        
        #TODO: 설정 정보 필요 => 여기 변경
        #TODO: 초기화 오류는 exception 발생으로 처리.        
        httpRequest.Initialize(http_query_map_list)
        
        return ERR_OK