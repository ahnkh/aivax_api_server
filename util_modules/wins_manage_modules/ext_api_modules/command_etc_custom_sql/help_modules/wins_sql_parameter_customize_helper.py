
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *

'''
요청 받은 parameter, 지정된 sql 변환 함수를 실행, 변환한다.
'''

class WinsSQLParameterCustomizeHelper:
    
    def __init__(self):        
        pass
    
    
    def ConvertParameter(self, strCustomizeMethodName:str, dictParameter:dict):
        
        '''
        '''
        
        if None != strCustomizeMethodName and 0 < len(strCustomizeMethodName):
        
            methodFunction = getattr(self, strCustomizeMethodName, None)
            
            if callable(methodFunction):
                LOG().debug(f"customize method {strCustomizeMethodName}")
                methodFunction(dictParameter)
        
        return ERR_OK
    
    ################################################# reflection
    
    
    # 사용자 그룹 추가 item 변환
    def convert_user_group_insert_item(self, dictOpt:dict):
        
        dictOpt["reg_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        #TODO: 유효성 검증이 필요하면, 검증 모듈 호출도 여기서 고려.
        
        return ERR_OK
    
    