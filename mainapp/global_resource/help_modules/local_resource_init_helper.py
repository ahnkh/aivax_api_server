
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

'''
'''

class LocalResourceInitHelper:
    
    def __init__(self):
        pass
    
    def InitializeResource(self, dictJsonLocalConfigRoot:dict):
        
        '''
        '''
        
        initial_local_resource = dictJsonLocalConfigRoot.get("initial_local_resource")
        
        self.__initalizeGlobalDirectory(initial_local_resource)
        
        return ERR_OK
    
    ############################################ private
    
    def __initalizeGlobalDirectory(self, dictInitialLocalResource:dict):
        
        '''
        '''
        
        LOG().info("initialize global directory")
        
        default_init_directory:dict = dictInitialLocalResource.get("default_init_directory")
        
        directory_list_group:list = default_init_directory.get("directory_list_group")
        
        for dictDirectoryList in directory_list_group:
            
            directory_list:list = dictDirectoryList.get("directory_list")
            
            for strDirectory in directory_list:
            
                FileIOHelper.CreateDirectory(strDirectory)
        
        return ERR_OK
        
