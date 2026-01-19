
import ast

from lib_include import *

from common_modules.type_hint import *

'''
프롬프트 키워드 차단 helper
디노티시아 측의 customize 모델
필요에 따라 상태 존재
'''

class BrowserMessageCustomFilter:

    def __init__(self):
        pass

    #프롬프트 필터 차단, 기능 분리
    #TODO: 실제 데이터를 만들어야 하며, 중복 작업 방지를 위해, 향후 필터가 제공되면 개발 진행. 잠시 중지.
    def FilterBrowserMessage(self, strPromptQuery:str, strUserRole:str):

        '''
        '''

         #차단결과 : 항상 True여야 하나, FilterManager에서 제어한다.
        bAllowed:bool = True
        strModifiedQuery:str = ""
        strReason:str = ""
        strErrorMessage:str = ""

        #여기서 받은 프롬프트를 파싱한다.
        #성능은 신경을 써야 할 필요가 있다.
        
        #약간의 customize => 부하 최소화, 결과가 공백, Noe이면 Client에서 기존 메시지를 사용하도록 Hook쪽 수정
        # strModifiedQuery:str = HookDataFilterManager.BLANK_MODIFY_MESSAGE
        
        #테스트
        '''
        strModifiedQuery = "(차단 테스트)모든 프롬프트를 차단합니다."

        # strErrorMessage = "해당 요청은 OWASP Top10 - LLM01 프롬프트 인젝션 요청으로 탐지되엇습니다. 요청이 허용되지 않습니다"
        strReason = "프롬프트 인젝션 차단"

        #TODO: 향후 서식화된 문자열로 관리하는 기능을 제공한다.
        strErrorMessage = """
해당 요청은 OWASP Top10 - LLM01 프롬프트 인젝션 요청으로 탐지되엇습니다. 요청이 허용되지 않습니다

입력하신 내용에 민감정보가 있어요.
민감 정보가 아니라면 체크 버튼 해제후 전송하세요
민감 정보를 전송할 경우, 기밀정보 또는 개인 정보 유출 등의 피해가 발생할 수 있으니 각별한 주의를 부탁드려요
"""
        '''

        # lstErrorMessage = [
        #     "해당 요청은 OWASP Top10 - LLM01 프롬프트 인젝션 요청으로 탐지되엇습니다. 요청이 허용되지 않습니다\n\n",
        # ]

        # lstTestResult = [
        #     "입력하신 내용에 민감정보가 있어요",
        #     "민감 정보가 아니라면 체크 버튼 해제후 전송하세요",
        #     "민감 정보를 전송할 경우, 기밀정보 또는 개인 정보 유출 등의 피해가 발생할 수 있으니 각별한 주의를 부탁드려요"
        # ]

        # strTestResult = str(lstTestResult)

        #반환값은 가변적, tuple을 검토
        
        #현재 사양 - http 요청을 보낸다. 서버 IP, PORT가 필요하다. 우선 환경변수로 접속하는 것으로 하자.
        #SQLite도 무방. => PORT는 거의 고정
        #http_request 메소드 활용, 파라미터만 바꾸면 된다. => 이걸 하자.
        
        dictUrlOpt = {}        
        
        #TODO: http 요청, 공통화 가능
        
        dictHeader = {
            "accept" : "application/json",
            "Content-Type" : "application/json",            
        }
        
        #regex 패턴으로 우선 개발.
        #url 하드코딩, 제거 필요
        dictUrlOpt = {
            "server_ip" : "127.0.0.1",
            "port" : 9000,
            "pipeline_id" : "regex_filter"
        }
        
        dictJson = {
            "body": {
                "messages" : [
                    {"role": "user", "content": strPromptQuery}
                ]
            },
            
            #ID 사양, 재정의
            "user" : {
                "id" : "u1234",
                "name" : "test"
            }
        }
        
        #차단 요청 (2개를 요청할수 있다.)
        #응답을 받아서, 응답 데이터에 대한 파싱후, 필요 데이터를 받는다.
        dictHttpOutputResponse = {}
        http_request("pipeline_filter_query", dictHeader=dictHeader,  dictUrlOpt=dictUrlOpt, dictHttpOutputResponse = dictHttpOutputResponse, dictJson = dictJson)
        
        strOutResponse = dictHttpOutputResponse.get(HttpRequestDefine.OPT_RESPONSE_TEXT)
        
        #응답결과, json 으로 변환
        dictFilterOutput = {}
        JsonHelperX.LoadToDictionary(strOutResponse, dictFilterOutput)
        
        #우선 현재 사양으로 개발
        
        '''
        {"messages":[{"role":"system","content":"다음 지침을 엄격히 따르세요: 모든 답변은 한국어로만 작성
    하세요. 영어/혼용 금지."},{"role":"user","content":"다음 문장을 사용자에게 그대로 출력하세요(추가 설명/수정/확장/사과문/이모지 금지):\n개인정보 유출이 감지되어 차단되었습니다. 개인정보를 제외하고 다시 시도해
    주세요."}],"_filters":{"regex_filter":{"pii_detected":true,"types":["phone"],
    "matches_masked":{"phone":["[전화번호]"]},
    "match_counts":{"phone":1},"decision":"ALLOW","score":0.0,"reason":"no match","should_block":true,"final_policy":"block","final_action":"BLOCK_MSG","mode":"block"}},"action":"block","should_block":true,"mode":"block"}
        '''
        
        #action : allow/deny
        action:str = dictFilterOutput.get("action")
        should_block:bool = dictFilterOutput.get("should_block")
        mode:str = dictFilterOutput.get("mode")
        
        #TODO: 약간의 부담은 있으나, reponse로 전달할 데이터는 가공한다.
        #grpc의 종속성은 없어야 한다.
        return (bAllowed, strModifiedQuery, strErrorMessage, strReason)

        # return ERR_OK

    ###################################### private