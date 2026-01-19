
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

'''
custom sql 명령 - filter view 명령
'''

class FilterViewDetailSQLCommand:
    
    def __init__(self):
        pass
    
    def RunCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        
        #detail cmd 이하 추가적인 하위 command
        detail_sub_cmd = dictOpt.get(KShellParameterDefine.DETAIL_SUB_CMD)
        
        if WinsCommandDefine.DETAIL_SUB_CMD_FILTER_VIEW_ADD == detail_sub_cmd:
            
            pass
            
        elif WinsCommandDefine.DETAIL_SUB_CMD_FILTER_VIEW_EDIT == detail_sub_cmd:
            
            pass
        
        elif WinsCommandDefine.DETAIL_SUB_CMD_FILTER_VIEW_DELETE == detail_sub_cmd:
            
            pass
        
        elif WinsCommandDefine.DETAIL_SUB_CMD_FILTER_VIEW_LIST == detail_sub_cmd:
            
            pass
        
        else:
            GlobalCommonModule.RaiseHttpException(WinsErrorDefine.API_ROUTER_COMMAND_ERROR, WinsErrorDefine.API_ROUTER_COMMAND_ERROR_MSG, f"unknown user account detail sub command {detail_sub_cmd}")
            return ERR_FAIL
        
        return ERR_OK