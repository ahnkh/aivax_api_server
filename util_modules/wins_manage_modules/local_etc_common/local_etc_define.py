
from lib_include import *

from util_modules.wins_manage_modules.local_etc_common.local_define.wins_error_define import WinsErrorDefine

from util_modules.wins_manage_modules.local_etc_common.local_define.wins_command_define import WinsCommandDefine

from util_modules.wins_manage_modules.local_etc_common.local_define.aivax_util_command_define import AivaxUtilCommandDefine

from util_modules.wins_manage_modules.local_etc_common.local_common_helper.wins_sql_db_helper import WinsSQLDBHelper

class WinsModuleDefine:
    
    WINS_COMMAND_DEFINE = WinsCommandDefine
    
    AIVAX_COMMAND_DEFINE = AivaxUtilCommandDefine   
    
    ERROR_DEFINE =  WinsErrorDefine
    # pass