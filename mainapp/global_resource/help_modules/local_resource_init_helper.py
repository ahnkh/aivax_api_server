
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

'''
내부 물리 자원, 디렉토리, 파일 등 초기화 기능 관리
'''

class LocalResourceInitHelper:
    
    def __init__(self):
        pass
    
    # 초기화, 최초 기동시 실행
    def InitializeResource(self, dictJsonLocalConfigRoot:dict):
        
        '''
        제공 기능 
        - CONFIG에 지정된 경로의 디렉토리 생성 (최대한 상대 경로, 또는 global.json 이하 경로)
        TODO: 오류 발생은, exception으로 처리.
        '''
        
        #TODO: 향후를 위해서, initial_local_resource를 확장한다고 가정하고 처리
        initial_local_resource = dictJsonLocalConfigRoot.get("initial_local_resource")
        
        #설정 config의 내용 - 우선 디렉토리의 초기화 기능 추가
        #경로에 지정된 디렉토리, 자동 생성한다. 디렉토리 생성 기능은 khanlib로 모듈화
        self.__initalizeGlobalDirectory(initial_local_resource)
        
        return ERR_OK
    
    ############################################ private
    
    #디렉토리 초기화
    def __initalizeGlobalDirectory(self, dictInitialLocalResource:dict):
        
        '''
        '''
        
        LOG().info("initialize global directory")
        
        # default_init_directory 정보, 디렉토리만 처리
        default_init_directory:dict = dictInitialLocalResource.get("default_init_directory")
        
        # 디렉토리 리스트
        directory_list_group:list = default_init_directory.get("directory_list_group")
        
        #지정된 디렉토리, 생성한다.
        for dictDirectoryList in directory_list_group:
            
            #초기화 경로, 리스트로 관리된다.
            directory_list:list = dictDirectoryList.get("directory_list")
            
            for strDirectory in directory_list:
            
                #디렉토리, 생성한다.
                FileIOHelper.CreateDirectory(strDirectory)
        
        return ERR_OK
        
