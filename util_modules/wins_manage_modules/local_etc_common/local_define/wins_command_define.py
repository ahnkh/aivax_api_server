

class WinsCommandDefine:

    EXT_MODULE_MANAGE_WINS_DATA_PROCESS = "manage_wins_data_process"

    EXT_MODULE_MANAGE_WINS_API_MODULE = "manage_wins_api_module"

    CMD_CATEGORY_DATA_PROCESS_SERVER = "data_process_server"

    COMMAND_RUN_DATA_SERVER = "run_data_server"
    
    
    #계정관리 명령, 세부 분기
    DETAIL_CMD_ADD_USER = "add_user"
    DETAIL_CMD_EDIT_USER = "edit_user"
    DETAIL_CMD_DELETE_USER = "delete_user"
    DETAIL_CMD_LIST_USER = "list_user"
    
    #sql etc command
    DETAIL_CMD_CUSTOM_USER_GROUP = "user_group"
    DETAIL_CMD_CUSTOM_FILTER_VIEW = "filter_view"
    DETAIL_CMD_CUSTOM_ETC_SQL_COMMAND = "etc_sql_command"
    
    
    #detail sub command - 사용자 그룹
    DETAIL_SUB_CMD_USER_GROUP_ADD = "add_user_group"
    DETAIL_SUB_CMD_USER_GROUP_EDIT = "edit_user_group"
    DETAIL_SUB_CMD_USER_GROUP_DELETE = "delete_user_group"
    # DETAIL_SUB_CMD_USER_GROUP_LIST = "list_user_group"
    
    #detail sub command - filterview
    DETAIL_SUB_CMD_FILTER_VIEW_ADD = "add_filter_view"
    DETAIL_SUB_CMD_FILTER_VIEW_EDIT = "edit_filter_view"
    DETAIL_SUB_CMD_FILTER_VIEW_DELETE = "delete_filter_view"
    DETAIL_SUB_CMD_FILTER_VIEW_LIST = "list_filter_view"
    
    #detail sub commnad - etc sql
    DETAIL_SUB_CMD_ADD_DATA = "add_data"
    DETAIL_SUB_CMD_EDIT_DATA = "edit_data"
    DETAIL_SUB_CMD_DELETE_DATA = "delete_data"
    DETAIL_SUB_CMD_LIST_DATA = "list_data"
    
    
    #Filed 관련 상수
    SET = "set"
    WHERE = "where"
    LIMIT = "limit"
    
    pass
