
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

'''
kshell local json config
helper 클래스, 무상태 패턴, 초기 기동시 호출, dictionary로 관리
GlobalResourceManager의 helper 모듈로 활용한다.
'''

class LocalJsonConfigHelper:
    
    def __init__(self):
        pass
    
    #설정 config 초기화 - TODO: 약간의 customize, baseconfig의 인식 기능은 필요하다
    def InitializeLocalConfig(self, strLocalBaseConfigPath:str, dictJsonLocalConfig:dict) -> int:
        
        '''
        config 파일의 merge, local 설정으로 관리한다.
        
        base config의 path를 읽어서, 그 이하 설정된 config 값을 읽어온다. 
        key를 토대로 merge 한다.
        지정된 경로를 읽어서, merge한다. config 경로를 외부에서 지정한다.
        
        config 이하 subconfig를 merge하여 dictionary를 반환한다.
        
        TODO: base-config.json 의 위치는 상수로 관리하여 전달받는다. 이후 처리는 JsonConfigHelper 에서 처리.            
        '''
        
        #TODO: 우선 호출 인터페이스 부터, 세부 구현은 이후에.
        
        #구현이 복잡할수 있다. 단, 앞으로 python은 kshell을 확장하는 전략으로, 여기서 모두 개발한다.
        
        LOG().debug("intialize local config root")
        
        #큰 고민 없이, baseconfig는 jsonHelper로 읽어들인다.
        #main config에 이름으로 업데이트 해야 한다.
        JsonHelperX.JsonFileToDictionary(strLocalBaseConfigPath, dictJsonLocalConfig)
        
        #리소스 정보를 읽어들인다. - 25.06.17 구조 변경
        #파일의 내용을 읽어서, globalresource로 치환후, dictionary로 변환후, root에 추가
        #기존과 거의 같은 형상 유지.
        self.__mergeGlobalResourceConfig(dictJsonLocalConfig)
        
        #이후 baseconfig에 지정된 설정값을 merge
        self.__mergeSubJsonConfig(dictJsonLocalConfig)
        
        #TODO: 설정 config에 한정해서 기능을 부여한다. 이후 처리는 다른 모듈에서 처리.
        
        return ERR_OK
    
    ######################################################### private
    
    # 전역 설정, base-config 에서 가져온다. global-config는 반복해서 읽는 것으로 하자.
    def __mergeGlobalResourceConfig(self, dictJsonLocalConfig:dict):
        
        '''
        global-config 에서 reserved_keyword를 가져온다.
        resource-config 의 파일을 읽어서 string으로 변환한다.
        string 치환 => reserved keyword, 이 기능은 공통화
        치환된 string을 dictionary로 변환, json local config에 병합, 기존과 동일한 사양이어야 한다.
        
        TODO: global_config 부분에 대해서, 반복해서 사용하기에, 함수화를 검토, 우선 만들고 진행
        '''
        
        # global_config:dict = dictJsonLocalConfig.get("global_config")
        
        # #reseved_keyword 이하 예약어를 설정 config 문자열에서 치환한다.
        # reserved_keyword:dict = global_config.get("reserved_keyword")
        
        resource_config:str = dictJsonLocalConfig.get("resource_config")
        
        #여기서 부터 공통화
        self.__readJsonConfig(resource_config, dictJsonLocalConfig)
        
        return ERR_OK
    
    #읽어들인 base config에서 sub config를 merge 한다. 편의성
    def __mergeSubJsonConfig(self, dictJsonLocalConfig:dict):
        
        '''
        base config, local_resource 기준으로 경로를 읽어 들인다.
        
        "local_config_list":
        [
            {"name" : "ext_config_atoh", "path" : "local_resource/config/subconfig/ext_config_atoh.json"},
            {"name" : "ext_config_itop", "path" : "local_resource/config/subconfig/ext_config_itop.json"},
            {"name" : "ext_config_qtoz", "path" : "local_resource/config/subconfig/ext_config_qtoz.json"}
        ],
        
        #TODO: 초기설정이라, 별다른 예외처리는 하지 않는다. 에러가 발생하면 바로 노출된다.
        #TODO: 이름을 그대로 써야 하기에, 가독성을 늘리자.
        '''
        
        #base-config에 지정된 local config
        local_config_list:list = dictJsonLocalConfig.get("local_config_list")
        
        for dictLocalConfig in local_config_list:
            
            name = dictLocalConfig.get("name")
            path = dictLocalConfig.get("path")
            
            LOG().debug(f"merge sub config, name = {name}, path = {path}")
            
            #key=value 구조를 포기하고, 하나로 통일한다.
            #결국 여기서 변경된 부분은 include 기능과 global keyword 기능이다.
            self.__readJsonConfig(path, dictJsonLocalConfig)
        
        return ERR_OK
    
    #하위 json을 dictionary로 치환한다. 공통, 개별 치환
    def __readJsonConfig(self, strJsonPath:str, dictJsonLocalConfig:dict):
        
        '''
        예약된 키워드로 변환한다. => 키워드도 정해진 규칙에 의해, 읽어서 반환
        '''
        
        global_config:dict = dictJsonLocalConfig.get("global_config")
        
        #reseved_keyword 이하 예약어를 설정 config 문자열에서 치환한다.
        reserved_keyword:dict = global_config.get("reserved_keyword")
        
        #지정된 json 파일을 읽는다. 파일을 읽어서
        strConfigData:str = FileIOHelperX.OpenFileAsUTFToStream(strJsonPath)
        
        #지정된 키워드, 치환.
        for strKey in reserved_keyword:
            
            strData = reserved_keyword.get(strKey)
            
            strConfigData = strConfigData.replace(strKey, strData)
            
        #치환후, json으로 변환 및 jsonConfig에 저장 => TODO: 한줄로 해결이 될것 같다.
        
        nErrLoadResult = JsonHelperX.LoadToDictionary(strConfigData, dictJsonLocalConfig)
            
        #실패하면 exception, TODO: 예외처리 공통화는 필요
        if ERR_FAIL == nErrLoadResult:
            # LOG().error(f"fail load sub config {path}")
            # raise Exception(f"fail load sub config {strJsonPath}")
            GlobalCommonModule.RaiseException(ErrorDefine.CLI_GLOBAL_INIT_ERROR, ErrorDefine.CLI_GLOBAL_INIT_ERROR, f"fail load sub config {strJsonPath}")        
            return ERR_FAIL
        
        return ERR_OK
        
        