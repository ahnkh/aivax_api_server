
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

'''
사용자 계정 조회 명령 detail command
'''

class UserAccountListDetailCommand:
    
    def __init__(self):
        
        self.__customDBHelper = WinsSQLDBHelper()
        pass
    
    
    #사용자 계정 조회 명령 실행
    def ListUserAccount(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        사용자 계정을 조회한다.
        조건식을 받아서 where 쿼리를 만든다.
        조건식이 없으면 전체 조회가 되도록 처리한다. ({where}로 제어)
        where, limit 두개를 제공한다.
        '''
        
        apiResponseHandler.attachApiCommandCode("user account list command")
        
        
        #sqlmap id, 이건 변경 가능해서, 별도의 파라미터로 받는다.
        sqlmap_id:str = dictOpt.get(KShellParameterDefine.ID)
        
        dictCondition:dict = dictOpt.get(KShellParameterDefine.CONDITION)
        
        limit:int = dictOpt.get(KShellParameterDefine.LIMIT)
        
        # strSQLMapID:str = "rdb_select_user_account"
        
        dictDBOutResult = {}
        self.__customDBHelper.RunSQLCustomSelectQuery(sqlmap_id, dictCondition, limit, dictDBOutResult)
        
        # #where절을 동적으로 생성한다.
        # strWhere:str = self.__generateWhereSQLCondition(dictOpt)
        
        # #옵션절, 별도 parameter로 받는다.
        # limit:int = dictOpt.get("limit")
        
        # dictParameter:dict = {
        #     "where" : strWhere,
        #     "limit" : limit
        # }
        
        # dictDBOutResult = {}

        # sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_select_user_account", dictParameter, dictDBOutResult)

        apiResponseHandler.attachSuccessCode(dictDBOutResult)
        
        return ERR_OK
    
    
    ########################################## private
    
    # #where SQL 조건 문자열을 생성한다.
    # def __generateWhereSQLCondition(self, dictOpt:dict) -> str:
        
    #     '''
    #     문자열의 조합을 만든다.
    #     우선 개발, 지저분한 구문이 되는 문제가 잇어 향후 리펙토링
    #     공통화 개발 필요.
    #     '''
        
    #     #TODO: 2개 이상이면 and 절도 고려해야 한다. customize 성격이 강하다.
    #     lstCondition:list = []
        
    #     self.__convertConditionToList(dictOpt, lstCondition)
        
    #     strWhere:str = self.__convertListToSQLString(lstCondition)
        
    #     #return 구문, 하나로
    #     return strWhere
    
    # def __convertListToSQLString(self, lstCondition:list) -> str:
        
    #     '''
    #     '''
        
    #     strWhere:str = ""
    #     nConditionCount = len(lstCondition)
        
    #     if 0 == nConditionCount: #불필요하지만, 가독성, 향후를 위해서 분가 구문 선언
            
    #         # return ""
    #         pass
        
    #     elif 1 == nConditionCount:
            
    #         # return f"where {nConditionCount}"
    #         strWhere = f"where {lstCondition[0]}"
        
    #     else : #모든 condition을 and 절로 묶어서 치환
            
    #         #한개를 먼저 꺼낸다.
    #         strFistCondition = lstCondition.pop(0)
            
    #         strWhere = f"where {strFistCondition}"
            
    #         #이후부터는 and 추가
    #         for strCondition in lstCondition:
                
    #             strWhere += f" and {strCondition}"
                
    #     return strWhere
    
    # #각 조건별로 list로 변환한다.
    # def __convertConditionToList(self, dictOpt:dict, lstCondition:list):
        
    #     '''
    #     '''
        
    #     #1차, user_id만 제공한다. 여기는 종속성 허용        
    #     user_id = dictOpt.get("user_id")
    #     login_status = dictOpt.get("login_status")
    #     user_flag = dictOpt.get("user_flag")
        
    #     LOG().debug(f"convert condition, user_id = {user_id}, login_status = {login_status}, user_flag = {user_flag}")
        
    #     #TODO: 이건 나중에 고민하자.
    #     #TODO: default value에 대한 정의 필요.
        
        
    #     strUserIDQuery = self.__convertConditionToSQLEqualQuery("USER_ID", user_id, "", True)
        
    #     if 0 < len(strUserIDQuery):
    #         lstCondition.append(strUserIDQuery)
        
    #     strLoginStatusQuery = self.__convertConditionToSQLEqualQuery("LOGIN_STATUS", login_status, -1, False)
        
    #     if 0 < len(strLoginStatusQuery):
    #         lstCondition.append(strLoginStatusQuery)
        
    #     strUserFlagQuery = self.__convertConditionToSQLEqualQuery("USE_FLAG", user_flag, -1, False)
        
    #     if 0 < len(strUserFlagQuery):
    #         lstCondition.append(strUserFlagQuery)
        
    #     return ERR_OK
    
    # #입력한 조건식에 대한 Equal (=) 쿼리로 변경
    # def __convertConditionToSQLEqualQuery(self, strSQLField:str, condition:Any, defaultValue:Any, bStrType:bool):
        
    #     '''
    #     필드명 = 값 형태의 조건으로 변경
    #     문자형이면 '' 추가, 아니면 그냥 전달
    #     '''
        
    #     if None == condition or defaultValue == condition:
    #         return ""
        
    #     #TODO: 향후 3항 연산자 고민
    #     if True == bStrType:
    #         return f"{strSQLField} = '{condition}'" 
    #     else:
    #         return f"{strSQLField} = {condition}" 
