
from lib_include import *

from common_modules.type_hint import *

from web_app_modules.web_lib_include import *

class WinsModelConvertHelper:

    @staticmethod
    def runGrpcServer(modelItem:GrpcServerItem):

        '''        
        '''

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_data_process",
            KShellParameterDefine.CMD_CATEGORY : "agent_hook_data_server",
            KShellParameterDefine.COMMAND : "grpc_data_recv_server_fromapi",
            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.PORT : modelItem.port
        }

    #grpc client 실행
    @staticmethod
    def runGrpcClient(modelItem:GrpcClientItem):
        
        return {

            KShellParameterDefine.METHOD : ["manage_wins_modules"], 
            KShellParameterDefine.EXT_MODULE : "manage_wins_data_process",
            KShellParameterDefine.CMD_CATEGORY : "agent_hook_data_server",
            KShellParameterDefine.COMMAND : "grpc_data_req_client",
            KShellParameterDefine.EXEC_TYPE : "dbb",

            KShellParameterDefine.HOST : modelItem.host,
            KShellParameterDefine.PORT : modelItem.port,

            KShellParameterDefine.QUERY : modelItem.prompt,
            KShellParameterDefine.REQUEST : modelItem.hook

            #TODO: 부가기능, 프롬프트등 전달. 통일된 파라미터로 전달
        }
    
    #사용자 로그인 요청
    @staticmethod
    def authLogin(modelItem:LoginModelItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "login_auth_api",
            KShellParameterDefine.COMMAND : "login_command",
            KShellParameterDefine.EXEC_TYPE : "dbb",

            KShellParameterDefine.ID : modelItem.user_id,
            KShellParameterDefine.PASSWORD : modelItem.user_pw
        }
    
    #사용자 계정 정보 조회
    @staticmethod
    def getUserAccount(modelItem: UserAccountListItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "list_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_select_user_account",
            
            KShellParameterDefine.LIMIT : modelItem.limit,
            
            KShellParameterDefine.CONDITION : {
                "user_id" : modelItem.condition.user_id,          
                "login_status" : modelItem.condition.login_status,
                "use_flag" : modelItem.condition.use_flag  
            }            
        }
    
    #사용자 계정 등록
    @staticmethod
    def insertUserAccount(modelItem:UserAccountInsertItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "add_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_insert_to_user_account",
            # KShellParameterDefine.CUSTOMIZE_CONVERTOR : "convert_user_group_insert_item",
            
            KShellParameterDefine.PARAMETER : {
                "user_id" : modelItem.user_id,
                "user_passwd" : modelItem.user_passwd,
                "email" : modelItem.email,
                "dept" : modelItem.dept,
                
                "tel" : modelItem.tel,
                "etc_comment" : modelItem.etc_comment,
                "login_status" : modelItem.login_status,
            }  

        }
        
    #사용자 계정 수정
    @staticmethod
    def editUserAccount(modelItem:UserAccountEditItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "edit_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_update_user_account",
            # KShellParameterDefine.CUSTOMIZE_CONVERTOR : "convert_user_group_insert_item",
            
            KShellParameterDefine.UPDATE : {
                
                "user_passwd" : modelItem.update.user_passwd,
                "email" : modelItem.update.email,
                "dept" : modelItem.update.dept,
                "tel" : modelItem.update.tel,
                "etc_comment" : modelItem.update.etc_comment,
                "login_status" : modelItem.update.login_status
            },
            
            KShellParameterDefine.CONDITION : {
                "user_id" : modelItem.condition.user_id,
                "login_status" : modelItem.condition.login_status,
                "use_flag" : modelItem.condition.use_flag
            }


        }
        
    #사용자 계정 삭제
    @staticmethod
    def deleteUserAccount(modelItem:UserAccountDeleteItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "delete_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_delete_user_account",

            KShellParameterDefine.CONDITION : {
                "user_id" : modelItem.condition.user_id,
                "login_status" : modelItem.condition.login_status,
                "use_flag" : modelItem.condition.use_flag
            }

        }
    
    #그룹 추가,수정,삭제,조회
    @staticmethod
    def getUserGroup(modelItem:UserGroupListItem):

        return {            
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "list_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_select_user_group",
            
            KShellParameterDefine.LIMIT : modelItem.limit,
            
            KShellParameterDefine.CONDITION : {
                "group_id" : modelItem.condition.group_id,
                "group_name" : modelItem.condition.group_name,
                "use_flag" : modelItem.condition.use_flag
            },

        }
        
    @staticmethod
    def insertUserGroup(modelItem:UserGroupInsertItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "add_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_insert_to_user_group",
            KShellParameterDefine.CUSTOMIZE_CONVERTOR : "convert_user_group_insert_item",
            
            KShellParameterDefine.PARAMETER : {
                "group_id" : modelItem.group_id,
                "group_name" : modelItem.group_name,
                "etc_comment" : modelItem.etc_comment,
                "use_flag" : modelItem.use_flag
            }     

        }
        
    @staticmethod
    def editUserGroup(modelItem:UserGroupEditItem):

        return {            
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "edit_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_update_set_user_group",
            # KShellParameterDefine.CUSTOMIZE_CONVERTOR : "convert_user_group_insert_item",
            
            KShellParameterDefine.UPDATE : {
                
                "group_name" : modelItem.update.group_name,
                "etc_comment" : modelItem.update.etc_comment,
                "use_flag" : modelItem.update.use_flag
            },
            
            KShellParameterDefine.CONDITION : {
                "group_id" : modelItem.condition.group_id,
                "group_name" : modelItem.condition.group_name,
                "use_flag" : modelItem.condition.use_flag
            }

        }
        
    @staticmethod
    def deleteUserGroup(modelItem:UserGroupDeleteItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "delete_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_delete_user_group",

            KShellParameterDefine.CONDITION : {
                "group_id" : modelItem.condition.group_id,
                "group_name" : modelItem.condition.group_name,
                "use_flag" : modelItem.condition.use_flag
            }
        }
        
    #filterview 추가,수정,삭제,조회
    @staticmethod
    def getFilterView(modelItem:UserAccountEditItem):

        return {
            # KShellParameterDefine.METHOD : ["manage_operation_util_modules"],
            # KShellParameterDefine.EXT_MODULE : "manage_sql_cli_module",
            # KShellParameterDefine.CMD_CATEGORY : "sql_cli_module",
            # KShellParameterDefine.COMMAND : "sql_map_cli",

            # KShellParameterDefine.ID : "rdb_select_all_user_account",

        }
        
    @staticmethod
    def insertFilterView(modelItem:UserAccountEditItem):

        return {
            # KShellParameterDefine.METHOD : ["manage_operation_util_modules"],
            # KShellParameterDefine.EXT_MODULE : "manage_sql_cli_module",
            # KShellParameterDefine.CMD_CATEGORY : "sql_cli_module",
            # KShellParameterDefine.COMMAND : "sql_map_cli",

            # KShellParameterDefine.ID : "rdb_select_all_user_account",

        }
        
    @staticmethod
    def editFilterView(modelItem:UserAccountEditItem):

        return {
            # KShellParameterDefine.METHOD : ["manage_operation_util_modules"],
            # KShellParameterDefine.EXT_MODULE : "manage_sql_cli_module",
            # KShellParameterDefine.CMD_CATEGORY : "sql_cli_module",
            # KShellParameterDefine.COMMAND : "sql_map_cli",

            # KShellParameterDefine.ID : "rdb_select_all_user_account",

        }
        
    @staticmethod
    def deleteFilterView(modelItem:UserAccountEditItem):

        return {
            # KShellParameterDefine.METHOD : ["manage_operation_util_modules"],
            # KShellParameterDefine.EXT_MODULE : "manage_sql_cli_module",
            # KShellParameterDefine.CMD_CATEGORY : "sql_cli_module",
            # KShellParameterDefine.COMMAND : "sql_map_cli",

            # KShellParameterDefine.ID : "rdb_select_all_user_account",

        }
        
    #차단 정보 조회
    @staticmethod
    def getPromptBlockInfo(modelItem:PromptBlockLogItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "list_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_select_browser_prompt",
            
            KShellParameterDefine.LIMIT : modelItem.limit,
            
            KShellParameterDefine.CONDITION : {
                "allowed" : modelItem.condition.allowed,
                "reason" : modelItem.condition.reason,                
            },

        }
        
    @staticmethod
    def getMCPServerBlockInfo(modelItem:MCPServerBlockLogItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "list_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_select_user_group",
            
            KShellParameterDefine.LIMIT : modelItem.limit,
            
            KShellParameterDefine.CONDITION : {
                "tool_name" : modelItem.condition.tool_name,
                "reg_type" : modelItem.condition.reg_type,
                "allowed" : modelItem.condition.allowed,
                "reason" : modelItem.condition.reason
            },

        }
    
    @staticmethod
    def getUserMonitorStatus(modelItem:UserMonitorLogItem):

        return {
            KShellParameterDefine.METHOD : ["manage_wins_modules"],
            KShellParameterDefine.EXT_MODULE : "manage_wins_api_module",
            KShellParameterDefine.CMD_CATEGORY : "etc_custom_sql",
            KShellParameterDefine.COMMAND : "etc_custom_sql_command",
                        
            KShellParameterDefine.DETAIL_CMD : "etc_sql_command",

            KShellParameterDefine.DETAIL_SUB_CMD : "list_data",

            KShellParameterDefine.EXEC_TYPE : "dbb",
            
            KShellParameterDefine.ID : "rdb_select_user_group",
            
            KShellParameterDefine.LIMIT : modelItem.limit,
            
            KShellParameterDefine.CONDITION : {
                "user_id" : modelItem.condition.user_id,
                "allowed" : modelItem.condition.allowed,
                "reason" : modelItem.condition.reason
            },

        }
    
    
    


    

