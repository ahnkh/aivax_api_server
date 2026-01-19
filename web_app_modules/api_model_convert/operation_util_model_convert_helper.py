
from lib_include import *

from common_modules.type_hint import *

from web_app_modules.web_lib_include import *

class OperationUtilModelConvertHelper:

    @staticmethod
    def executeSQLApi(byteRawBody: bytes):

        dictItemModel = {}
        JsonHelperX.LoadToDictionary(byteRawBody, dictItemModel)

        dictItemModel[KShellParameterDefine.METHOD] = ["manage_operation_util_modules"]
        dictItemModel[KShellParameterDefine.EXT_MODULE] = "manage_sql_cli_module"
        dictItemModel[KShellParameterDefine.CMD_CATEGORY] = "sql_cli_module"
        dictItemModel[KShellParameterDefine.COMMAND] = "sql_map_cli"

        return dictItemModel