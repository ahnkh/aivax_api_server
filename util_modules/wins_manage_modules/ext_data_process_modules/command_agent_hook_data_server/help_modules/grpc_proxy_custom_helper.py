
import threading
# import grpc
from pymysql.converters import escape_string

from lib_include import *

from common_modules.type_hint import *

#DB, SQL DB 관리 TODO: 잘못된 설계, Bulk, Pool구조로 변경하고, 로그와 단발성 DB는 분리한다.
from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.sqldb_custom_submodules.local_custom_db_helper import LocalCustomDBHelper

#DataFilter처리 담당.
from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.filter_submodules.hook_data_filter_manager import HookDataFilterManager

#수집 로그의 Filter저장 관리
from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.log_write_submodules.grpc_log_write_handler import GrpcLogWriteHandler
from util_modules.wins_manage_modules.ext_data_process_modules.command_agent_hook_data_server.help_modules.log_write_submodules.gprc_log_write_custom_helper import GrpcLogWriteCustomHelper

'''
grpc proxy에서 실제 로직의 담당, customize로 로직 다수.
request, response 는 any로 감싼다.
TODO: 너무 잘라도 부담이다. request에 관련된 처리는 여기서 수행한다.
TODO: DB 처리만 따로 분리해야 할 필요성. => DB가 결정되면 그때 이동하자.
DB가 MariaDB외 다른 DB가 있으며, SQLDB와 LogDB로 분리한다.
TODO: Helper는 하나로, 여기서 분리한다. SQL, LogDB결정되면 개발, 이후 주석 정리.
'''

class GrpcProxyCustomHelper:

    def __init__(self):

        #helper 클래스, 로컬에서 생성, 관리 (스레드/동시 접근 주의)
        self.__localCustomDBHelper = LocalCustomDBHelper()

        #hook, data filter처리
        self.__hookDataFilterManager = HookDataFilterManager()

        #TODO: 제거, 로직 변경 필요
        # self.__lock = threading.Lock()
        # self.__lock = threading.RLock()

        self.__gprcLogWriteCustomHelper = GrpcLogWriteCustomHelper()

        pass


    ####################################################  중계기능, Getter

    #TODO: 별로 적절하지는 않으나, 소스 최소화, 중계기 개념으로 접근
    def LocalCustomDBHelper(self) -> LocalCustomDBHelper:

        return self.__localCustomDBHelper
    
    def FilterManager(self) -> HookDataFilterManager:

        return self.__hookDataFilterManager
    
    def GrpcLogWriteCustomHelper(self) -> GrpcLogWriteCustomHelper:

        return self.__gprcLogWriteCustomHelper
    
    #TOOD: 감사로그 관리자 개발.
    
