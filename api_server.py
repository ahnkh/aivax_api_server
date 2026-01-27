
import getopt
import logging
import uvloop

from lib_include import *
from common_modules.type_hint import *

# from common_modules.global_common_module import GlobalCommonModule

from mainapp.kshell_mainapp import KShellMainApp

from web_app_modules.web_api_mainapp import WebApiMainApp

uvloop.install()

def RunOpenApiServer(dictOpt:dict, mainApp:KShellMainApp):
    
    strMainDescriptFile = "local_resource/web_api_resource_files/api_description/main_desc.txt"
    strDescription = FileIOHelper.OpenFileAsUTFToStream(strMainDescriptFile)
    
    strApiRootPath:str = dictOpt.get(KShellParameterDefine.API_ROOT_PATH)
    
    webMainApp = WebApiMainApp(title="AIVAX Open API", 
                               docs_url="/docs", 
                               redoc_url=None,                             
                               root_path=strApiRootPath,
                               openapi_url="/openapi.json", 
                               description = strDescription)
                            
    strRootFilePath = os.path.dirname(__file__)
    strAbsoluteDir = os.path.join(strRootFilePath, "local_resource/web_api_resource_files/openapi/static/")

    from fastapi.staticfiles import StaticFiles
    webMainApp.mount("/openapi/static", StaticFiles(directory=strAbsoluteDir), name="static")
    
    webMainApp.Initialize(dictOpt, mainApp)

    webMainApp.AddApiRouter()
     
    webMainApp.RunWebApiServer(dictOpt)
    pass

def main():

    InitLogger("tracelog.txt", TRACE_LOG_PATH, TRACE_PREFIX)
    
    winsCliMainApp = KShellMainApp()
    
    try:
        
        opts, args = getopt.getopt(sys.argv[1:], "dhm:pw:f:s:",
            [
                "debug", "printlog", "method=", "module=", "dummy", "cmd_category=", "command=", "ext_module=",
                "open_api",
                                
                "api_out_response=", "api_print_console=", "app_root=", "api_root_path=",
                "config_base_path=",
                
                "host=",                
                "port=",
                "query=",
                "request=",

                "script_config=", "script_file=",
                "ssl_cert_file_path=",
                "ssl_key_file_path=", 
                
                "uniq_id=",
            ])
                    
        dictOpt = {
            KShellParameterDefine.APP_ROOT : KSHELL_APP_ROOT,
            KShellParameterDefine.API_ROOT_PATH : "",
            KShellParameterDefine.CONFIG_BASE_PATH : CONFIG_BASE_PATH,
            KShellParameterDefine.OPEN_API : CONFIG_OPT_ENABLE,

            KShellParameterDefine.METHOD : [],
        }
        
        for o, args in opts:

            if o in ("-d", "--debug"):
                LOG().setLevel(logging.DEBUG)
            
            elif o in ("-p", "--printlog"): 
                AddStreamLogger()

            elif o in ("-m", "--method", "--module"): 
                dictOpt["method"].append(args)

            else:
                                
                strOptKey = o[2:]
                
                if None != args and 0 < len(args) :
                    dictOpt[strOptKey] = args
                else:
                    dictOpt[strOptKey] = CONFIG_OPT_ENABLE
        
        LOG().info(f"start process pid = {os.getpid()}, argc = {len(sys.argv)}, argv = {str(sys.argv)}, option = {dictOpt}")
        
        bInitializeMainApp = winsCliMainApp.Initialize(dictOpt)
        
        if ERR_FAIL == bInitializeMainApp:
            LOG().error("fail initialize main app, exit")
            return ERR_FAIL
        
        if CONFIG_OPT_ENABLE == dictOpt.get(KShellParameterDefine.OPEN_API):
            
            LOG().info("start open api server")
            RunOpenApiServer(dictOpt, winsCliMainApp)            
            pass
        
        winsCliMainApp.RunCLICommand(dictOpt)
        
    except Exception as err: 
        
        AddStreamLogger()
        
        LOG().error(traceback.format_exc())
        
        GlobalCommonModule.RaiseException(ErrorDefine.CLI_UNKNOWN_ERROR, ErrorDefine.CLI_UNKNOWN_ERROR_MSG, str(err))      
        pass
    
    finally:

        strDisposeMethodName:str = "dispose_instance"
        winsCliMainApp.DisposeApplication(strDisposeMethodName)
        pass
    
    return ERR_OK

if __name__ == "__main__":
    main()    
