
from lib_include import *

from common_modules.type_hint import *

'''
SQLMap Interface 관련 명령 실행
'''

class SQLMapCliCommand:

    def __init__(self):
        pass

    #SQLMap 명령, CLI로 호출한다.
    def RunCommand(self, dictOpt:dict, dictSQLCliProcessModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        dbb : 기본 RDB
        id : sqlmap id
        parameter는 그대로 전달
        result 반환

        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_insert_to_browse_info", dictDBInfo, dictDBResult)
        '''

        LOG().info("run sql map cli command")

        apiResponseHandler.attachApiCommandCode("sql map cli command")

        #sqlmap id
        id = dictOpt.get(KShellParameterDefine.ID)

        #나머지 파라미터, 그대로 전달, 파라미터에서 호환성을 보장.

        dictDBResult = {}

        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, id, dictOpt, dictDBResult)

        apiResponseHandler.attachSuccessCode(dictDBResult)

        return ERR_OK