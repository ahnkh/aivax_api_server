
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

from util_modules.wins_manage_modules.ext_api_modules.command_etc_custom_sql.help_modules.wins_sql_parameter_customize_helper import WinsSQLParameterCustomizeHelper

'''
custom sql 명령 - 기타 공통 명령
'''

class EtcDetailSQLCommand:
    
    def __init__(self):
        self.__customDBHelper = WinsSQLDBHelper()
        
        self.__sqlParameterCustomizeHelper = WinsSQLParameterCustomizeHelper()
        pass
    
    
    def RunCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        
        detail_sub_cmd:str = dictOpt.get(KShellParameterDefine.DETAIL_SUB_CMD)
        
        if WinsCommandDefine.DETAIL_SUB_CMD_ADD_DATA == detail_sub_cmd:
            self.__runAddSQLDataCommand(dictOpt, dictWinsApiModuleLocalConfig, apiResponseHandler)
            pass
        
        elif WinsCommandDefine.DETAIL_SUB_CMD_EDIT_DATA == detail_sub_cmd:
            self.__runEditSQLDataCommand(dictOpt, dictWinsApiModuleLocalConfig, apiResponseHandler)
            pass
        
        elif WinsCommandDefine.DETAIL_SUB_CMD_DELETE_DATA == detail_sub_cmd:
            self.__runDeleteSQLDataCommand(dictOpt, dictWinsApiModuleLocalConfig, apiResponseHandler)
            pass
        
        elif WinsCommandDefine.DETAIL_SUB_CMD_LIST_DATA == detail_sub_cmd:
            self.__runListSQLDataCommand(dictOpt, dictWinsApiModuleLocalConfig, apiResponseHandler)
            pass
        
        else:
            GlobalCommonModule.RaiseHttpException(WinsErrorDefine.API_ROUTER_COMMAND_ERROR, WinsErrorDefine.API_ROUTER_COMMAND_ERROR_MSG, f"unknown user account detail sub command {detail_sub_cmd}")
            return ERR_FAIL
        
        
        return ERR_OK
    
    ################################################# private
    
    #기본 데이터 저장, 변환 parameter를 호출하여 customize
    def __runAddSQLDataCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        입력 parameter, convert로 가공
        sqlprint 실행
        '''
        
        sqlmap_id:str = dictOpt.get(KShellParameterDefine.ID)
        
        customize_convertor:str = dictOpt.get(KShellParameterDefine.CUSTOMIZE_CONVERTOR)
        
        parameter:dict = dictOpt.get(KShellParameterDefine.PARAMETER)
        
        self.__sqlParameterCustomizeHelper.ConvertParameter(customize_convertor, parameter)
        
        #TODO: parameter 정의 한번 재 검토 필요
        dictDBOutResult = {}
        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, sqlmap_id, parameter, dictDBOutResult)
        
        apiResponseHandler.attachSuccessCode(dictDBOutResult)
        
        return ERR_OK
    
    #기본 데이터 수정
    def __runEditSQLDataCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        
        sqlmap_id:str = dictOpt.get(KShellParameterDefine.ID)
        
        dictUpdateItem:dict = dictOpt.get(KShellParameterDefine.UPDATE)
        dictCondition:dict = dictOpt.get(KShellParameterDefine.CONDITION)
        
        #where절을 만들어서, update와 합쳐서 전달한다.
        #deepcopy 대신 가독성, 새로운 필드로 생성
        queryHelper:QueryHelperX = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_QUERY_HELPER)
        
        #update set 쿼리 생성
        strUpdateSet = queryHelper.GenerateUpdateSetQuery(dictUpdateItem)
        
        #where절 생성
        strWhere = queryHelper.GenerateBaseConditionWhereQuery(dictCondition)
        
        dictParameter:dict = {
            WinsCommandDefine.SET : strUpdateSet,
            WinsCommandDefine.WHERE : strWhere
        }
        
        dictDBOutResult = {}
        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, sqlmap_id, dictParameter, dictDBOutResult)
        
        apiResponseHandler.attachSuccessCode(dictDBOutResult)
        
        return ERR_OK
    
    #기본 데이터 삭제
    def __runDeleteSQLDataCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        '''
        
        sqlmap_id:str = dictOpt.get(KShellParameterDefine.ID)
        
        dictCondition:dict = dictOpt.get(KShellParameterDefine.CONDITION)
        
        queryHelper:QueryHelperX = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_QUERY_HELPER)
        
        #where절 생성
        strWhere = queryHelper.GenerateBaseConditionWhereQuery(dictCondition)
        
        dictParameter:dict = {            
            WinsCommandDefine.WHERE : strWhere
        }
        
        dictDBOutResult = {}
        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, sqlmap_id, dictParameter, dictDBOutResult)
        
        apiResponseHandler.attachSuccessCode(dictDBOutResult)
        
        return ERR_OK
    
    #기본 데이터 조회 명령
    def __runListSQLDataCommand(self, dictOpt:dict, dictWinsApiModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        TODO: 우선 하나로 관리, 필요시 모듈 분리
        '''
        
        sqlmap_id:str = dictOpt.get(KShellParameterDefine.ID)
        
        dictCondition:dict = dictOpt.get(KShellParameterDefine.CONDITION)
        
        limit:int = dictOpt.get(KShellParameterDefine.LIMIT)
        
        dictDBOutResult = {}
        self.__customDBHelper.RunSQLCustomSelectQuery(sqlmap_id, dictCondition, limit, dictDBOutResult)
        
        apiResponseHandler.attachSuccessCode(dictDBOutResult)