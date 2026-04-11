
from lib_include import *

from common_modules.type_hint import *

from util_modules.wins_manage_modules.local_etc_common.local_etc_define import * #WinsModuleDefine

'''
'''

class PipelineDataAggregateHelper:
    
    def __init__(self):
        pass
    
    # 개별 filter별 차단 결과값의 수집
    def GenerateEachFilterDetectResult(self, lstAllFilterDetectList:list, dictEachFilterResult:dict):
        
        '''
        각 filter별 mode 값을 꺼낸다.
        filter, mode값의 쌍으로 반환하면 된다.
        '''
        
        for dictFilterDetect in lstAllFilterDetectList:
            
            mode:str = dictFilterDetect.get("mode")
            filter:str = dictFilterDetect.get("filter")
            
            dictEachFilterResult[filter] = mode
            # pass
        
        return ERR_OK
    
    # 탐지결과와 기존 정책을 받아서 행열의 행으로 만든다.
    def GenerateRegexDetectResultMatrix(self, lstAllFilterDetectList:list, lstRegexPolicyPattern:list, listDetectMatrixRow:list):
        
        '''
        탐지된 패턴, id, name, category 등이 제공된다. 해당값을 토대로 regex 패턴과 비교하여, 행,열을 만든다.
        '''
        
        #일단 regex만 고민
        # for dictFilterDetect in lstAllFilterDetectList:
        
        dictRegexFilterDetect:dict = {}
        
        self.__gatherRegexDetectList(lstAllFilterDetectList, dictRegexFilterDetect)
        
        #TODO: 향후 필터별 공통화 로직 개발 필요
        #TODO: filter가 없어도, 포맷을 만드는 방식도 필요
        # if None == dictRegexFilterDetect:
        #     LOG().error(f"test error - no regex filter detect")
        
        evidence:list = dictRegexFilterDetect.get("evidence", [])
        
        #id만 필요하다.
        #일단 성능은 무시, 재활용성만 생각.
        # id:str = evidence.get("id")
            
        #정책 카운트 만큼 행을 만든다. python에 배열이 있는지 확인
        # lstDetectMatrix = []
        
        for dictPolicyPattern in lstRegexPolicyPattern:
            
            #정책 개수만큼 matrix 리스트에 행 추가
            #탐지 결과에 존재하면 O, 없으면 X로 추가 (향후 상수 필요)
            #상수는 config로 관리해보자. 향후.
            
            strPolicyID:str = dictPolicyPattern.get("id")
            
            #정책, 포함 여부 탐지 > 함수 분리, 성능은 미 고려
            bMatchDetectResult:bool = self.__checkMatchDetectResult(strPolicyID, evidence)
            
            # 탐지 되었으면 O, 아니면 X => 테스트 자동화 개념, 상수화는 나중에 고민.
            if True == bMatchDetectResult:
                
                listDetectMatrixRow.append("O")
            else:
                listDetectMatrixRow.append("X")
                
        # 결과 업데이트
        # listDetectMatrixRow[:] = lstDetectMatrix
        
        return ERR_OK
    
    # 탐지된 정책, 이름에 대한 행을 생성한다.
    def GenerateDetectedPolicyNameRow(self, lstAllFilterDetectList:list, listDetectPolicyNameRow:list):
        
        '''
        '''
        
        dictRegexFilterDetect = {}
        self.__gatherRegexDetectList(lstAllFilterDetectList, dictRegexFilterDetect)
        
        # #TODO: 향후 필터별 공통화 로직 개발 필요
        # if None == dictRegexFilterDetect:
        #     LOG().error(f"test error - no regex filter detect")
        #     return ERR_OK
        
        evidence:list = dictRegexFilterDetect.get("evidence", [])
        
        nIndex:int = 0
        
        for dictEvidence in evidence:
            
            name:str = dictEvidence.get("name")
            
            listDetectPolicyNameRow[nIndex] = name
            nIndex += 1
            # pass
        
        return ERR_OK
    
    
    ################################################ private
    
    #regex 정책을 찾는다. custom
    def __gatherRegexDetectList(self, lstAllFilterDetectList:list, dictRegexFilterDetect:dict) -> dict:
        
        '''
        list에서 filter 값이 regex인 결과물을 추출한다.
        '''
        
        for dictFilterDetect in lstAllFilterDetectList:
            
            filter:str = dictFilterDetect.get("filter")
            
            if "regex" == filter:
                
                # return dictFilterDetect
                dictRegexFilterDetect.update(dictFilterDetect)
        
        # return None
        return ERR_OK
    
    # 정책의 탐지 여부, 별도의 함수로 분리한다.
    def __checkMatchDetectResult(self, strPolicyID:str, lstDetectEvidence:list):
        
        '''
        TODO: 성능은 무시
        '''
        
        #filter_detect 안에 evicence
        '''
        {
            "filter": "regex",
            "mode": "block",
            "policy_id": "cadb6a56-a97c-4a2f-851b-a03b6659bfc2",
            "policy_name": "신 우편번호",
            "target": "etc",
            "category": "연락·위치:물리적/지리적 위치",
            "masked_contents": "내 API key는 [AIVAX MASKING] 인데 이걸로 어떻게 OpenAI 로 KEY를 전달하는지 예제를 알려주세요",
            "evidence": [
                {
                    "id": "cadb6a56-a97c-4a2f-851b-a03b6659bfc2",
                    "name": "신 우편번호",
                    "action": "block",
                    "targets": "etc",
                    "category": "연락·위치:물리적/지리적 위치",
                    "match": "12345 (22,27)"
                },
                {
                    "id": "9e972718-b4f5-4411-bce8-8e698f803c94",
                    "name": "구 우편번호",
                    "action": "block",
                    "targets": "etc",
                    "category": "연락·위치:물리적/지리적 위치",
                    "match": "567-000 (26,33)"
                }
            ]
        }
        '''
        
        for dictEvidence in lstDetectEvidence:
            
            id:str = dictEvidence.get("id")
            
            if id == strPolicyID:
                return True
        
        return False
