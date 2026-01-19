
from lib_include import *

from common_modules.type_hint import *

'''
scheduler daemon 구현
'''

class ScheduleDaemonCommand:
    
    def __init__(self):
        pass
    
    #schedule daemone command 실행.
    def RunCommand(self, dictOpt:dict, dictScheduleDaemonLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        dbb : 기본 RDB
        id : sqlmap id
        parameter는 그대로 전달
        result 반환

        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_insert_to_browse_info", dictDBInfo, dictDBResult)
        '''

        LOG().info("run schedule daemon command")

        apiResponseHandler.attachApiCommandCode("schedule daemon command")

        
        # apiResponseHandler.attachSuccessCode(dictDBResult)

        return ERR_OK
