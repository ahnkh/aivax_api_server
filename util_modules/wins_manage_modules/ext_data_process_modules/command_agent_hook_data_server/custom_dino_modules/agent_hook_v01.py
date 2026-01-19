
"""
Agent Hook System (docker-compose mounted version)

로컬 docker-compose 환경에서 컨테이너 내 `/app/app/agent_hook.py`를 대체합니다.
로그에 [HOOK/LOCAL] 접두사를 사용합니다.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

#AgentHook 소스에 맞춰 수정
import sys
sys.path.append("/app/app/")

import grpc

import hook_pb2
import hook_pb2_grpc

logger = logging.getLogger(__name__)

"""
TODO: wins sec server 접속 정보 관리 필요
IP, PORT
"""

LOCAL_CONFIG = {
    # "wins_ip" : "10.0.80.35",
    "wins_ip" : "192.168.122.12",    
    "wins_port" : 50000,
    "agent_id" : 100
}

class AgentHook(ABC):
    """Agent Hook 인터페이스"""

    @abstractmethod
    async def on_browser_message(
        self,
        query: str,
        session_id: Optional[str],
        user_role: Optional[str],
    ) -> Dict[str, Any]:
        """Browser → Agent 메시지 수신 시점 hook"""
        pass

    @abstractmethod
    async def on_llm_request(
        self,
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int,
        stream: bool,
    ) -> Dict[str, Any]:
        """Agent → LLM 요청 시점 hook"""
        pass

    @abstractmethod
    async def on_mcp_call(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Agent → MCP 도구 호출 시점 hook"""
        pass


class DefaultAgentHook(AgentHook):
    """기본 Agent Hook 구현체 - Local docker-compose 버전"""

    def __init__(self):
        self.name = "LocalComposeAgentHook"
        logger.info(f"[HOOK/LOCAL] {self.name} 초기화됨 (docker-compose로 마운트됨)")

    async def on_browser_message(
        self,
        query: str,
        session_id: Optional[str],
        user_role: Optional[str],
    ) -> Dict[str, Any]:
        
        strWinsIP:str = LOCAL_CONFIG.get("wins_ip")
        nWinsPort:int = LOCAL_CONFIG.get("wins_port")
        nAgentID:int = LOCAL_CONFIG.get("agent_id")

        strRPCUrl = f"{strWinsIP}:{nWinsPort}"

        logger.info(
            f"[HOOK/LOCAL] Browser → Agent(WINS TEST): session_id={session_id}, user_role={user_role}, query_length={len(query)}, WinsIP={strRPCUrl}"
        )
        logger.info(f"[HOOK/LOCAL] Query preview: {query[:100]}...")

        bAllowed = True

        with grpc.insecure_channel(strRPCUrl) as channel:

            stub = hook_pb2_grpc.HookProxyStub(channel)
            response = stub.HookBrowserMessage(hook_pb2.BrowserHookRequest(
                request_id = "0",
                agent_id = nAgentID,
                query = query,
                session_id = session_id,
                user_role = user_role
            ))

            logger.info(f"[HOOK/BROWSER_REQUEST] grpc response = {response}")

            bAllowed = response.allowed
            # response.source

        return {
            "allowed": bAllowed,
            "modified_query": query,
            "metadata": {
                "hook_name": self.name,
                "source": "local-compose",
                "session_id": session_id,
                "user_role": user_role,
                "original_query_length": len(query),
            },
        }

    async def on_llm_request(
        self,
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int,
        stream: bool,
    ) -> Dict[str, Any]:
        logger.info(
            f"[HOOK/LOCAL] Agent → LLM: llm_key={llm_key}, iteration={iteration}, stream={stream}, messages_count={len(messages)}"
        )

        if messages:
            last_message = messages[-1]
            logger.info(
                f"[HOOK/LOCAL] Last message role={last_message.get('role')}, content_preview={last_message.get('content', '')[:100]}..."
            )
        
        strWinsIP:str = LOCAL_CONFIG.get("wins_ip")
        nWinsPort:int = LOCAL_CONFIG.get("wins_port")
        nAgentID:int = LOCAL_CONFIG.get("agent_id")

        bAllowed = True

        #grpc 채널 생성
        with grpc.insecure_channel(f"{strWinsIP}:{nWinsPort}") as channel:
            
            stub = hook_pb2_grpc.HookProxyStub(channel)

            #Request 객체, stub에서 호출시 선언을 분리하여 구현
            request = hook_pb2.LLMRequest(
                request_id = "0",
                agent_id = nAgentID,
                messages = str(messages),
                llm_key = llm_key,
                iteration = int(iteration),
                stream = stream
            )

            #서비스 요청 (Request 요청, Response 수신)
            response = stub.HookLLMRequest(request)

            bAllowed = response.allowed

            logger.info(f"[HOOK/LLM_REQUEST] grpc response = {response}")

        return {
            "allowed": bAllowed,
            "modified_messages": messages,
            "metadata": {
                "hook_name": self.name,
                "source": "local-compose",
                "llm_key": llm_key,
                "iteration": iteration,
                "stream": stream,
                "messages_count": len(messages),
            },
        }

    async def on_mcp_call(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> Dict[str, Any]:
        logger.info(
            f"[HOOK/LOCAL] Agent → MCP: server={server_name}, tool={tool_name}, args_keys={list(arguments.keys())}"
        )
        logger.info(f"[HOOK/LOCAL] Tool arguments: {arguments}")

        strWinsIP:str = LOCAL_CONFIG.get("wins_ip")
        nWinsPort:int = LOCAL_CONFIG.get("wins_port")
        nAgentID:int = LOCAL_CONFIG.get("agent_id")

        #grpc 채널 생성
        bAllowed = True

        with grpc.insecure_channel(f"{strWinsIP}:{nWinsPort}") as channel:
            
            stub = hook_pb2_grpc.HookProxyStub(channel)

            #Request 객체, stub에서 호출시 선언을 분리하여 구현
            request = hook_pb2.MCPCallRequest(
                request_id = "0",
                agent_id = nAgentID,
                server_name = server_name,                
                tool_name = tool_name,
                arguments = str(arguments)
            )

            #서비스 요청 (Request 요청, Response 수신)
            response = stub.HookMCPCall(request)

            logger.info(f"[HOOK/MCP_CALL] grpc response = {response}")

            bAllowed = response.allowed

        return {
            "allowed": bAllowed,
            "modified_arguments": arguments,
            "metadata": {
                "hook_name": self.name,
                "source": "local-compose",
                "server_name": server_name,
                "tool_name": tool_name,
                "arguments_keys": list(arguments.keys()),
            },
        }

_agent_hook: Optional[AgentHook] = None


def get_agent_hook() -> AgentHook:
    global _agent_hook
    if _agent_hook is None:
        _agent_hook = DefaultAgentHook()
    return _agent_hook


def set_agent_hook(hook: AgentHook) -> None:
    global _agent_hook
    _agent_hook = hook
    logger.info(f"[HOOK/LOCAL] Agent hook 변경됨: {hook.__class__.__name__}")