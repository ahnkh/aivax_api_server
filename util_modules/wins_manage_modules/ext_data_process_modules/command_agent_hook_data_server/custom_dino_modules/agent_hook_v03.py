"""
Custom Agent Hook for Seahorse MCP Agent

This ConfigMap-based plugin overrides the default hook behavior.
Modify this file to implement custom security policies and filters.
"""

import logging
from typing import Dict, Any, List, Optional
from app.agent_hook import AgentHook

logger = logging.getLogger(__name__)


class CustomAgentHook(AgentHook):
    """Production-ready custom hook implementation"""
    
    def __init__(self):
        self.name = "CustomAgentHook"
        logger.info(f"{self.name} plugin loaded via ConfigMap")
        
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
    
    async def on_browser_message(
        self, 
        query: str, 
        session_id: Optional[str], 
        user_role: Optional[str]
    ) -> Dict[str, Any]:
        """Filter and validate incoming user messages"""
        
        if self.config["log_queries"]:
            logger.info(f"[CUSTOM HOOK] Browser message from {user_role}: {query[:100]}...")
        
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
        
        # Default: allow the message
        return {
            "allowed": True,
            "modified_query": query,
            "metadata": {
                "hook_name": self.name,
                "session_id": session_id,
                "user_role": user_role
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
        
        return {
            "allowed": True,
            "modified_messages": messages,
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
        
        return {
            "allowed": True,
            "modified_arguments": arguments,
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
        
        return {
            "allowed": True,
            "modified_chunk": modified_chunk,
            "stop_stream": False,
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
        
        return {
            "allowed": True,
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
        
        return {
            "allowed": True,
            "modified_response": response,
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