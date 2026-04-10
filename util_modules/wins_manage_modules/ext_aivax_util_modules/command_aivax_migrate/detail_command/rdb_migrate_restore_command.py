
from lib_include import *

from common_modules.type_hint import *

'''
aivax - RDB 복구 모듈
'''

class RDBMigrateRestoreCommand:
    
    def __init__(self):
        pass
    
    def RunCommand(self, dictOpt:dict, dictAivaxUtilModuleLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        백업된 RDB의 json 파일을 읽어서 
        테이블별로 복구한다.
        '''
        
        LOG().info("aivax migrate - restore command")
        
        apiResponseHandler.attachApiDetailCommandCode("aivax rdb restore")
        
        restore_table_list:list = dictOpt.get(KShellParameterDefine.WINS_MODULE.DB_MIGRATE_RESTORE_TABLE_LIST)
        
        restore_source_path:str = dictOpt.get(KShellParameterDefine.WINS_MODULE.DB_MIGRATE_RESTORE_SOURCE_PATH)
        
        #기존 테이블 삭제 여부, 기본값 False
        use_truncate:bool = dictOpt.get(KShellParameterDefine.WINS_MODULE.DB_MIGRATE_USE_TABLE_TRUNCATE, False)
        
        # 테이블별 복구
        dictOutputResponse:dict = {
            "header.metadata":
            {
                "backup_date" : datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), # 백업 날짜
                "backup_source" : restore_source_path, #백업 경로 
                "restore_table_list" : restore_table_list, #백업 대상 테이블
                "truncate" : use_truncate
            }
        }
        self.__restoreFromBakupDBFile(restore_table_list, restore_source_path, use_truncate, dictOutputResponse)
        
        #복구 결과 저장
        apiResponseHandler.attachSuccessCode(dictOutputResponse)
        
        return ERR_OK
        
    def __restoreFromBakupDBFile(self, lstRestoreTable:list, strSourceFilePath:str, bUseTruncate:bool, dictOutputResponse:dict):
        
        '''
        저장된 백업파일, 테이블 정보와 데이터를 토대로 복구한다.
        bulk 형태로 넣되, 내부의 컬럼 개수로 insert into 구문으로 bulk 처리를 해본다.
        복구는 선택된 정보로 추가한다.
        TODO: 기존 데이터를 삭제후 추가할지, append 시킬지, 선택 옵션이 제공되어야 한다.
        
        source 파일을 복구, dictionary로 만든다.
        '''
        
        dictSourceDBInfo = {}
        nErrorReadFile:int = JsonHelperX.JsonFileToDictionary(strSourceFilePath, dictSourceDBInfo)
        
        if ERR_FAIL == nErrorReadFile:
            LOG().error("fail read source file {strSourceFilePath}")
            return ERR_FAIL
        
        for strTableName in dictSourceDBInfo.keys():
            
            #복구목록에 존재하는지 확인 (상세 예외처리는 필요)
            if strTableName in lstRestoreTable:
                
                dictTableInfo:dict = dictSourceDBInfo.get(strTableName)
                
                if None == dictTableInfo:
                    LOG().error(f"invalid restore, table {strTableName} backup is not exist")
                    continue
                
                query_data:list = dictTableInfo.get("query_data")
                
                #첫번째 컬럼, 키 정보가 있다.
                #데이터가 없으면 skip
                if None == query_data or 0 == len(query_data):
                    LOG().info(f"table {strTableName} is empty, no data, skip")
                    continue
                
                #TODO: 개별 테이블별로 호출
                self.__restoreEachDBTableAt(strTableName, query_data, bUseTruncate, dictOutputResponse)
                # pass
            
            # pass
                
        return ERR_OK
    
    def __restoreEachDBTableAt(self, strTableName:str, lstQueryData:list, bUseTruncate:bool, dictOutputResponse:dict):
        
        '''
        TODO: 복구시, 백업테이블과 컬럼이 상이, 컬럼이 추가되거나 삭제되었을경우 테이블 오류가 발생한다.
        자동으로 테이블 개수를 생성하는 것은 문제가 되고, 이경우 config를 통해서 제어하는, 옵션화가 필요하다.
        '''
        
        dictColumnMeta:dict = lstQueryData[0]
                
        lstTableColumn = dictColumnMeta.keys()
        
        strTableColumnField = ", ".join(f"`{col}`" for col in lstTableColumn)
        
        #AI 추천코드, VALUE 이하 필드를 생성한다.
        placeholders = ", ".join(["%s"] * len(lstTableColumn))
        
        # sqlmap에서 처리
        # sql = f"INSERT INTO `{strTableName}` ({strTableColumnField}) VALUES ({placeholders})"
        
        lstBulkData:list = []
        
        for dictDBData in lstQueryData:
            
            #TODO: DB에 저장, 동적으로 => 여기는 성능이 문제가 되지 않는다. 단건 저장도 고려
            
            lstBulkData.append(tuple(dictDBData[col] for col in lstTableColumn))
            # pass
            
        #복구전 과거 데이터 삭제 여부
        if True == bUseTruncate:
            dictTruncateResult:dict = {}
            dictParameter:dict = {
                "table" : strTableName,
            }
            
            sqlprintf(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_bulk_truncate_any_table", dictParameter, dictTruncateResult)
            # pass
            
        # 마지막에 bulk
        dictDBBulkResult = {}
        
        dictSQLParameter:dict = {
            "table" : strTableName,
            "columns" : strTableColumnField,
            "values" : placeholders
        }
        # INSERT INTO `{table}` ({columns}) VALUES ( {values} )
        sqlbulk(DBSQLDefine.BASE_CATEGORY_RDB, "rdb_bulk_migration_any_table", lstBulkData, dictDBBulkResult, dictSQLParameter=dictSQLParameter)
        
        LOG().info(f"restore {strTableName}, data count = {len(lstQueryData)}, result = {dictDBBulkResult}")
        
        #복구 결과 기록
        dictOutputResponse[strTableName] = dictDBBulkResult
        
        return ERR_OK
        
        