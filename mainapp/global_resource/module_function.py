
from lib_include import *

from common_modules.type_hint import *

'''
편의성 차원의 함수의 제작 및 선언
lib_include 와의 순환 참조 주의
'''

#http request 모듈, 외부 함수 추가
def http_request(strQueryMapID: str, dictHttpOutputResponse: dict, dictUrlOpt: dict = None, dictPostOpt: dict = None, dictReflectMethod: dict = None, dictHeader : dict = None, dictFile :dict = None, dictCookie: dict = None, dictJson:dict = None):

    '''
    Global CommonModule 외 추가적인 편의성, 함수로 접근하도록 기능 제공
    '''
    
    httpRequestInterface:HttpRequestInterfaceHelper = GlobalCommonModule.SingletonFactoryInstance(FactoryInstanceDefine.CLASS_HTTP_REQUEST_INTERFACE)

    nErrorRequest = httpRequestInterface.ExecuteHttpRequest(strQueryMapID, dictHttpOutputResponse, dictUrlOpt, dictPostOpt, dictReflectMethod, dictHeader, dictFile, dictCookie, dictJson)

    if ERR_FAIL == nErrorRequest:
        LOG().error("fail execute http request")
        return ERR_FAIL
    
    return ERR_OK

#pyconv, utftext 함수로 제공
def UTF8Text(strText):
    
    return PYCONV().UTF8Text(strText)

#sqlprint, query 실행
def sqlprintf(strQueryMapCategory:str, strQueryMapID:str, dictParameter:dict, dictDBResult:dict):

    '''
    GlobalCommonModule, 그대로 호출
    TODO: 예외처리, 반환값 구조에 대한 고민.
    '''

    GlobalCommonModule.SQLPrintf(strQueryMapCategory, strQueryMapID, dictParameter, dictDBResult)

    return ERR_OK

    