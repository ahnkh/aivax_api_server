#!/home1/aivax/aivax-venv/bin/python

from lib_include import *

from mainapp.kshell_mainapp import KShellMainApp

def debug_print(kshellMainApp:KShellMainApp):
    
    LOG().setLevel(logging.DEBUG)
    AddStreamLogger()
    # pass

def init_command(kshellMainApp:KShellMainApp):
        
    kshellMainApp.RunCLICommand({                
        "method" : ["manage_wins_modules"],
        "ext_module" : "manage_aivax_pipeline",
        "cmd_category" : "aivax_pipeline_util",
        "command" : "aivax_backup",
        "detail_cmd" : "attach_file_backup"    
    })  
    
    # kshellMainApp.RunCLICommand({
    #     "method" : ["manage_wins_modules"],
    #     "ext_module" : "manage_aivax_pipeline",
    #     "cmd_category" : "aivax_pipeline_util",
    #     "command" : "aivax_backup",
    #     "detail_cmd" : "aivax_disk_rotation"            
    # }) 
    
    # kshellMainApp.RunCLICommand({
    #     "method" : ["manage_wins_modules"],
    #     "ext_module" : "manage_aivax_pipeline",
    #     "cmd_category" : "aivax_pipeline_util",
    #     "command" : "aivax_backup",
    #     "detail_cmd" : "aivax_disk_rotation"            
    # })           
    # pass


def main():
    
    InitLogger("tracelog.txt", TRACE_LOG_PATH)
    
    kshellMainApp = KShellMainApp()
    
    dictOpt = {
        KShellParameterDefine.APP_ROOT : KSHELL_APP_ROOT,
        KShellParameterDefine.CONFIG_BASE_PATH : CONFIG_BASE_PATH,
    }
    
    kshellMainApp.Initialize(dictOpt)    
    
    dictFunction:dict[str:Any] = {
        "debug" : debug_print,
        "init" : init_command,        
    }
    
    for strCommand in sys.argv[1:]:
        
        dictFunction[strCommand](kshellMainApp)
        #break
        
    #pass

if __name__ == "__main__":
    main()