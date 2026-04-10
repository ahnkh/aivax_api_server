
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import * #WinsModuleDefine

'''
'''

class PipelineFilterPolicyHelper:
    
    def __init__(self):
        pass
    
    # regex 패턴 정책의 수집
    def GetRegexFilterPolicy(self, listRegexPattern:list):
        
        '''
        TODO: 전수 검증이 필요하다. => 모든 Regex 정책을 수집한다.
        '''
        
        dictDBResult = {}
        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_select_pipline_all_pattern_list", {}, dictDBResult)
        
        lstRegexPatternList:list = dictDBResult.get(DBSQLDefine.QUERY_DATA)
        
        listRegexPattern[:] = lstRegexPatternList
        # lstRegexPatternList.extend(listRegexPattern) #가독성이 좋으나, slice 방식이 더 적절하다.
        
        return ERR_OK