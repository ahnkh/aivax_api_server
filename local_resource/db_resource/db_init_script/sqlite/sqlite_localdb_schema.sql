
/** local db config scheam **/
drop table INSTANCE_MODULE_MAP;

-- meta 데이터, 컬럼은 소문자로 정의.

CREATE TABLE INSTANCE_MODULE_MAP(
    "cmd_category" TEXT,
    "command" TEXT PRIMARY KEY,
    "package" TEXT,
    "class" TEXT,
    "method" TEXT,

    UNIQUE (CMD_CATEGORY, COMMAND)
);

--grpc server 실행
INSERT OR REPLACE INTO INSTANCE_MODULE_MAP VALUES (
    'agent_hook_data_server', 
    'grpc_data_recv_server', 
    'util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_agent_data_recv_server_command',
    'GRPCAgentDataRecvServerCommand',
    'RunDaemon'
    );

-- grpd server - api에서 실행
INSERT OR REPLACE INTO INSTANCE_MODULE_MAP VALUES (
    'agent_hook_data_server', 
    'grpc_data_recv_server_fromapi', 
    'util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_agent_data_recv_server_command',
    'GRPCAgentDataRecvServerCommand',
    'RunExtProcess'
    );  

-- grpc client 실행
INSERT OR REPLACE INTO INSTANCE_MODULE_MAP VALUES (
    'agent_hook_data_server', 
    'grpc_data_req_client', 
    'util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.grpc_client_command',
    'GrpcClientCommand',
    'RequestToGrpcServer'
    );        

-- login 명령 실행
INSERT OR REPLACE INTO INSTANCE_MODULE_MAP VALUES (
    'login_auth_api', 
    'login_command', 
    'util_modules.wins_manage_modules.ext_api_modules.command_login_auth.login_command',
    'LoginCommand',
    'RunCommand'
    );

-- 사용자 계정 관리 명령 실행
INSERT OR REPLACE INTO INSTANCE_MODULE_MAP VALUES (
    'user_account_api', 
    'user_account_manage_command', 
    'util_modules.wins_manage_modules.ext_api_modules.command_user_account.user_account_manage_command',
    'UserAccountManageCommand',
    'RunCommand'
    );

-- 기타 sql 명령 실행
INSERT OR REPLACE INTO INSTANCE_MODULE_MAP VALUES (
    'etc_custom_sql', 
    'etc_custom_sql_command', 
    'util_modules.wins_manage_modules.ext_api_modules.command_etc_custom_sql.sql_etc_customize_command',
    'SQLEtcCustomizeCommand',
    'RunCommand'
    );
