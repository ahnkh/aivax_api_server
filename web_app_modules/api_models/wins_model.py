
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from dataclasses import dataclass

from lib_include import *

class GrpcServerItem(BaseModel):
    
    port : Optional[int] = 8000
    pass

class GrpcClientItem(BaseModel):

    host: Optional[str] = "127.0.0.1"
    port : Optional[int] = 8000

    prompt : Optional[str] = ""
    hook : Optional[str] = "on_browser_message"
    pass

#Login
class LoginModelItem(BaseModel):

    user_id : Optional[str]
    user_pw : Optional[str]
    pass


#사용자 계정 - 추가, 수정, 삭제, 조회 (조회는 GET)

class UserAccountBaseConditionItem(BaseModel):
    
    '''
    사용자 계정 조건 옵션
    - user_id : 사용자 ID
    - login_status : 로그인 상태
    - use_flag : 사용 여부
    '''
    
    user_id : Optional[str] = Field(default=None)
    login_status : Optional[int] = Field(default=None)
    use_flag : Optional[int] = Field(default=None)
    pass
    
#계정 추가
class UserAccountInsertItem(BaseModel):
    
    '''    
    '''

    user_id : Optional[str]
    user_passwd : Optional[str]
    email : Optional[str] = Field(default=STRING_NULL_VALUE)
    dept : Optional[str] = Field(default=STRING_NULL_VALUE)
    tel : Optional[str] = Field(default=STRING_NULL_VALUE)
    etc_comment : Optional[str] = Field(default=STRING_NULL_VALUE)
    login_status : Optional[int] = Field(default=0)
    pass
    
class UserAccountEditItem(BaseModel):
    
    class UpdateItem(BaseModel):
        
        user_passwd: Optional[str] = Field(default=None, description="")
        email: Optional[str] = Field(default=None, description="")
        dept: Optional[str] = Field(default=None, description="")
        tel : Optional[str] = Field(default=None)
        etc_comment : Optional[str] = Field(default=None)
        login_status : Optional[int] = Field(default=None)
        
        
    update : Optional[UpdateItem]    
    condition : Optional[UserAccountBaseConditionItem]  
    pass
    
class UserAccountDeleteItem(BaseModel):

    condition : Optional[UserAccountBaseConditionItem]
    pass


class UserAccountListItem(BaseModel):
    
    limit:int = 10
    condition : Optional[UserAccountBaseConditionItem]
    pass

#사용자 그룹 - 추가,수정,삭제,조회
class UserAccountBaseConditionItem(BaseModel):
    
    user_id: Optional[str] = Field(default=None, description="")
    user_id: Optional[str] = Field(default=None, description="")
    pass


#condition, 공통 조건 Item
class UserGroupBaseConditionItem(BaseModel):
    
    group_id : Optional[int] = Field(default=INTEGER_NULL_VALUE, description="")
    group_name : Optional[str] = Field(default=STRING_NULL_VALUE, description="")
    use_flag: Optional[int] = Field(default=INTEGER_NULL_VALUE, description="")
    pass

class UserGroupInsertItem(BaseModel):
    
    '''    
    '''
    
    group_id: Optional[int] = Field(default=INTEGER_NULL_VALUE, description="")
    group_name: Optional[str] = Field(default=STRING_NULL_VALUE, description="")
    etc_comment: Optional[str] = STRING_NULL_VALUE
    use_flag: Optional[int] = 1
    pass

class UserGroupEditItem(BaseModel):
    
    class UpdateItem(BaseModel):
        
        group_name: Optional[str] = Field(default=None, description="")
        use_flag: Optional[int] = Field(default=None, description="")
        etc_comment: Optional[str] = Field(default=None, description="")
        
    update : Optional[UpdateItem]    
    condition : Optional[UserGroupBaseConditionItem]    
    pass

class UserGroupDeleteItem(BaseModel):
    
    condition : Optional[UserGroupBaseConditionItem]
    pass

class UserGroupListItem(BaseModel):
    
    limit:int = 10
    condition : Optional[UserGroupBaseConditionItem]
    pass


# 차단 정보 조회
class PromptBlockLogItem(BaseModel):
    
    limit:int = 10
    
    class PromptBlockBaseConditionItem(BaseModel):
        
        allowed : Optional[int] = Field(default=None)
        reason : Optional[str] = Field(default=None)
        
    condition : Optional[PromptBlockBaseConditionItem]
    
    
    pass

#MCP 차단 로그 조회
class MCPServerBlockLogItem(BaseModel):
    
    limit:int = 10
    
    class MCPServerBlockBaseConditionItem(BaseModel):
    
        tool_name: Optional[str] = Field(default=None)
        reg_type: Optional[int] = Field(default=None)
        allowed : Optional[int] = Field(default=None)
        reason : Optional[str] = Field(default=None)
        
    condition : Optional[MCPServerBlockBaseConditionItem]
    pass
    
#사용자 행위 로그 조회
class UserMonitorLogItem(BaseModel):
    
    limit:int = 10
    
    class UserMonitorBaseConditionItem(BaseModel):
    
        user_id: Optional[str] = Field(default=None)    
        allowed : Optional[int] = Field(default=None)
        reason : Optional[str] = Field(default=None)
        
    condition : Optional[UserMonitorBaseConditionItem]
    pass


############################################ pipeline 관련

# 차단정보
class FileAttachItem(BaseModel):
    
    id : Optional[str] = Field(default="", description="file id")
    size : Optional[int] = Field(default=0, description="file size")
    name : Optional[str] = Field(default="", description="file name")
    mime_type : Optional[str] = Field(default="", description="mime type")
    # pass

#엔진등, 다중 차단을 위한 API 데이터
class VariantFilterForm(BaseModel):
    
    '''
    filter_list : 차단 필터 리스트
    
    - llm_filter : AI 필터
    - inlet_raw_logger : 테스트용, 미사용
    - secret_filter : API 차단 필터
    - regex_filter : 정규표현식 기반 필터
    - file_block_filter : 파일 분석 필터
    - input_filter : opensearch 저장 (프롬프트)
    - output_filter : opensearch 저장 (LLM 응답)    
    
    prompt : 프롬프트 문자열 (예: 프롬프트를 입력해주세요)
    
    - prompt, prompt_base64 둘다 사용시, prompt를 우선하여 사용
    
        body": {
        "messages": [
        {"role": "user", "content": "안녕하세요"}
        ]
    },
    "user": {
        "id": "u1234",
        "name": "홍길동"
    }
    }'
    '''
    
    server_ip:str = Field(default="127.0.0.1", description="pipeline server ip")
    port:str = Field(default="9099", description="pipeline server port")
    openapi:str = Field(default="", description="pipeline server api root")
        
    filter_list: Optional[List[str]] = ["input_filter", "secret_filter", "slm_filter", "file_block_filter"] 
        
    prompt: str = Field(default="", description="입력 프롬프트")
    
    user_id : Optional[str] = Field(default="", description="사용자ID")
    email : Optional[str] = Field(default="", description="email")
    ai_service : Optional[int] = Field(default=0, description="ai 서비스 타입 (GPT=0, CLAUDE=1, GEMINI=2,)")
    client_host : Optional[str] = Field(default="", description="사용자 host, ip")
    session_id : Optional[str] = Field(default="", description="session id")
    
    attachments: Optional[List[FileAttachItem]] = Field(default_factory=list, description="첨부 파일 리스트")
        
    message_id:str = Field(default="", description="message id, 요청 및 응답간의 연결 키")
    
    debug: Optional[bool] = Field(default=False, description="debug mode")
    # pass
    
#filter 룰 테스트 기능
class FilterRuleTestItem(BaseModel):
    
    server_ip:str = Field(default="127.0.0.1", description="pipeline server ip")
    port:str = Field(default="9099", description="pipeline server port")
    openapi:str = Field(default="", description="pipeline server api root")
    
    prompt: str = Field(default="", description="입력 프롬프트")
    
    rule:str = Field(default="", description="정책 Rule")
    action:str = Field(default="", description="action (block/masking)")    
    # pass
    
# 정책 signal 갱신 요청
class FilterPolicySignalItem(BaseModel):
    
    '''
    '''
    
    server_ip:str = Field(default="127.0.0.1", description="pipeline server ip")
    port:str = Field(default="9099", description="pipeline server port")
    openapi:str = Field(default="", description="pipeline server api root")
    
    date : datetime.datetime = Field(default_factory=datetime.datetime.now)    
    pass
    