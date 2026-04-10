
class AivaxUtilCommandDefine:
    
    # RDB Migration 관련
    
    # migration - detail command
    DETAIL_CMD_MIGRATE_TYPE_BACKUP = "backup"
    DETAIL_CMD_MIGRATE_TYPE_RESTORE = "restore"
    
    # Pipeline filter - detail command
    DETAIL_CMD_FILTER_DETECT_TEST = "filter_detect_test"
    
    #세부 옵션 - pipeline, 우선 하나로
    # pipline 탐지 테스트 - 입력 프롬프트, 목록
    PROMPT_TEST_LIST = "prompt_test_list"
    # FILTER_TEST_TYPE = "filter_test_type" #pipeline filter, 테스트 유형, regex, file, slm
    PIPELINE_FILTER_LIST = "pipeline_filter_list" # 실패 filter ["input_filter", "secret_filter", "file_block_filter", "slm_filter"]
    TEST_EMAIL = "test_email" # pipeline 탐지시, 이메일 테스트를 위해서 전달
    
    pass