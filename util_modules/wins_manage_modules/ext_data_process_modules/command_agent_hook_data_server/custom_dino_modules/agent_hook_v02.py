"""
Default Plugin Agent Hook

이 파일은 플러그인 시스템의 기본 hook 파일입니다.
ConfigMap을 통해 이 파일을 오버라이드하여 커스터마이징할 수 있습니다.

커스터마이징 예시:
1. 사용자 역할별 쿼리 필터링
2. 특정 LLM 모델 제한
3. 특정 MCP 서버/도구 호출 차단
4. 응답 후처리 및 로깅 강화
"""

import logging
from typing import Dict, Any, List, Optional
from app.agent_hook import AgentHook

#AgentHook 소스에 맞춰 수정
# import sys
# sys.path.append("/app/plugins/")

# import grpc

# import hook_pb2
# import hook_pb2_grpc

logger = logging.getLogger(__name__)

from wins_security_client import WinsSecurityClient, WinsHookRequestCustomizeHelper

"""
TODO: wins sec server 접속 정보 관리 필요
IP, PORT
"""

LOCAL_CONFIG = {
    # "wins_ip" : "10.0.80.35",
    "wins_ip" : "192.168.122.12",    
    "wins_port" : 50001,
    "agent_id" : 100
}

class CustomAgentHook(AgentHook):
    """커스터마이징 가능한 Agent Hook 구현체"""
    
    def __init__(self):
        self.name = "CustomAgentHook"
        logger.info(f"{self.name} 플러그인 로드됨")
        
        # 커스터마이징 설정
        self.config = {
            # 차단할 LLM 모델 키 (예시)
            "blocked_llm_keys": [],
            
            # 차단할 MCP 서버/도구 조합 (예시)  
            "blocked_tools": [],
            
            # 사용자 역할별 제한 (예시)
            "role_restrictions": {},
            
            # 로깅 레벨 설정
            "detailed_logging": True
        }

        #TODO: client 접속 정보 전달
        self.__winsSecurityClient = WinsSecurityClient()

        #우선 기본값으로 초기화, 향후 서버 설정 정보 업데이트 기능 필요
        self.__winsSecurityClient.Initialize(LOCAL_CONFIG)
        pass
    
    async def on_browser_message(
        self, 
        query: str, 
        session_id: Optional[str], 
        user_role: Optional[str]
    ) -> Dict[str, Any]:
        """Browser → Agent 메시지 처리"""
        
        if self.config["detailed_logging"]:
            logger.info(f"[PLUGIN HOOK] Browser → Agent: session_id={session_id}, user_role={user_role}")
            logger.info(f"[PLUGIN HOOK] Query length: {len(query)}")

        
        # strWinsIP:str = LOCAL_CONFIG.get("wins_ip")
        # nWinsPort:int = LOCAL_CONFIG.get("wins_port")
        # nAgentID:int = LOCAL_CONFIG.get("agent_id")

        # strRPCUrl = f"{strWinsIP}:{nWinsPort}"
        
        # 사용자 역할별 제한 체크 (예시)
        if user_role and user_role in self.config["role_restrictions"]:
            restrictions = self.config["role_restrictions"][user_role]
            if restrictions.get("max_query_length", 0) > 0:
                if len(query) > restrictions["max_query_length"]:
                    logger.warning(f"[PLUGIN HOOK] Query too long for role {user_role}: {len(query)}")
                    return {
                        "allowed": False,
                        "modified_query": query,
                        "metadata": {
                            "error": f"Query too long for role {user_role}",
                            "max_length": restrictions["max_query_length"]
                        }
                    }

        # with grpc.insecure_channel(strRPCUrl) as channel:

        #     stub = hook_pb2_grpc.HookProxyStub(channel)
        #     response = stub.HookBrowserMessage(hook_pb2.BrowserHookRequest(
        #         request_id = "0",
        #         agent_id = nAgentID,
        #         query = query,
        #         session_id = session_id,
        #         user_role = user_role
        #     ), timeout=5)

        #     logger.info(f"[HOOK/BROWSER_REQUEST] grpc response = {response}")

        #     bAllowed = response.allowed

        #     #데이터가 없으면 이전 데이터 전달, 공통화
        #     strModifiedQuery = response.modified_query
        #     if None or 0 == len(strModifiedQuery):
        #         strModifiedQuery = query

            # strModifiedQuery = "당신의 프롬프트를 차단합니다."
            # response.source

        
        request = WinsHookRequestCustomizeHelper.BrowserHookRequest(self.__winsSecurityClient, query, session_id, user_role)

        response = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOOK_BROWSER_MESSAGE, request)

        bAllowed:bool = response.allowed
        strModifiedQuery:str = response.modified_query
        strModifiedQuery = WinsSecurityClient.UtilGetModifiedStringData(strModifiedQuery, query)

        # 기본적으로는 모든 메시지 허용
        return {
            "allowed": bAllowed,
            "modified_query": strModifiedQuery,
            "metadata": {
                "hook_name": self.name,
                "session_id": session_id,
                "user_role": user_role,
                "processed": True
            }
        }
    
    async def on_llm_request(
        self,
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int,
        stream: bool
    ) -> Dict[str, Any]:
        """Agent → LLM 요청 처리"""
        
        if self.config["detailed_logging"]:
            logger.info(f"[PLUGIN HOOK] Agent → LLM: llm_key={llm_key}, iteration={iteration}, stream={stream}")
            logger.info(f"[PLUGIN HOOK] Messages count: {len(messages)}")
        
        # 차단된 LLM 키 체크
        if llm_key and llm_key in self.config["blocked_llm_keys"]:
            logger.warning(f"[PLUGIN HOOK] Blocked LLM key: {llm_key}")
            return {
                "allowed": False,
                "modified_messages": messages,
                "metadata": {
                    "error": f"LLM key {llm_key} is blocked",
                    "hook_name": self.name
                }
            }
        
        # 반복 횟수 제한 (예시)
        if iteration > 50:  # 무한 루프 방지
            logger.warning(f"[PLUGIN HOOK] Too many iterations: {iteration}")
            return {
                "allowed": False,
                "modified_messages": messages,
                "metadata": {
                    "error": f"Too many iterations: {iteration}",
                    "hook_name": self.name
                }
            }

        # strWinsIP:str = LOCAL_CONFIG.get("wins_ip")
        # nWinsPort:int = LOCAL_CONFIG.get("wins_port")
        # nAgentID:int = LOCAL_CONFIG.get("agent_id")

        # bAllowed:bool = True
        # strModifiedMessage:str = ""

        # #grpc 채널 생성
        # with grpc.insecure_channel(f"{strWinsIP}:{nWinsPort}") as channel:
            
        #     stub = hook_pb2_grpc.HookProxyStub(channel)

        #     #Request 객체, stub에서 호출시 선언을 분리하여 구현
        #     request = hook_pb2.LLMRequest(
        #         request_id = "0",
        #         agent_id = nAgentID,
        #         messages = str(messages),
        #         llm_key = llm_key,
        #         iteration = int(iteration),
        #         stream = stream
        #     )

        #     #서비스 요청 (Request 요청, Response 수신)
        #     response = stub.HookLLMRequest(request, timeout=5)

        #     bAllowed:bool = response.allowed

        #     #사이즈 문제
        #     if 0 == len(response.modified_message):
        #         #TODO: str to list, 변환에 대한 문제. => 확인 필요.
        #         strModifiedMessage = messages

        #     logger.info(f"[HOOK/LLM_REQUEST] grpc response = {response}")

        # request = hook_pb2.LLMRequest(
        #     request_id = "0",
        #     agent_id = nAgentID,
        #     messages = str(messages),
        #     llm_key = llm_key,
        #     iteration = int(iteration),
        #     stream = stream
        # )
        
        request = WinsHookRequestCustomizeHelper.LLMRequest(self.__winsSecurityClient, messages, llm_key, iteration, stream)
        
        response = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOOK_LLM_REQUEST, request)

        bAllowed:bool = response.allowed
        
        #TODO: message 변환 기능 제공 필요. string -> list
        strModifiedMessage:str = response.modified_message        
        lstModifiedMessages:list = WinsSecurityClient.UtilGetModifiedStringData(strModifiedMessage, messages)
        
        return {
            "allowed": bAllowed,
            "modified_messages": lstModifiedMessages,
            "metadata": {
                "hook_name": self.name,
                "llm_key": llm_key,
                "iteration": iteration,
                "processed": True
            }
        }
    
    async def on_mcp_call(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Agent → MCP 도구 호출 처리"""
        
        if self.config["detailed_logging"]:
            logger.info(f"[PLUGIN HOOK] Agent → MCP: server={server_name}, tool={tool_name}")
            logger.info(f"[PLUGIN HOOK] Arguments keys: {list(arguments.keys())}")
        
        # 차단된 도구 체크
        tool_key = f"{server_name}:{tool_name}"
        if tool_key in self.config["blocked_tools"]:
            logger.warning(f"[PLUGIN HOOK] Blocked tool: {tool_key}")
            return {
                "allowed": False,
                "modified_arguments": arguments,
                "metadata": {
                    "error": f"Tool {tool_key} is blocked",
                    "hook_name": self.name
                }
            }
        
        # 위험한 도구 사용 시 경고 (예시)
        dangerous_tools = ["delete", "remove", "drop", "truncate"]
        if any(danger in tool_name.lower() for danger in dangerous_tools):
            logger.warning(f"[PLUGIN HOOK] Dangerous tool call detected: {server_name}:{tool_name}")

        # request = hook_pb2.MCPCallRequest(
        #     request_id = "0",
        #     agent_id = nAgentID,
        #     server_name = server_name,                
        #     tool_name = tool_name,
        #     arguments = str(arguments)
        # )

        #TODO: modified arguments 에 대한 사양 확인 필요
        
        #TODO: message 변환 기능 제공 필요. string -> list
        # strModifiedMessage:str = response.modified_message        
        # lstModifiedMessages:list = WinsSecurityClient.UtilGetModifiedStringData(strModifiedMessage, messages)
        
        # strWinsIP:str = LOCAL_CONFIG.get("wins_ip")
        # nWinsPort:int = LOCAL_CONFIG.get("wins_port")
        # nAgentID:int = LOCAL_CONFIG.get("agent_id")

        # #grpc 채널 생성
        # bAllowed:bool = True
        # # strModifiedArgument:str = ""

        # with grpc.insecure_channel(f"{strWinsIP}:{nWinsPort}") as channel:
            
        #     stub = hook_pb2_grpc.HookProxyStub(channel)

        #     #Request 객체, stub에서 호출시 선언을 분리하여 구현
        #     request = hook_pb2.MCPCallRequest(
        #         request_id = "0",
        #         agent_id = nAgentID,
        #         server_name = server_name,                
        #         tool_name = tool_name,
        #         arguments = str(arguments)
        #     )

        #     #서비스 요청 (Request 요청, Response 수신)
        #     response = stub.HookMCPCall(request, timeout=5)

        #     logger.info(f"[HOOK/MCP_CALL] grpc response = {response}")

        #     bAllowed = response.allowed
        #     # strModifiedArgument = response.modified_arguments

        
        request = WinsHookRequestCustomizeHelper.MCPCallRequest(self.__winsSecurityClient, server_name, tool_name, arguments)        
        response = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOK_MCP_CALL, request)

        bAllowed:bool = response.allowed

        return {
            "allowed": bAllowed,
            "modified_arguments": arguments,
            "metadata": {
                "hook_name": self.name,
                "server_name": server_name,
                "tool_name": tool_name,
                "processed": True
            }
        }

    async def on_mcp_response(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """MCP → Agent 도구 응답 처리"""
        
        if self.config["detailed_logging"]:
            response_preview = str(response)[:200]
            logger.info(f"[PLUGIN HOOK] MCP → Agent: server={server_name}, tool={tool_name}")
            logger.info(f"[PLUGIN HOOK] Response preview: {response_preview}")
        
        # 에러 응답 로깅 강화
        if "error" in response or (isinstance(response, dict) and response.get("is_error", False)):
            logger.error(f"[PLUGIN HOOK] MCP Error: {server_name}:{tool_name} - {response}")
        
        # 응답 크기 체크 (예시)
        response_str = str(response)
        if len(response_str) > 100000:  # 100KB 초과 시 경고
            logger.warning(f"[PLUGIN HOOK] Large response from {server_name}:{tool_name}: {len(response_str)} chars")
        
        return {
            "allowed": True,
            "modified_response": response,
            "metadata": {
                "hook_name": self.name,
                "server_name": server_name,
                "tool_name": tool_name,
                "response_size": len(response_str),
                "processed": True
            }
        }