
from lib_include import *

from common_modules.type_hint import *

'''
RDB migrate - backup command
'''

class RDBMigrateBackupCommand:
    
    def __init__(self):
        pass
    
    def RunCommand(self, dictOpt:dict, dictAivaxUtilModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        백업대상 테이블 목록, 인자로 받는다.
        공용의 sqlmap을 호출한다. 전체 백업, 테이블 정보를 받는다.
        결과를 json (list, dictionary)로, 테이블 정보를 키로, 파일에 저장한다.
        TODO: API로 호출, command 관리 필요
        
        TODO: 복구시, 기존 데이터 삭제후 복구, merge 복구 선택이 되어야 한다.
        백업 및 복구 기능도 UI가 필요하며, UI이전에 명령 개발을 먼저 진행후 전달한다.
        '''
        
        LOG().info("aivax migrate - backup command")
        
        backup_table_list:list = dictOpt.get(KShellParameterDefine.WINS_MODULE.DB_MIGRATE_BACKUP_TABLE_LIST)
        
        backup_dest_path:str = dictOpt.get(KShellParameterDefine.WINS_MODULE.DB_MIGRATE_BACKUP_DEST_PATH)
        
        # migration 관련 local config
        aivax_rdb_migrate_command:dict = dictAivaxUtilModuleLocalConfig.get("aivax_rdb_migrate_command")
        
        backup_sql_query_map_id:str = aivax_rdb_migrate_command.get("backup_sql_query_map_id")
        
        self.__exportBackupRDBTable(backup_sql_query_map_id, backup_table_list, backup_dest_path)
        
        return ERR_OK
    
    ############################## private
    
    #RDB의 테이블을 외부 파일로 백업, export 시킨다.
    def __exportBackupRDBTable(self, strSQLQueryMapID:str, lstBackupTableList:list, strBackupDestPath:str):
        
        '''
        '''
        
        dictAllDBExportInfo = {}
        
        for strBackupTable in lstBackupTableList:
            
            #TODO: 개별 테이블에 대한 백업
            #백업이 실패하거나 없더라도, 오류만 기록하고 다음으로 이동한다.
            nErrEachBackup:int = self.__exportEachBackupRDBTable(strBackupTable, strSQLQueryMapID, dictAllDBExportInfo)
            
            if ERR_FAIL == nErrEachBackup:
                LOG().error(f"fail backup table {strBackupTable}")
            # pass
        
        #TODO: json 으로 저장
        JsonHelperX.WriteMapToJsonFile(dictAllDBExportInfo, strBackupDestPath, bIndent=False, strDateTime="%Y-%m-%d %H:%M:%S")
        
        return ERR_OK
    
    # 개별 테이블에 대한 백업, 오류 발생시 오류만 출력한다.
    def __exportEachBackupRDBTable(self, strBackupTable:str, strSQLQueryMapID:str, dictAllDBExportInfo:dict):
        
        '''
        '''
        
        try:
            
            dictParameter = {
                "table" : strBackupTable
            }
            
            #table, 존재 여부 체크
            strTableNameForExistCheck:str = self.__splitTableName(strBackupTable)
            
            nTableCount:int = self.__getTableCount(strTableNameForExistCheck)
            
            if 0 == nTableCount:
                LOG().info(f"table {strBackupTable} is not exist, stop backup table")
                return ERR_FAIL
            
            # DB 조회
            dictDBResult = {}
                
            sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, strSQLQueryMapID, dictParameter, dictDBResult)
            
            #TODO: 응답 결과, 저장
            #table 이름으로 update하는게 가장 깔끔
            #TODO: 결과에 대한 처리 - 그대로 저장도 가능
            dictAllDBExportInfo[strBackupTable] = dictDBResult
            
        except Exception as err: 
                       
            LOG().error(traceback.format_exc())
            return ERR_FAIL
        
        
        return ERR_OK
    
    
    # table 명, 추출한다.
    def __splitTableName(self, strTableName:str) -> str:
        
        '''
        '''
        
        if "." in strTableName:
            return strTableName.rsplit(".", 1)[-1]
        else:
            return strTableName
        
    # DB내에 Table이 존재하는지 확인
    def __getTableCount(self, strTableName:str) -> int:
        
        '''
        '''
        
        dictDBResult = {}
        
        dictParameter = {
            "table" : strTableName
        }
                
        sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_select_migrate_table_exist", dictParameter, dictDBResult)
        
        dictQueryData:dict = dictDBResult.get(DBSQLDefine.QUERY_DATA)
        
        count:int = dictQueryData.get("count")
        
        return count
        
    
            
        
            
        
        
    
    