
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

'''
login 인증 기능 제공
'''

class LoginCommand:

    def __init__(self):

        pass


    def RunCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        DB를 조회한다. ID, PASSWORD를 입력받는다.
        PASSWORD는 sha256 hash를 우선 받는다. 비교한다. 
        일치하면 성공, 불일치하면 오류 => 오류에시지 처리
        TODO: 응답데이터, 맞출것.
        '''

        LOG().info("login authenticate command")

        apiResponseHandler.attachApiCommandCode("login command")

        # apiResponseHandler.attachSuccessCode(f"run process, port = {port}")

        userID = dictOpt.get(KShellParameterDefine.ID)
        userPassword = dictOpt.get(KShellParameterDefine.PASSWORD)

        #TODO: 결과에 따른 조건 응답값 분기 정의 필요
        #우선 나열: DB 조회 실패, 패스워드 미스매치, 입력값 미정의

        #DB 조회.
        dictDBResult = {}
        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_select_user_account_login", {"user_id" : userID}, dictDBResult)

        #TODO: 데이터가 없으면, None 이다.
        dictQueryData:dict = dictDBResult.get(DBSQLDefine.QUERY_DATA)

        if None == dictQueryData:            
            GlobalCommonModule.RaiseHttpException(WinsErrorDefine.API_APP_LOGIN_EROR, WinsErrorDefine.API_APP_LOGIN_ERROR_MSG, f"no user account found, not exist, id = {userID}")
            return ERR_FAIL

        #패스워드를 추출, 데이터 비교
        #TODO: 우선 개발하고, 향후 리펙토링
        USER_PASSWD:str = dictQueryData.get("USER_PASSWD") #password, description 구조상 대문자.

        #일단 입력값과 비교, 어떻게 변환할지는 향후 UI와 협의 한다.
        if userPassword != USER_PASSWD:
            #TODO: api command에서의 오류는 가급적 Exception            
            GlobalCommonModule.RaiseHttpException(WinsErrorDefine.API_APP_LOGIN_EROR, WinsErrorDefine.API_APP_LOGIN_ERROR_MSG, f"password is not mismatch, id = {userID}")
            return ERR_FAIL


        #마지막에 성공메시지.
        apiResponseHandler.attachSuccessCode(f"login success")

        return ERR_OK