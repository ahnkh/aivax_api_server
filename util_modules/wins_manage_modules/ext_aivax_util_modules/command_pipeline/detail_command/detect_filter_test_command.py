import copy

from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import * #WinsModuleDefine

from util_modules.wins_manage_modules.ext_aivax_util_modules.command_pipeline.help_modules.pipeline_filter_policy_helper import PipelineFilterPolicyHelper
from util_modules.wins_manage_modules.ext_aivax_util_modules.command_pipeline.help_modules.pipeline_http_api_helper import PipelineHttpApiHelper
from util_modules.wins_manage_modules.ext_aivax_util_modules.command_pipeline.help_modules.pipeline_data_aggregate_helper import PipelineDataAggregateHelper
from util_modules.wins_manage_modules.ext_aivax_util_modules.command_pipeline.help_modules.pipeline_testout_writer import PipelineTestOutWriter

'''
pipeline filter 테스트
'''

class DetectFilterTestCommand:
    
    def __init__(self):
        pass
    
    
    # pipline Filter 탐지 테스트
    def testDetectFilter(self, dictOpt:dict, dictPipelineFilterCommandLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        탐지 정책, DB에서 조회한다.
        프롬프트 -> 외부 또는 dictOpt로 수집한다.
        pipeline filter API를 호출한다.
        호출 결과를 파싱한다. (임시 저장, 메모리)
        프롬프트, 탐지정책, filter 결과의 조합으로 결과를 생성한다.
        결과를 메일 알람으로 발송한다.
        
        TODO: 테스트 성격, customize가 일부 추가된다. regex, file, slm은 별도로 테스트한다.
        '''
        
        LOG().info(f"test detect filter")
        
        #로그 수집단계, 정책 데이터를 조회한다.
        #프롬프트, email등 필요 정보를 수집
        prompt_test_list:list = dictOpt.get(WinsModuleDefine.AIVAX_COMMAND_DEFINE.PROMPT_TEST_LIST)
        test_email:str = dictOpt.get(WinsModuleDefine.AIVAX_COMMAND_DEFINE.TEST_EMAIL)
        
        # filter 테스트, 각각 분리한다. 일부 customize가 포함된다.
        # 테스트키는, 실제 pipeline의 api 키를 사용한다. => pipeline_filter, api, 그대로 전달. customize 최소화
        pipeline_filter_list:list = dictOpt.get(WinsModuleDefine.AIVAX_COMMAND_DEFINE.PIPELINE_FILTER_LIST)
        
        #패턴 정책 조회, 현재는 regex만 존재한다.
        # TODO: 테스트코드, 성능은 고려하지 않는다. => 확장을 위해서 가림처리는 필요
        lstRegexPolicyPattern:list = []
        self.__getRegexFilterPolicy(lstRegexPolicyPattern)
        
        # pipeline으로 API 요청
        # 모든 프롬프트에 대해서 요청해야 한다.
        # 프롬프트를 키로, API 결과를 모은다.
        dictPromptDetectResult = {}
        self.__filterPromptList(prompt_test_list, test_email, pipeline_filter_list, dictPipelineFilterCommandLocalConfig, dictPromptDetectResult)
        
        #prompt 별 filter 결과의 가공, 집계 - 1차 집계
        #결과데이터는 dictionary 형태로 저장
        #TODO: 타입별로 상이하다. customize 필요
        lstDetectSummary:list = []
        self.__aggregatePipelineFilterResult(dictPromptDetectResult, pipeline_filter_list, lstDetectSummary, lstRegexPolicyPattern)
        
        #결과 데이터 출력, 패턴별 카운트        
        testOutoutWriter:PipelineTestOutWriter = PipelineTestOutWriter()
        
        self.__writeTestOutput(testOutoutWriter, dictPipelineFilterCommandLocalConfig, lstRegexPolicyPattern, lstDetectSummary)
        
        return ERR_OK
    
    ################################### private
    
    # pipeline 정책, 수집한다.
    def __getRegexFilterPolicy(self, lstRegexPolicyPattern:list):
        
        '''
        '''
        
        filterPolicyHelper:PipelineFilterPolicyHelper = PipelineFilterPolicyHelper()
        filterPolicyHelper.GetRegexFilterPolicy(lstRegexPolicyPattern)
        
        return ERR_OK
    
    # prompt 별 filter api 요청, 프롬프트별 응답 결과 수집 (응답데이터는 ApiHelper에 정규화)
    def __filterPromptList(self, lstTestPrompt:list, strTestEmail:str, lstPipelineFilterList:list, dictPipelineFilterCommandLocalConfig:dict, dictPromptDetectResult:dict):
        
        '''
        프롬프트별로 pipeline에 응답을 요청한다. 응답 데이터는 ApiHelpe에서 필요데이터를 정리한다.
        TODO: 성능 무시, 원시 데이터 대신 Model구조체도 고려
        '''
        
        pipeline_api_request:dict = dictPipelineFilterCommandLocalConfig.get("pipeline_api_request")
        
        # pipeline 서버 url, 이건 config로 제어한다.
        url_option:dict = pipeline_api_request.get("url_option")
        
        # port 요청, 기본 port 값, 여기서 email만 변경한다.
        post_default_parameter:dict = pipeline_api_request.get("post_default_parameter")
        
        for strPrompt in lstTestPrompt:
            
            #프롬프트 요청마다 post 데이터는 복사한다.
            dictPostData:dict = copy.deepcopy(post_default_parameter)
            
            dictPostData["email"] = strTestEmail
        
            dictPostData["filter_list"] = lstPipelineFilterList        
            dictPostData["prompt"] = strPrompt
            
            dictOuputResponse:dict = {}
            
            self.__requestToFilterApi(url_option, dictPostData, dictOuputResponse)
            
            dictPromptDetectResult[strPrompt] = dictOuputResponse
        
        return ERR_OK
    
    
    # pipeline, api 요청, 프롬프트별로 loop을 돌때, 개별 필터로 사용한다.
    def __requestToFilterApi(self, dictUrlOption:dict, dictPostJson:dict, dictOuputResponse:dict):
        
        '''
        '''
        
        pipelineHttpApiHelper:PipelineHttpApiHelper = PipelineHttpApiHelper()
        pipelineHttpApiHelper.RequestFilterApi(dictUrlOption, dictPostJson, dictOuputResponse)
        
        return ERR_OK
    
    # pipeline, 탐지 결과의 가공
    def __aggregatePipelineFilterResult(self, dictPromptDetectResult:dict, lstPipelineFilter:list, lstDetectSummary:list, lstRegexPolicyPattern:list):
        
        '''
        prompt별 loop
        응답 결과에서의 유효 데이터 추출, regex, file, slm 별로 상이하게 처리
        결과 데이터 반환
        TODO: lstPipelineFilter는 재정립 필요, filter별 분기, 우선 regex만 고려
        '''
        
        #각 라인별로 No 추가
        nIndex:int = 0
        
        aggregateHelper:PipelineDataAggregateHelper = PipelineDataAggregateHelper()
        
        for strPrompt in dictPromptDetectResult.keys():
            
            dictEachDetectResult:dict = dictPromptDetectResult.get(strPrompt)
            
            #log_event 내 filter_detect에 탐지 결과가 저장되어 있다.
            
            if None == dictEachDetectResult:
                LOG().error(f"test error - no api output, prompt = {strPrompt}")
                continue
            
            #pipeline의 최종 탐지 결과
            # strMode:str = "undetect" #탐지 결과
            strMode:str = dictEachDetectResult.get("mode") #TODO: regex, file, slm등 filter별로 분리되면, mode값이 달라질수는 있다.
            strDate:str = dictEachDetectResult.get("completed_date")
            
            log_evidence:dict = dictEachDetectResult.get("log_evidence", {})
            
            #실제 다중 탐지 결과
            #여기서 부터는 aggregateHelper로 전달, customize가 필요할수 있다. 탐지가 안되면 log_evidence는 없다.
            filter_detect:list = log_evidence.get("filter_detect", [])
            
            #evidence
            # evidence:list = filter_detect.get("evidence")
            
            #TODO: 이 타입말고, 다른 타입으로 저장도 필요
            listDetectMatrixRow:list = []
            aggregateHelper.GenerateDetectResultMatrix(filter_detect, lstRegexPolicyPattern, listDetectMatrixRow)
            
            #탐지된 패턴에 대한 이름, 기본 5개
            listDetectPolicyNameRow:list = ["","","","",""]
            aggregateHelper.GenerateDetectedPolicyNameRow(filter_detect, listDetectPolicyNameRow)
            
            nIndex += 1 #집계 번호
            
            #TODO: filter 별 분리, 우선 Regex 패턴
            #일단 regex 패턴만 생각
            
            #등록된 정책과 탐지된 결과를 비교, matrix 형태의 행을 만든다.
            #데이터 가공관리 helper 추가
            
            #TODO: 상수 필요, 최종 포맷은 한글로 고려
            lstDetectSummary.append({
                "no" : nIndex,
                "prompt" : strPrompt,
                "mode" : strMode,
                "date" : strDate,
                "detect_policy_name_row" : listDetectPolicyNameRow,
                "detect_matrix_row" : listDetectMatrixRow, #regex 정책과 비교, 행열의 한 행으로 생성
                
                # "evidence" : evidence #향후 사용을 위해서 원본 저장
            })
        
        return ERR_OK
    
    #테스트 결과 저장
    def __writeTestOutput(self, testOutoutWriter:PipelineTestOutWriter, dictPipelineFilterCommandLocalConfig:dict, lstRegexPolicyPattern:list, lstDetectSummary:list):
        
        '''
        '''
        
        #저장관련 설정, config 수집
        test_output_writer:dict = dictPipelineFilterCommandLocalConfig.get("test_output_writer")
        
        regex_policy_writer:dict = test_output_writer.get("regex_policy_writer")
        
        policy_output_path:str = regex_policy_writer.get("policy_output_path")
        
        filter_detect_writer:dict = test_output_writer.get("filter_detect_writer")
        
        detect_result_output_path:str = filter_detect_writer.get("detect_result_output_path")
        
        # 정책 저장        
        testOutoutWriter.WritePipelineRegexFilterPolicy(policy_output_path, lstRegexPolicyPattern)
        
        # 프롬프트 탐지 결과, 정책 출력
        # 우선 가독성, CSV로 , 이건 AI의 도움을 받는다. 잠시 보류
        testOutoutWriter.WriteDetectTestOutput(detect_result_output_path, lstDetectSummary)
        
        return ERR_OK