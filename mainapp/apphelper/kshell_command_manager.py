
from lib_include import *

from common_modules.type_hint import *

class KShellCommandManager:
    
    def __init__(self):
        pass
    
    def RunCLICommand(self, mainApp, dictOpt:dict):
        
        apiResponseHandler = ApiResponseHandlerX()
        
        apiResponseHandler.attachSuccessCode()
        
        self.__runCommandList(mainApp, dictOpt, apiResponseHandler)
        
        dictResponse = apiResponseHandler.outResponse()
        self.__writeOutputResponse(dictOpt, dictResponse)
        
        return dictResponse
    
    def RunMultiCommand(self, mainApp, lstMultiCommand:list, dictOpt:dict):
        
        apiResponseHandler = ApiResponseHandlerX()
        
        for dictCommand in lstMultiCommand:
            
            enable_command:int = dictOpt.get(KShellParameterDefine.SCRIPT_MODULE.ENABLE_COMMAND)
            
            if None != enable_command and CONFIG_OPT_DISABLE == enable_command:
                continue
            
            for key in dictOpt.keys():
                
                value:Any = dictOpt.get(key)
                
                if key in dictCommand:
                    continue
                
                dictCommand[key] = value
            
            self.__runCommandList(mainApp, dictCommand, apiResponseHandler)
            
            dictResponse = apiResponseHandler.outResponse()
            self.__writeOutputResponse(dictOpt, dictResponse)
        
        return dictResponse
    
    ################################################### private
    
    def __runCommandList(self, mainApp, dictOpt:dict, apiResponseHandler:ApiResponseHandlerX):
        
        
        lstMethod = dictOpt.get(KShellParameterDefine.METHOD)
        
        if None == lstMethod or 0 == len(lstMethod):
            return ERR_OK
        
        for strMethod in lstMethod:
            
            self.__runCommandAt(mainApp, dictOpt, strMethod, apiResponseHandler)
        
        return ERR_OK
    
    def __runCommandAt(self, mainApp, dictOpt:dict, strMethod:str, apiResponseHandler:ApiResponseHandlerX):
        
        strMethod = str(strMethod).strip()

        method = getattr(mainApp, strMethod)

        method(dictOpt, apiResponseHandler)
        
        return ERR_OK
    
    def __writeOutputResponse(self, dictOpt:dict, dictResponse:dict):
        
        if None == dictResponse:            
            return ERR_OK
        
        api_out_reponse = dictOpt.get(KShellParameterDefine.API_OUT_RESPONSE)
        
        if None != api_out_reponse:        
            JsonHelperX.WriteMapToJsonFile(dictResponse, api_out_reponse)
        
        api_print_console = int(dictOpt.get(KShellParameterDefine.API_PRINT_CONSOLE, CONFIG_OPT_DISABLE))
        
        if None != api_print_console and CONFIG_OPT_ENABLE == api_print_console:
            
            print(json.dumps(dictResponse, indent=4, ensure_ascii=False))
        
        return ERR_OK
        
        