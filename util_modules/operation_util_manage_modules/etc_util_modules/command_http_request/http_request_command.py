
from lib_include import *

from common_modules.type_hint import *

'''
http request 요청 추가
'''

class HttpRequestCommand:
    
    def __init__(self):
        pass
    
    #http request 요청
    def RunCommand(self, dictOpt:dict, dictHttpRequestLocalConfig:dict, apiResponseHandler:ApiResponseHandlerX):
        
        '''
        http_request, 외부 및 API에서 호출 가능하도록 개발.
        '''
        
        # 잦은 요청, LOG 출력 자제.
        LOG().debug(f"run http request, option = {dictOpt}")
        
        # http request id
        strHttpRequestID:str = dictOpt.get(KShellParameterDefine.UTIL_MODULE.HTTP_REQUEST_ID)
        
        # http url opt
        dictUrlOpt:dict = dictOpt.get(KShellParameterDefine.UTIL_MODULE.HTTP_URL_OPT)
        
        # http cookie
        dictCookie:dict = dictOpt.get(KShellParameterDefine.UTIL_MODULE.HTTP_COOKIE)
        
        # http json request
        dictHttpJsonRequest:dict = dictOpt.get(KShellParameterDefine.UTIL_MODULE.HTTP_JSON_REQUEST)
        
        dictHttpOutputResponse = {}
        
        #TODO: 실패시 exception 반환.
        http_request(strHttpRequestID, 
                     dictHttpOutputResponse = dictHttpOutputResponse, 
                     dictUrlOpt=dictUrlOpt, 
                     dictCookie=dictCookie,
                     dictJson=dictHttpJsonRequest)
        
        strOutResponse = dictHttpOutputResponse.get(HttpRequestDefine.OPT_RESPONSE_TEXT)
        
        #TODO: string, dictionary로 변환하여 전달
        dictOutResponse:dict = {}
        JsonHelperX.LoadToDictionary(strOutResponse, dictOutResponse)
        
        apiResponseHandler.attachApiCommandCode("http request command")
        
        # 일단 string으로, 그대로 전달
        apiResponseHandler.attachSuccessCode(dictOutResponse)
        
        return ERR_OK