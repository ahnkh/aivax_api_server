
import schedule

from lib_include import *

from common_modules.type_hint import *

from util_modules.operation_util_manage_modules.etc_util_modules.command_schedule_module.help_modules.schedule_job_app_helper import ScheduleJobAppHelper

'''
scheduler daemon 구현
우선 schedule 기능에만 집중, 기존 로직 그대로 구현
'''

class ScheduleDaemonCommand:
    
    def __init__(self):
                
        self.__scheduleUtil:ScheduleUtilHelper = None
        
        self.__scheduleJobAppHelper:ScheduleJobAppHelper = None
        pass
    
   
    
    #schedule daemone command 실행.
    def RunDaemon(self, dictOpt:dict, dictScheduleDaemonLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):

        '''
        등록방식, command에서는 별도 config 경로로 읽는다.
        
        '''

        LOG().info("run schedule daemon command")
        
        self.__scheduleUtil:ScheduleUtilHelper = ScheduleUtilHelper()
        self.__scheduleJobAppHelper:ScheduleJobAppHelper = ScheduleJobAppHelper()

        apiResponseHandler.attachApiCommandCode("schedule daemon command")
        
        # scheudler 실행, 외부 path를 기본으로 수행한다. 향후 확장
        strScheduleConfigPath:str = dictOpt.get(KShellParameterDefine.UTIL_MODULE.SCHEDULE_CONFIG)
        
        # schedule에 등록한다. (1차 버전, 향후 추가 개발, 옵션 분기)
        # lstScheduleConfig:list = []
        scheduleUtil:ScheduleUtilHelper = self.__scheduleUtil
        scheduleJobAppHelper:ScheduleJobAppHelper = self.__scheduleJobAppHelper
        self.__loadFromScheduleConfig(scheduleUtil, scheduleJobAppHelper, strScheduleConfigPath)
        
        # apiResponseHandler.attachSuccessCode(dictDBResult)
        
        # python의 기본 스케쥴러, 더 개선할수 있지만, 우선 유지한다. 
        # sleep만 3초로, 분 이상의 스케쥴러만 사용한다.
        while True:
            schedule.run_pending()
            #TODO: Alive Check 필요
            time.sleep(1)

        # return ERR_OK
    
    
    ##################################### private
    
    # schedule config를 읽는다. 역할 분리
    def __loadFromScheduleConfig(self, scheduleUtil:ScheduleUtilHelper, scheduleJobAppHelper:ScheduleJobAppHelper, strScheduleConfigPath:str):
        '''
        schedule config 경로의 파일을 읽어서 dictionary에 추가
        현재 schedule은 list형으로 관리, list형 변수에 각각 담아서 반환
        '''
        
        dictScheduleConfig:dict = dict()
        JsonHelperX.JsonFileToDictionary(strScheduleConfigPath, dictScheduleConfig)
        
        schedule_list:list = dictScheduleConfig.get("schedule_list")
        
        for dictEachSchedule in schedule_list:
            
            #{"use":0, "interval":10, "schedule_unit":"seconds", "method":"", "extern_command":""}
            use:int = dictEachSchedule.get("use")
            interval:int = dictEachSchedule.get("interval")
            schedule_unit:str = dictEachSchedule.get("schedule_unit")
            
            #method 또는 extern_command, callback을 생성한다.
            method:str = dictEachSchedule.get("method")
            parameter:str = dictEachSchedule.get("parameter") #TODO: 가변 처리 필요
            
            scheduleCallBack:callable = None
            
            # 실행 우선순위
            if None != method and 0 < len(method):
                
                scheduleCallBack = getattr(scheduleJobAppHelper, method)
                
            else: #error, 발생시 바로 종료
                GlobalCommonModule.RaiseException(ErrorDefine.UTIL_COMMAND_UNKNOWN_EROR, ErrorDefine.UTIL_COMMAND_UNKNOWN_ERROR_MSG, "no schedule job defined")
                return ERR_FAIL
            
            # def RegisterSchedule(self, nInterval:int, strScheduleUnit:str, scheduleCallBack:callable, *parameter:Any, strAtTimeCustom:str = None):
            scheduleUtil.RegisterSchedule(interval, schedule_unit, scheduleCallBack, parameter)
        
        return ERR_OK
    
