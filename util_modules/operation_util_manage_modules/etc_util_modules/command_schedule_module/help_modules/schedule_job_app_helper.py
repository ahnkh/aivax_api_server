
from lib_include import *

from common_modules.type_hint import *

'''
schedule 명령, app 실행 helper
'''

class ScheduleJobAppHelper:
    
    def __init__(self):
        pass
    
    # 특수 스케쥴러, 아직 미구현
    
    
    
    # 외부 스케쥴러 실행, 외부 호출, snake notation
    def do_extern_command(self, strExternCommand:str):
        
        '''
        '''
        
        #TODO: 개선 필요 + 모듈화
        if None != strExternCommand and 0 < len(strExternCommand):
            os.system(strExternCommand)
        
        return ERR_OK