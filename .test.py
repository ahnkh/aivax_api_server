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
    
def check_integrity(kshellMainApp:KShellMainApp):
    
    strAivaxInstallPath:str = "/home1/aivax"
    
    kshellMainApp.RunCLICommand({                
        "method" : ["manage_wins_modules"],
        "ext_module" : "manage_aivax_install",
        "cmd_category" : "aivax_install",
        "command" : "aivax_install_util",
        "detail_cmd" : "server_integrity",
        "detail_sub_cmd" : "check_server_integrity",
        "aivax_install_root" :"/home1/aivax",
        "api_print_console" : 1
    })  
    
    
    pass


def main():
    
    InitLogger("tracelog.txt", TRACE_LOG_PATH)
    
    kshellMainApp = KShellMainApp()
    
    dictOpt = {
        KShellParameterDefine.APP_ROOT : KSHELL_APP_ROOT,
        KShellParameterDefine.CONFIG_BASE_PATH : CONFIG_BASE_PATH,
    }
    
    kshellMainApp.Initialize(dictOpt)    
    
    #test
    # check_integrity(kshellMainApp)
    
    dictFunction:dict[str:Any] = {
        "debug" : debug_print,
        "init" : init_command,
        "integrity" : check_integrity        
    }
    
    for strCommand in sys.argv[1:]:
        
        dictFunction[strCommand](kshellMainApp)
        #break
        
    #pass

if __name__ == "__main__":
    main()
    
    