
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

'''
SQLDB조회, helper
TODO: 다른 모듈도 사용필요시 common_modules로 이동
'''

class WinsSQLDBHelper:
    
    def __init__(self):
        pass
    
    #sql 조회, custom 조회, 공통 포맷
    def RunSQLCustomSelectQuery(self, strSqlMapID:str, dictWhereCondition:dict, nLimit:dict, dictDBOutResult:dict):
        
        '''
        where, limit를 공통으로 갖는다.
        
        "limit" : 100
        "condition": => 우선 and 조건만
        {
            "user_id" : "root001",
            "login_status" : 0,
            "user_flag" : 1
        }
        
        "complex_condition": => 항후 개발
        [
            {"field": "user_id", "value": "root001", "operand": "and"}
        ]
        
        #TODO: 향후 group 쿼리도 고민.
        '''
        
        queryHelper:QueryHelperX = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_QUERY_HELPER)
        
        #where절, 공통 패턴으로 만든다. POST parameter로 받는다.
        strWhere = queryHelper.GenerateBaseConditionWhereQuery(dictWhereCondition)
        
        dictParameter:dict = {
            WinsCommandDefine.WHERE : strWhere,
            WinsCommandDefine.LIMIT : nLimit
        }
        
        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, strSqlMapID, dictParameter, dictDBOutResult)
        
        return ERR_OK
    
    ###################################### private
    
    