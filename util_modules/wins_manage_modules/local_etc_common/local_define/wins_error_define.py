
from lib_include import *

'''
Error code 정의
CATEGORY_API_APP_ERROR = 4000 #WINS API 프로그램 중오류
'''

class WinsErrorDefine(ErrorDefine):
    
    API_APP_LOGIN_EROR = ErrorDefine.CATEGORY_API_APP_ERROR + "1001" #로그인 오류
    API_APP_LOGIN_ERROR_MSG = "login error"
    
    API_APP_USER_ACCOUNT_ERROR = ErrorDefine.CATEGORY_API_APP_ERROR + "1002" # 계정관리 오류
    API_APP_USER_ACCOUNT_ERROR_MSG = "user account error"
    pass
    
    