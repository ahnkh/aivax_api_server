
#외부 라이브러리
from lib_include import *

from common_modules.type_hint import *

from util_modules.operation_util_manage_modules.local_etc_common.local_etc_define import *

'''
범용 유틸리티 모듈 명령 관리
'''

class OperationUtilManageModule:

    def __init__(self):
        pass

    def RunModule(self, dictOpt:dict, dictJsonLocalConfigRoot:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        self.__runModule(dictOpt, dictJsonLocalConfigRoot, apiResponseHandler)

        return ERR_OK
    
    ############################################################# private


    def __runModule(self, dictOpt:dict, dictJsonLocalConfigRoot:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        ext_module = dictOpt.get(KShellParameterDefine.EXT_MODULE)

        LOG().debug(f"run module, ext_module = {ext_module}")

        strLocalModuleConfigName:str = ""

        if UtilCommandDefine.EXT_MODULE_MANAGE_SQL_CLI_MODULE == ext_module:

            strLocalModuleConfigName = "operation.sql_cli_process_module"
            # pass
            
        elif UtilCommandDefine.EXT_MODULE_MANAGE_ETC_UTIL_MODULE == ext_module:
            strLocalModuleConfigName = "operation.sql_cli_process_module"
            #pass
        else:            
            GlobalCommonModule.RaiseHttpException(UtilErrorDefine.CLI_COMMAND_ERROR, UtilErrorDefine.CLI_COMMAND_ERROR_MSG, f"not defined ext module {ext_module}", apiResponseHandler)
            return ERR_FAIL

        GlobalCommonModule.ExecuteUtilCliInstanceMethod(dictOpt, dictJsonLocalConfigRoot, strLocalModuleConfigName, apiResponseHandler)

        return ERR_OK
    