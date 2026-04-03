
from lib_include import *

from common_modules.type_hint import *

'''
aivax rdb migrate module 추가
'''

class AivaxRDBMigrateCommand:
    
    #TODO: 필요시 향후 적절한 곳으로 이동
    MIGRATE_TYPE_BACKUP = "backup"
    MIGRATE_TYPE_RESTORE = "restore"
    
    def __init__(self):
        pass
    
    def RunCommand(self, dictOpt:dict, dictAivaxUtilModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        백업 및 복구 옵션화
        백업대상 테이블 목록, 해당 목록의 테이블을 백업한다.
        데이터는 지정된 포맷, 또는 원본의 bulk 데이터를 추출한다.
        '''
        
        LOG().info("migrate aivax rdb migrate command")
        
        apiResponseHandler.attachApiCommandCode("rdb migrate command")
        
        apiResponseHandler.attachSuccessCode(f"login success")
        
        # migration 유형에 따른 분기
        # TODO: deftail command 로 분기
        
        detail_cmd = dictOpt.get(KShellParameterDefine.DETAIL_CMD)
        
        # db_migrate_type:str = dictOpt.get(KShellParameterDefine.WINS_MODULE.DB_MIGRATE_TYPE)
        
        if AivaxRDBMigrateCommand.MIGRATE_TYPE_BACKUP == detail_cmd:
            
            from util_modules.wins_manage_modules.ext_aivax_util_modules.command_aivax_migrate.detail_command.rdb_migrate_backup_command import RDBMigrateBackupCommand
            
            detailCommand:RDBMigrateBackupCommand = RDBMigrateBackupCommand()
            detailCommand.RunCommand(dictOpt, dictAivaxUtilModuleLocalConfig, apiResponseHandler)
            # LOG().info("backup aivax rdb")
            
        elif AivaxRDBMigrateCommand.MIGRATE_TYPE_RESTORE == detail_cmd:
            
            from util_modules.wins_manage_modules.ext_aivax_util_modules.command_aivax_migrate.detail_command.rdb_migrate_restore_command import RDBMigrateRestoreCommand
            
            detailCommand:RDBMigrateRestoreCommand = RDBMigrateRestoreCommand()
            detailCommand.RunCommand(dictOpt, dictAivaxUtilModuleLocalConfig, apiResponseHandler)            
            # pass
        
        return ERR_OK
    
    #################################################### private
    
    