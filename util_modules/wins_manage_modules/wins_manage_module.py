
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

class WinsManageModule:

    def __init__(self):
        pass
    
    def RunModule(self, dictOpt:dict, dictJsonLocalConfigRoot:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        self.__runModule(dictOpt, dictJsonLocalConfigRoot, apiResponseHandler)

        return ERR_OK

    def __runModule(self, dictOpt:dict, dictJsonLocalConfigRoot:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        ext_module = dictOpt.get(KShellParameterDefine.EXT_MODULE)
        
        strLocalModuleConfigName:str = ""

        if WinsCommandDefine.EXT_MODULE_MANAGE_WINS_DATA_PROCESS == ext_module:

            strLocalModuleConfigName = "wins_data_process_module"

        elif WinsCommandDefine.EXT_MODULE_MANAGE_WINS_API_MODULE == ext_module:

            strLocalModuleConfigName = "wins_api_module"

        else:            
            GlobalCommonModule.RaiseException(ErrorDefine.CLI_COMMAND_ERROR, ErrorDefine.CLI_COMMAND_ERROR_MSG, f"not defined ext module {ext_module}", apiResponseHandler)
            return ERR_FAIL

        GlobalCommonModule.ExecuteUtilCliInstanceMethod(dictOpt, dictJsonLocalConfigRoot, strLocalModuleConfigName, apiResponseHandler)
            
        return ERR_OK