#!/home1/aivax/aivax-venv/bin/python

from lib_include import *

from mainapp.kshell_mainapp import KShellMainApp

def init_command(kshellMainApp:KShellMainApp):
        
    kshellMainApp.RunCLICommand({                
        "method" : ["manage_wins_modules"],
        "ext_module" : "manage_aivax_pipeline",
        "cmd_category" : "aivax_pipeline_util",
        "command" : "aivax_backup",
        "detail_cmd" : "attach_file_backup"    
    })  
    
    kshellMainApp.RunCLICommand({
        "method" : ["manage_wins_modules"],
        "ext_module" : "manage_aivax_pipeline",
        "cmd_category" : "aivax_pipeline_util",
        "command" : "aivax_backup",
        "detail_cmd" : "aivax_disk_rotation"            
    }) 
    
    kshellMainApp.RunCLICommand({
        "method" : ["manage_wins_modules"],
        "ext_module" : "manage_aivax_pipeline",
        "cmd_category" : "aivax_pipeline_util",
        "command" : "aivax_backup",
        "detail_cmd" : "aivax_disk_rotation"            
    })   
        
    # pass


def main():
    
    InitLogger("tracelog.txt", TRACE_LOG_PATH)
    LOG().setLevel(logging.DEBUG)
    
    kshellMainApp = KShellMainApp()
    
    dictOpt = {
        KShellParameterDefine.APP_ROOT : KSHELL_APP_ROOT,
        KShellParameterDefine.CONFIG_BASE_PATH : CONFIG_BASE_PATH,
    }
    
    kshellMainApp.Initialize(dictOpt)    
    # pass
    
    dictFunction:dict[str:Any] = {
        "init" : init_command
    }
    
    command:list[str] = sys.argv[1:]   
    
    for strCommand in sys.argv[1:]:
        
        command:Any = dictFunction.get(strCommand)     
        command(kshellMainApp)
        #break
        
    #pass

if __name__ == "__main__":
    main()