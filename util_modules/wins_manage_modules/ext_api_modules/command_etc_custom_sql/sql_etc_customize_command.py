
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

'''
기타 SQL command 명령 관리
'''

class SQLEtcCustomizeCommand:
    
    def __init__(self):
        pass
    
    def RunCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        
        LOG().info("sql etc customize command")
        
        detail_cmd = dictOpt.get(KShellParameterDefine.DETAIL_CMD)
        
        if WinsCommandDefine.DETAIL_CMD_CUSTOM_USER_GROUP == detail_cmd:
            
            from util_modules.wins_manage_modules.ext_api_modules.command_etc_custom_sql.detail_command.user_group_detail_sql_command import UserGroupDetailSQLCommand
            
            detailCommand = UserGroupDetailSQLCommand()
            detailCommand.RunCommand(dictOpt, dictWinsApiModuleLocalConfig, apiResponseHandler)
            pass
        
        elif WinsCommandDefine.DETAIL_CMD_CUSTOM_FILTER_VIEW == detail_cmd:
            
            from util_modules.wins_manage_modules.ext_api_modules.command_etc_custom_sql.detail_command.filter_view_detail_sql_command import FilterViewDetailSQLCommand
            
            detailCommand = FilterViewDetailSQLCommand()
            detailCommand.RunCommand(dictOpt, dictWinsApiModuleLocalConfig, apiResponseHandler)
            pass
        
        elif WinsCommandDefine.DETAIL_CMD_CUSTOM_ETC_SQL_COMMAND == detail_cmd:
            
            from util_modules.wins_manage_modules.ext_api_modules.command_etc_custom_sql.detail_command.etc_detail_sql_command import EtcDetailSQLCommand
            
            detailCommand = EtcDetailSQLCommand()
            detailCommand.RunCommand(dictOpt, dictWinsApiModuleLocalConfig, apiResponseHandler)
            pass
        
        else:
            GlobalCommonModule.RaiseHttpException(WinsErrorDefine.API_ROUTER_COMMAND_ERROR, WinsErrorDefine.API_ROUTER_COMMAND_ERROR_MSG, f"unknown user account detail command {detail_cmd}")
            return ERR_FAIL
        
        return ERR_OK