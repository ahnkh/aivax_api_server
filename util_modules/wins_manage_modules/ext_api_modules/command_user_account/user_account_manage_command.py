
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

'''
사용자 계정, 등록 등 관리 명령
패스워드, 사용자 유효성등 검증.
조회, 추가, 수정, 삭제 명령 제공 => Type으로 분기
'''

class UserAccountManageCommand:

    def __init__(self):
        pass

    def RunCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        '''

        LOG().info("user account manage command")
        
        # apiResponseHandler.attachApiCommandCode("user account command")
        
        detail_cmd = dictOpt.get(KShellParameterDefine.DETAIL_CMD)
        
        if WinsCommandDefine.DETAIL_CMD_ADD_USER == detail_cmd:
            
            pass
            
        elif WinsCommandDefine.DETAIL_CMD_EDIT_USER == detail_cmd:
            
            pass
        
        elif WinsCommandDefine.DETAIL_CMD_DELETE_USER == detail_cmd:
            
            pass
        
        elif WinsCommandDefine.DETAIL_CMD_LIST_USER == detail_cmd:
            
            from util_modules.wins_manage_modules.ext_api_modules.command_user_account.detail_command.user_account_list_detail_command import UserAccountListDetailCommand
            
            detailModule = UserAccountListDetailCommand()
            detailModule.ListUserAccount(dictOpt, dictWinsApiModuleLocalConfig, apiResponseHandler)
            
            pass
        
        else:
            
            GlobalCommonModule.RaiseHttpException(WinsErrorDefine.API_ROUTER_COMMAND_ERROR, WinsErrorDefine.API_ROUTER_COMMAND_ERROR_MSG, f"unknown user account detail command {detail_cmd}")
            return ERR_FAIL
            
        return ERR_OK
    
    
    





