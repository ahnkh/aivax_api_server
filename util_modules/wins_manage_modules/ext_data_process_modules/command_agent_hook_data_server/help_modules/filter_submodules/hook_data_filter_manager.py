
import ast

from lib_include import *

from common_modules.type_hint import *


'''
hook에서 수집된 데이터, 필터로직을 반영한다. 
필터후, 문자열 데이터를 가공해서 전달한다.
마스킹등 처리도 포함 가공된 데이터를 전달하며, 가공이 불필요하면 공백으로 전달한다.
원본과 modified로 구분하여 전달, 응답 데이터를 생성하는 개념으로 접근한다.

customize 성격이 강한 기능이며, 각 Hook별로 별도로 필터 메소드를 가져가며
필터 처리 모듈로 요청등 부분적으로 공통화 처리를 수행한다.

가공데이터 결과, 로그와 감사등 저장도 고려가 필요하다.
'''

from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.filter_submodules.browser_message_custom_filter import BrowserMessageCustomFilter

class HookDataFilterManager:

    BLANK_MODIFY_MESSAGE = ""

    def __init__(self):

        self.__browserMessageCustomFilter = BrowserMessageCustomFilter()
        pass


    #브라우저, 프롬프트 결과 Filter
    def FilterBrowserMessage(self, strPromptQuery:str, strUserRole:str) -> tuple:

        '''
        TODO: 기능이 매우 복잡할수 있다. 확장또는 다른 모듈화를 고려.
        사용자 권한에 따른 프롬프트 필터 로직의 분기도 고려.
        '''

        #기능 분리, 이관 (TODO: 서비스 모듈로 이관)
        return self.__browserMessageCustomFilter.FilterBrowserMessage(strPromptQuery, strUserRole)


    #LLM 요청 Filter
    def FilterLLMRequest(self, strMessage:str):

        '''
        '''

        bAllowed:bool = True

        #가공된 LLM 메시지
        strModifiedMessage:str = HookDataFilterManager.BLANK_MODIFY_MESSAGE

        #향후 리펙토링
        lstMessage:list = ast.literal_eval(strMessage)

        # #TODO: 테스트
        # #여기서 Loop를 돌고, 첫번째 라인을 XXXXXX 로 치환해본다.
        # # lstNewMessage:list = []
        # bAllowed = False

        # for dictMessage in lstMessage:

        #     #custom 성격, 디노티시아만 사용, 재활용은 못한다.
        #     # content:str = dictMessage.get("content")

        #     #stack 변수, 이값을 업데이트 해본다. 향후 고민
        #     dictMessage["content"] = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

        # strModifiedMessage = str(lstMessage)

        #다시 string으로 변환해서 반환한다.

        #TODO: 약간의 부담은 있으나, reponse로 전달할 데이터는 가공한다.
        #grpc의 종속성은 없어야 한다.
        return (bAllowed, strModifiedMessage)
    
    #MCP 요청 Filter
    def FilterMCPRequest(self, ):

        '''
        '''

        bAllowed:bool = True
        strModifiedArgument:str = HookDataFilterManager.BLANK_MODIFY_MESSAGE

        return (bAllowed, strModifiedArgument)



    # MCP 요청


    ############################################## private