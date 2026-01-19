
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
    