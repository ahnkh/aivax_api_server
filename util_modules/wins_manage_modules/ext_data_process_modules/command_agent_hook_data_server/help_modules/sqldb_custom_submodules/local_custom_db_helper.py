
from lib_include import *

from common_modules.type_hint import *

'''
grpc의 데이터 처리, local db
wins db에 저장 (local custom), 저장 로직도 위임.
'''

class LocalCustomDBHelper:

    def __init__(self):

        pass


    #broserHook 관련 부가 기능의 처리 - DB 저장
    def WriteBrowserHookMessageToDB(self, 
            nAgentID:int, 
            strPromptQuery:str, 
            strSessionID:str,
            strUserRule:str,
            bAllowed:bool,
            strModifiedQuery:str, 
            strReason:str, 
            dictDBResult:dict):

        '''
        #DB에 저장한다.
        #TODO: 최종 개발 시점에는 DB에 대한 데이터 큐 모듈로 전달, 비동기 처리를 수행하는 구조로 변경한다.
        #TODO: 여기서 처리가 아닌, bulk queue에 전달후, 모아서 저장하는 구조로 향후 개발한다.

        TOOD: 일단 BrowserHookReponse의 저장은 남기고
        나머지 MariaDB는 mongodb등 다른 DB를 검토한다.
        TODO: Helper는 중계기로 단순화 하고 (gprc proxy는 선언 최소화), 다시 각 helper로 위임한다.
        '''

        #TODO: 함수화
        nAllowed = CONFIG_OPT_ENABLE if True == bAllowed else CONFIG_OPT_DISABLE
        # nAllowed:int = CONFIG_OPT_ENABLE

        # if False == bAllowed:
        #     nAllowed = CONFIG_OPT_DISABLE

        #TODO: 가공이 필요한것, allowed, modified query
        #이게 결정되면 다시 소스 코드 리펙토링
        #TOD: 프롬프트는 MariaDB에 저장한다. 별도로 로그 저장 개념으로 양쪽에 저장.

        #수집된 데이터, DB에 저장한다. (helper 호출)
        #우선 가능한 데이터를 만들고, 가공이 필요한 데이터를 수정하여 만든다.
        #TODO: Allowed, Modified query 두개 값을 별도 수정한다. 수정 함수 제공.
        dictDBInfo = {
            "agent_id" : nAgentID,
            "reg_date" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "prompt_query" : strPromptQuery,
            "session_id" : strSessionID,
            "user_role" : strUserRule,

            "allowed" : nAllowed, #기본값, 허용 TODO: 전달시에는 True/False로 전달해야 한다.
            "modified_query" : strModifiedQuery,
            "reason" : strReason, #일단 하드코딩
        }

        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_insert_to_browse_info", dictDBInfo, dictDBResult)

        return ERR_OK


    # #browser 요청 정보, DB에 저장
    # #TODO: 공통화 가능    
    # def InsertToHookRequest(self, strQueryMapID:str, dictBrowserDBInsertInfo:dict, dictDBResult:dict):

    #     # dictDBResult:dict = {}
    #     #rdb_insert_to_browse_info

    #     sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, strQueryMapID, dictBrowserDBInsertInfo, dictDBResult)

    #     return ERR_OK


