
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

'''
custom sql 명령 - 그룹 명령
'''

class UserGroupDetailSQLCommand:
    
    def __init__(self):
        pass
    
    def RunCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        
        #detail cmd 이하 추가적인 하위 command
        detail_sub_cmd:str = dictOpt.get(KShellParameterDefine.DETAIL_SUB_CMD)
        
        if WinsCommandDefine.DETAIL_SUB_CMD_USER_GROUP_ADD == detail_sub_cmd:
            
            pass
            
        elif WinsCommandDefine.DETAIL_SUB_CMD_USER_GROUP_EDIT == detail_sub_cmd:
            
            pass
        
        elif WinsCommandDefine.DETAIL_SUB_CMD_USER_GROUP_DELETE == detail_sub_cmd:
            
            pass
        
        # elif WinsCommandDefine.DETAIL_SUB_CMD_USER_GROUP_LIST == detail_sub_cmd:
            
        #     #TODO: 조회로직, 그대로 parameter 전달
        #     #where 조건, query helper 공통 모듈 호출.
            
        #     pass
        
        else:
            GlobalCommonModule.RaiseHttpException(WinsErrorDefine.API_ROUTER_COMMAND_ERROR, WinsErrorDefine.API_ROUTER_COMMAND_ERROR_MSG, f"unknown user account detail sub command {detail_sub_cmd}")
            return ERR_FAIL
        
        return ERR_OK
    
    ######################################## private
    
    #사용자 데이터 조회, 우선 개발후 리펙토링
    def __selectUserGroupList(self, dictOpt:dict):
        
        '''
        sqlmap id와 파라미터를 받아온다.
        조회는, 공통 where 조건절을 생성한다.
        호출후 결과를 반환한다.
        '''
        
        sqlmap_id:str = dictOpt.get(KShellParameterDefine.ID)
        
        dictParameter:dict = {
            
        }
        
        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, sqlmap_id)
        
        
        
        return ERR_OK