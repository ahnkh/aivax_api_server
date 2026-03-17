"""
Custom Agent Hook for Seahorse MCP Agent

This ConfigMap-based plugin overrides the default hook behavior.
Modify this file to implement custom security policies and filters.
"""

import logging
from typing import Dict, Any, List, Optional
from app.agent_hook import AgentHook
from app.hook_utils import HookUtils

logger = logging.getLogger(__name__)

import sys
sys.path.append("/app/plugins/")

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
    """Production-ready custom hook implementation"""
    
    def __init__(self):
        self.name = "CustomAgentHook"
        self.hook_utils = HookUtils()  # Initialize HookUtils
        logger.info(f"{self.name} plugin loaded via ConfigMap with HookUtils")
        
        # Configuration
        self.config = {
            # Maximum query length by role
            "max_query_length": {
                "admin": 50000,
                "user": 10000,
                "viewer": 5000
            },
            
            # Blocked LLM models
            "blocked_llm_keys": [
                # Add model keys to block here
                # "expensive-model-key",
            ],
            
            # Blocked MCP tools (server:tool format)
            "blocked_tools": [
                # Examples:
                # "erp-database:execute_sql_query",  # Block direct SQL on ERP
                # "kubernetes:delete_resource",       # Block K8s deletions
            ],
            
            # Sensitive patterns to mask
            "sensitive_patterns": [
                (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***'),  # Email
                (r'\b\d{3}-\d{3,4}-\d{4}\b', '***-****-****'),  # Phone
                (r'\b\d{6,}\b', '******'),  # Long numbers (potential IDs)
            ],
            
            # Keywords that trigger blocking
            "blocked_keywords": [
                "drop table",
                "delete from",
                "truncate",
                "rm -rf",
            ],
            
            # Test mode keywords (remove in production)
            "test_keywords": [
                "유저메시지 차단 테스트",
                "block_test",
                "test_block",
            ],
            
            # Logging configuration
            "detailed_logging": True,
            "log_queries": True,
            "log_responses": False,  # Set to True for debugging
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
        """Filter and validate incoming user messages"""
        
        if self.config["log_queries"]:
            logger.info(f"[CUSTOM HOOK] Browser message from {user_role}: {query[:100]}...")
        
        # HookUtils 테스트 키워드 체크
        if "훅 유틸리티 테스트" in query:
            logger.info(f"[CUSTOM HOOK] HookUtils test triggered for session: {session_id}")
            
            # HookUtils를 사용하여 세션 정보 조회
            test_results = []
            
            try:
                # 1. 세션 정보 조회
                if session_id:
                    session_info = self.hook_utils.get_session_info(session_id)
                    if session_info:
                        test_results.append(f"✅ 세션 정보 조회 성공:")
                        test_results.append(f"  - 세션 ID: {session_info.session_id}")
                        test_results.append(f"  - 생성 시간: {session_info.created_at}")
                        test_results.append(f"  - 메시지 수: {session_info.message_count}")
                        test_results.append(f"  - 제목: {session_info.title or '없음'}")
                    else:
                        test_results.append(f"⚠️ 세션 정보를 찾을 수 없음: {session_id}")
                
                # 2. 최근 메시지 조회
                if session_id:
                    recent_messages = self.hook_utils.get_recent_messages(session_id, limit=3)
                    test_results.append(f"\n📝 최근 메시지 {len(recent_messages)}개:")
                    for msg in recent_messages:
                        preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                        test_results.append(f"  - [{msg.role}]: {preview}")
                
                # 3. 세션 통계 조회
                if session_id:
                    stats = self.hook_utils.get_session_statistics(session_id)
                    test_results.append(f"\n📊 세션 통계:")
                    test_results.append(f"  - 총 메시지: {stats.get('total_messages', 0)}")
                    test_results.append(f"  - 평균 메시지 길이: {stats.get('avg_message_length', 0):.0f}")
                    test_results.append(f"  - 도구 호출 횟수: {stats.get('tool_calls_count', 0)}")
                
                # 4. 활성 시스템 프롬프트 조회
                system_prompt = self.hook_utils.get_active_system_prompt()
                if system_prompt:
                    test_results.append(f"\n🔧 활성 시스템 프롬프트: {system_prompt.get('name', 'Unknown')}")
                
                # 5. 활성 언어 설정 조회
                language = self.hook_utils.get_active_language()
                if language:
                    test_results.append(f"🌐 활성 언어: {language.get('name', 'Unknown')} ({language.get('code', 'Unknown')})")
                
                # 6. 사용자 활동 요약
                activity = self.hook_utils.get_user_activity_summary(days=1)
                test_results.append(f"\n📈 최근 24시간 활동:")
                test_results.append(f"  - 총 세션: {activity.get('total_sessions', 0)}")
                test_results.append(f"  - 활성 세션: {activity.get('active_sessions', 0)}")
                test_results.append(f"  - 총 메시지: {activity.get('total_messages', 0)}")
                
            except Exception as e:
                test_results.append(f"\n❌ 테스트 중 오류 발생: {str(e)}")
                logger.error(f"[CUSTOM HOOK] HookUtils test error: {e}", exc_info=True)
            
            # 테스트 결과를 error_message로 반환하여 웹에서 확인 가능하도록 함
            error_message = "🧪 HookUtils 테스트 결과:\n\n" + "\n".join(test_results)
            
            return {
                "allowed": False,  # 메시지를 차단하여 테스트 결과만 표시
                "modified_query": query,
                "error_message": error_message,
                "metadata": {
                    "hook_name": self.name,
                    "reason": "hook_utils_test",
                    "session_id": session_id,
                    "test_results": test_results
                }
            }
        
        # Check test keywords (remove in production)
        if any(keyword in query for keyword in self.config["test_keywords"]):
            logger.warning(f"[CUSTOM HOOK] Test keyword detected, blocking message")
            return {
                "allowed": False,
                "modified_query": query,
                "error_message": "🚫 Hook 시스템 테스트: 이 메시지는 보안 정책 테스트를 위해 차단되었습니다.",
                "metadata": {
                    "hook_name": self.name,
                    "reason": "test_keyword"
                }
            }
        
        # Check role-based query length limits
        if user_role in self.config["max_query_length"]:
            max_length = self.config["max_query_length"][user_role]
            if len(query) > max_length:
                logger.warning(f"[CUSTOM HOOK] Query too long for role {user_role}: {len(query)} > {max_length}")
                return {
                    "allowed": False,
                    "modified_query": query,
                    "error_message": f"Query exceeds maximum length for your role ({max_length} characters)",
                    "metadata": {
                        "hook_name": self.name,
                        "reason": "query_too_long",
                        "query_length": len(query),
                        "max_length": max_length
                    }
                }
        
        # Check for dangerous keywords
        query_lower = query.lower()
        for keyword in self.config["blocked_keywords"]:
            if keyword.lower() in query_lower:
                logger.warning(f"[CUSTOM HOOK] Blocked keyword detected: {keyword}")
                return {
                    "allowed": False,
                    "modified_query": query,
                    "error_message": "Your query contains restricted operations",
                    "metadata": {
                        "hook_name": self.name,
                        "reason": "blocked_keyword",
                        "keyword": keyword
                    }
                }
            

        request = WinsHookRequestCustomizeHelper.BrowserHookRequest(self.__winsSecurityClient, query, session_id, user_role)

        response = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOOK_BROWSER_MESSAGE, request)
        
        # Default: allow the message
        return {
            "allowed": response.allowed,
            "modified_query": WinsSecurityClient.UtilGetModifiedStringData(response.modified_query, query),
            # "error_message": "Your query contains restricted operations",
            "error_message": WinsSecurityClient.UtilGetModifiedStringData(response.error_message, ""),
            "metadata": {
                "hook_name": self.name,
                # "reason": "test_keyword",
                "reason": response.reason,
                "session_id": session_id,
                "user_role": user_role,                
            }
        }
    
    async def on_llm_request(
        self,
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int,
        stream: bool
    ) -> Dict[str, Any]:
        """Filter LLM requests"""
        
        if self.config["detailed_logging"]:
            logger.info(f"[CUSTOM HOOK] LLM request: model={llm_key}, iteration={iteration}")
        
        # Check blocked models
        if llm_key and llm_key in self.config["blocked_llm_keys"]:
            logger.warning(f"[CUSTOM HOOK] Blocked LLM model: {llm_key}")
            return {
                "allowed": False,
                "modified_messages": messages,
                "metadata": {
                    "hook_name": self.name,
                    "reason": "blocked_model",
                    "model": llm_key
                }
            }
        
        # Prevent infinite loops
        if iteration > 50:
            logger.warning(f"[CUSTOM HOOK] Too many iterations: {iteration}")
            return {
                "allowed": False,
                "modified_messages": messages,
                "metadata": {
                    "hook_name": self.name,
                    "reason": "too_many_iterations",
                    "iterations": iteration
                }
            }
        
        request = WinsHookRequestCustomizeHelper.LLMRequest(self.__winsSecurityClient, messages, llm_key, iteration, stream)
        
        response = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOOK_LLM_REQUEST, request)
        
        return {
            "allowed": response.allowed,
            "modified_messages": WinsSecurityClient.UtilGetModifiedCollectionData(response.modified_message, messages),
            "metadata": {
                "hook_name": self.name,
                "llm_key": llm_key,
                "iteration": iteration
            }
        }
    
    async def on_mcp_call(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Filter MCP tool calls"""
        
        tool_key = f"{server_name}:{tool_name}"
        
        if self.config["detailed_logging"]:
            logger.info(f"[CUSTOM HOOK] MCP call: {tool_key}")
        
        # Check blocked tools
        if tool_key in self.config["blocked_tools"]:
            logger.warning(f"[CUSTOM HOOK] Blocked tool: {tool_key}")
            return {
                "allowed": False,
                "modified_arguments": arguments,
                "metadata": {
                    "hook_name": self.name,
                    "reason": "blocked_tool",
                    "tool": tool_key
                }
            }
        
        # Log dangerous operations
        dangerous_tools = ["delete", "remove", "drop", "truncate", "execute_sql_query"]
        if any(danger in tool_name.lower() for danger in dangerous_tools):
            logger.warning(f"[CUSTOM HOOK] Potentially dangerous tool: {tool_key}")
            # You could add additional validation here
        
        request = WinsHookRequestCustomizeHelper.MCPCallRequest(self.__winsSecurityClient, server_name, tool_name, arguments)        
        response = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOK_MCP_CALL, request)

        return {
            "allowed": response.allowed,
            "modified_arguments": WinsSecurityClient.UtilGetModifiedCollectionData(response.modified_arguments, arguments),
            "metadata": {
                "hook_name": self.name,
                "server": server_name,
                "tool": tool_name
            }
        }
    
    async def on_llm_stream_chunk(
        self,
        chunk: str,
        accumulated_response: str,
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int
    ) -> Dict[str, Any]:
        """Process streaming chunks (be efficient here)"""
        
        # Apply sensitive data masking
        modified_chunk = self._mask_sensitive_data(chunk)

        request = WinsHookRequestCustomizeHelper.LLMStreamChunkRequest(self.__winsSecurityClient, chunk, accumulated_response, messages, llm_key, iteration)        
        response = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOOK_LLM_STREAM_CHUNK, request)

        modified_chunk = WinsSecurityClient.UtilGetModifiedCollectionData(response.modified_chunk, chunk)
        
        return {
            "allowed": response.allowed,
            "modified_chunk": modified_chunk,
            "stop_stream": response.stop_stream,
            "metadata": {
                "hook_name": self.name,
                "masked": modified_chunk != chunk
            }
        }
    
    async def on_llm_response(
        self,
        response: str,
        messages: List[Dict[str, str]],
        llm_key: Optional[str],
        iteration: int,
        stream: bool
    ) -> Dict[str, Any]:
        """Post-process complete LLM responses"""
        
        if self.config["log_responses"]:
            logger.info(f"[CUSTOM HOOK] LLM response length: {len(response)}")
        
        # Apply sensitive data masking
        modified_response = self._mask_sensitive_data(response)
        
        # Remove internal thinking tags if present
        import re
        think_pattern = r'<think>.*?</think>'
        if re.search(think_pattern, modified_response, re.DOTALL):
            modified_response = re.sub(think_pattern, '', modified_response, flags=re.DOTALL)
            if self.config["detailed_logging"]:
                logger.info("[CUSTOM HOOK] Removed thinking tags from response")
        
        # Truncate very long responses
        max_length = 100000  # 100KB
        if len(modified_response) > max_length:
            modified_response = modified_response[:max_length] + "\n\n[Response truncated]"
            logger.warning(f"[CUSTOM HOOK] Response truncated: {len(response)} -> {max_length}")


        request = WinsHookRequestCustomizeHelper.LLMResponseRequest(self.__winsSecurityClient, response, messages, llm_key, iteration, stream)        
        grpcResponse = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOOK_LLM_RESPONSE, request)

        modified_response = WinsSecurityClient.UtilGetModifiedCollectionData(grpcResponse.modified_response, response)
        
        return {
            "allowed": grpcResponse.allowed,
            "modified_response": modified_response,
            "metadata": {
                "hook_name": self.name,
                "original_length": len(response),
                "modified_length": len(modified_response)
            }
        }
    
    async def on_mcp_response(
        self,
        server_name: str,
        tool_name: str,
        arguments: Dict[str, Any],
        response: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process MCP tool responses"""
        
        # Log errors
        if "error" in response:
            logger.error(f"[CUSTOM HOOK] MCP error from {server_name}:{tool_name}: {response}")

        request = WinsHookRequestCustomizeHelper.MCPResponseRequest(self.__winsSecurityClient, server_name, tool_name, arguments, response)        
        grpcResponse = self.__winsSecurityClient.SendToWinsServer(WinsSecurityClient.METHOD_HOOK_MCP_RESPONSE, request)

        return {
            "allowed": grpcResponse.allowed,
            "modified_response": WinsSecurityClient.UtilGetModifiedCollectionData(grpcResponse.modified_response, response),
            "metadata": {
                "hook_name": self.name,
                "server": server_name,
                "tool": tool_name
            }
        }
    
    def _mask_sensitive_data(self, text: str) -> str:
        """Apply sensitive data masking patterns"""
        import re
        
        modified = text
        for pattern, replacement in self.config["sensitive_patterns"]:
            if re.search(pattern, modified):
                modified = re.sub(pattern, replacement, modified)
        
        return modified