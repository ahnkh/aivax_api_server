
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

'''
'''

class LocalJsonConfigHelper:
    
    def __init__(self):
        pass
    
    
    def InitializeLocalConfig(self, strLocalBaseConfigPath:str, dictJsonLocalConfig:dict) -> int:
        
        '''
        '''
        
        LOG().debug("intialize local config root")
        
        JsonHelperX.JsonFileToDictionary(strLocalBaseConfigPath, dictJsonLocalConfig)
        
        self.__mergeGlobalResourceConfig(dictJsonLocalConfig)
        
        self.__mergeSubJsonConfig(dictJsonLocalConfig)
        
        return ERR_OK
    
    ######################################################### private
    
    def __mergeGlobalResourceConfig(self, dictJsonLocalConfig:dict):
        
        '''
        '''
        resource_config:str = dictJsonLocalConfig.get("resource_config")
        
        self.__readJsonConfig(resource_config, dictJsonLocalConfig)
        
        return ERR_OK
    
    def __mergeSubJsonConfig(self, dictJsonLocalConfig:dict):
        
        '''
        '''
        
        local_config_list:list = dictJsonLocalConfig.get("local_config_list")
        
        for dictLocalConfig in local_config_list:
            
            name = dictLocalConfig.get("name")
            path = dictLocalConfig.get("path")
            
            LOG().debug(f"merge sub config, name = {name}, path = {path}")
            
            self.__readJsonConfig(path, dictJsonLocalConfig)
        
        return ERR_OK
    
    def __readJsonConfig(self, strJsonPath:str, dictJsonLocalConfig:dict):
        
        '''
        '''
        
        global_config:dict = dictJsonLocalConfig.get("global_config")
        
        reserved_keyword:dict = global_config.get("reserved_keyword")
        
        strConfigData:str = FileIOHelperX.OpenFileAsUTFToStream(strJsonPath)
        
        for strKey in reserved_keyword:
            
            strData = reserved_keyword.get(strKey)
            
            strConfigData = strConfigData.replace(strKey, strData)
            
        
        nErrLoadResult = JsonHelperX.LoadToDictionary(strConfigData, dictJsonLocalConfig)
            
        if ERR_FAIL == nErrLoadResult:
            GlobalCommonModule.RaiseException(ErrorDefine.CLI_GLOBAL_INIT_ERROR, ErrorDefine.CLI_GLOBAL_INIT_ERROR, f"fail load sub config {strJsonPath}")        
            return ERR_FAIL
        
        return ERR_OK
        
        