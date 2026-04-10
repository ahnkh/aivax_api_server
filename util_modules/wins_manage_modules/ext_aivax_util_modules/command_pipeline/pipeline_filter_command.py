
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import *
from util_modules.wins_manage_modules.local_etc_common.local_etc_define import WinsModuleDefine

'''
aivax pipeline 관련 util
'''

class PipelineFilterCommand:
    
    def __init__(self):
        pass
    
    def RunCommand(self, dictOpt:dict, dictAivaxUtilModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        pipeline util의 제공
        최초 - filter 탐지 테스트
        '''
        
        # Test
        LOG().info("run pipline filter command")
        
        detail_cmd = dictOpt.get(KShellParameterDefine.DETAIL_CMD)
        
        #pipeline 탐지 테스트
        if WinsModuleDefine.AIVAX_COMMAND_DEFINE.DETAIL_CMD_FILTER_DETECT_TEST == detail_cmd:
            
            pipeline_filter_command:dict = dictAivaxUtilModuleLocalConfig.get("pipeline_filter_command")
            
            from util_modules.wins_manage_modules.ext_aivax_util_modules.command_pipeline.detail_command.detect_filter_test_command import DetectFilterTestCommand
            detailCommand:DetectFilterTestCommand = DetectFilterTestCommand()
            detailCommand.testDetectFilter(dictOpt, pipeline_filter_command, apiResponseHandler)
            # pass
        
        return ERR_OK