

import csv
import copy
import base64

from lib_include import *

from common_modules.type_hint import *

'''
pipeline - 탐지 테스트 출력 관리
'''

class PipelineTestOutWriter:
    
    def __init__(self):
        pass
    
    # 정책 데이터 출력, 이것 중요
    def WritePipelineRegexFilterPolicy(self, strOutputPath:str, lstRegexPolicyPattern:list):
        
        '''
        패턴, 서식화된 리스트, 우선 열을 만들고, 헤더를 고민해보자.
        '''
        
        dictHeader:dict = lstRegexPolicyPattern[0]
        
        #TODO: 데이터 보정, base64 인코딩.
        lstRegexPolicyPatternCopy:list = copy.deepcopy(lstRegexPolicyPattern)
        
        #우선 하나의 함수에서 개발, 나중에 리펙토링
        for dictRegexPattern in lstRegexPolicyPatternCopy:
            
            rule:str = dictRegexPattern.get("rule")
            
            #base64 decoding
            
            byteBase64Decode = base64.b64decode(rule)
          
            #문자열로 변환
            strBase64Decode = byteBase64Decode.decode("utf-8")
            
            dictRegexPattern["rule"] = strBase64Decode
            # pass
        
        fieldnames = dictHeader.keys()
        
        #원본 그대로 저장, python 모듈 활용
        with open(strOutputPath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            
            writer.writeheader()   # 첫 행 (컬럼명)
            writer.writerows(lstRegexPolicyPatternCopy) # 데이터 행
            # pass
        
        return ERR_OK
    
    def WriteDetectTestOutput(self, strDetectResultOutputPath:str, lstDetectSummary:list):
        
        '''
        테스트 출력결과, 파일로 저장한다.
        기본 CSV 포맷을 저장하고, 수집된 정책 데이터도 저장한다.
        개별로, 일괄 호출 방식으로 API 제공
        TODO: 두가지 방식, 탐지된 이름을 나열 (csv는 10칸 정도 버퍼)
        전체 CSV, 매트릭스로 표기
        '''
        
        # 거의 유사, 리펙토링, 모듈화는 나중에
        
        #필드명, custom TODO: 눈에 안들어온다. 실제 정책명을 보이는게 낫다.
        lstFieldName:list = ["NO", "프롬프트", "탐지결과", "탐지일자", "탐지된정책"]
        
        # 그냥 다시 만들자. 큰 의미 없다.
        # lstDetectSummaryCopy:list = copy.deepcopy(lstDetectSummary)
        '''
        lstDetectSummary.append({
                "no" : nIndex,
                "prompt" : strPrompt,
                "mode" : strMode,
                "date" : strDate,
                "detect_policy_name_row" : listDetectPolicyNameRow,
                "detect_matrix_row" : listDetectMatrixRow, #regex 정책과 비교, 행열의 한 행으로 생성
                
                # "evidence" : evidence #향후 사용을 위해서 원본 저장
            }
        '''
        lstDetectSummaryRow:list = []
        
        #탐지 결과, csv 형태로 보정한다.
        for dictDetectSummary in lstDetectSummary:
            
            lstDetectSummaryRow.append({
                "NO" : dictDetectSummary.get("no"),
                "프롬프트" : dictDetectSummary.get("prompt"),
                "탐지결과" : dictDetectSummary.get("mode"),
                "탐지일자" : dictDetectSummary.get("date"),
                "탐지된정책" : dictDetectSummary.get("detect_policy_name_row"),
            })
        
        
        #원본 그대로 저장, python 모듈 활용
        with open(strDetectResultOutputPath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=lstFieldName, quoting=csv.QUOTE_ALL)
            
            writer.writeheader()   # 첫 행 (컬럼명)
            writer.writerows(lstDetectSummaryRow) # 데이터 행
            # pass
        
        return ERR_OK

