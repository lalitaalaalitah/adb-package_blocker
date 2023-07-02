#! /Users/lalitaalaalitah/.pyenv/versions/3.8.13/envs/adb/bin/python
# 
import re # regex
import os
# 
# from androguard.misc import AnalyzeAPK
# # 
# a, d, dx = AnalyzeAPK(apk_file)
# package_name = a.get_package()
# print(package_name)
import argparse
# 
# v1    :   20230526    :   Initial version highly modified. Args added to avoid manual entry of choices.
# v2    :   20230702    :   Added option to check each command and confirm each to run, Option to run batch is also there are previous version. Reboot option at end added.
# 
def get_args():
    parser = argparse.ArgumentParser(description='combine all images to a pdf.')
    parser.add_argument('-e', '--EnableTheApp', type=str, help='Enable App. y, n.', required=False)
    parser.add_argument('-d', '--DisableTheApp', type=str, help='Disable App. y, n', required=False)
    parser.add_argument('-t', '--TypeOfAppToSearch', type=str, help='Type of app to search : only user apps (u) , only system apps (s) , all apps (a) , disabled apps (d) , enabled apps (e).', required=False)
    parser.add_argument('-s', '--SearchString', type=str, help='string to search in app name..', required=False)
    args = parser.parse_args()
    # print(type(args))
    var_arguments = vars(args)
    # print(type(var_arguments))
    # for key in var_arguments.keys():
    #     print(key)
    #     print(var_arguments[key])
    return var_arguments



def create_file_with_app_package_name(what_to_search):
    if what_to_search == 'a':
        # list all installed apps
        file_to_save_app_list = 'dump_all_apps.txt'
        os.system(f"adb shell pm list packages > {file_to_save_app_list} --user 0")
    elif what_to_search == 'd':
        # list all disabled apps
        file_to_save_app_list = 'dump_all_disabled_apps.txt'
        os.system(f"cd /Volumes/14TB_EXOS_28102020/UserDataForMac/Documents/Github/adb-package_blocker && adb shell pm list packages > {file_to_save_app_list} --user 0 -d")
    elif what_to_search == 'u':
        # list all 3rd party apps.
        file_to_save_app_list = 'dump_all_user_apps.txt'
        os.system(f"adb shell pm list packages > {file_to_save_app_list} --user 0 -3")
    elif what_to_search == 's':
        # list all system apps.
        file_to_save_app_list = 'dump_all_system_apps.txt'
        os.system(f"adb shell pm list packages > {file_to_save_app_list} --user 0 -s")
    elif what_to_search == 'e':
        # list all system apps.
        file_to_save_app_list = 'dump_all_enabled_apps.txt'
        os.system(f"adb shell pm list packages > {file_to_save_app_list} --user 0 -e")
    # 
    return [file_to_save_app_list]



def find_n_disable_enable_apps(list_of_file_names_with_app_package_names, term_to_search_for, enable_or_disable, what_to_search, run_again, batch_work):
    # 
    with open('search-output.command', 'w') as output:     # open file for writing
        with open(f'{list_of_file_names_with_app_package_names[0]}','r',encoding='UTF-8') as myFile: # open file for reading (create it via cmd using: adb shell pm list packages > "c:\users\USER\dump-packages_all.txt")
            for line in myFile: # read myFile line by line
                if term_to_search_for != "":
                    reg = re.compile(rf'{term_to_search_for}') # matches "KEYWORD" in lines
                    # 
                    if reg.search(line): # if there is a match anywhere in a line
                        if enable_or_disable == 'd':
                            # disable apps.
                            output.write(line.replace('package:', 'adb shell pm disable-user ')) # write the line into the new file
                        elif enable_or_disable == 'e':
                            # enable apps.
                            output.write(line.replace('package:', 'adb shell pm enable ')) # write the line into the new file
                else:
                    if enable_or_disable == 'd':
                            # disable apps.
                            output.write(line.replace('package:', 'adb shell pm disable-user ')) # write the line into the new file
                    elif enable_or_disable == 'e':
                        # enable apps.
                        output.write(line.replace('package:', 'adb shell pm enable ')) # write the line into the new file
    # make command file executable.
    os.system('chmod +x search-output.command')
    # 
    run_script_confirmation_bool = False
    # 
    dict_of_app_type_n_string_to_print = {'a' : 'System+User>All', 's' : 'System', 'd' : 'Disabled' , 'e' : 'Enabled', 'u' : 'User'}
    # 
    if term_to_search_for == "":
        term_to_search_for_string_to_print = 'Have Not Filtered The Search With Any String'
    else:
        term_to_search_for_string_to_print = f'Have filtered the search with string : {term_to_search_for} ;'
    # 
    if enable_or_disable == 'd':
        # disable apps.
        enable_or_disable_string_to_print = 'Disable'
    elif enable_or_disable == 'e':
        # enable apps.
        enable_or_disable_string_to_print = 'Enable'
    # get confirmation again
    run_script_confirmation_raw = input(f'\n\nwe have found all {dict_of_app_type_n_string_to_print[what_to_search]} apps and we {term_to_search_for_string_to_print} and we are going to {enable_or_disable_string_to_print} these now. Are you sure to do this?\ty, AnyOtherKey\n')
    # 
    if run_script_confirmation_raw == 'y':
        run_script_confirmation_bool = True
    # run command file.
    if run_script_confirmation_bool and batch_work:
        print('now running a script to do desired work.')
        os.system('./search-output.command')
    # 
    if run_script_confirmation_bool and not batch_work:
        print('now we will ask to confirm enable/disable job for each matching app.')
        # 
        with open('search-output.command', 'r') as output:
            list_of_cmds = output.readlines()
        for each_cmd in list_of_cmds:
            print(each_cmd.strip())
            if input('do you want to do this ? y, n') == 'y':
                os.system(f'{each_cmd.strip()}')
    # delete files if no further run is needed.
    if not run_again:
        # delete all generate file.
        os.remove(f'{list_of_file_names_with_app_package_names[0]}')
        os.remove('./search-output.command')
# 
# 
# 
if __name__ == "__main__":
    # 
    os.chdir(os.path.dirname(__file__))
    # 
    var_arguments_1 = get_args()
    # 
    if var_arguments_1["TypeOfAppToSearch"]:
        what_to_search = var_arguments_1["TypeOfAppToSearch"]
    else:
        what_to_search = input('Do you want to search only user apps (u) , only system apps (s) , all apps (a) , disabled apps (d) , enabled apps (e) ?')
    # 
    # 
    list_of_file_names_with_app_package_names = create_file_with_app_package_name(what_to_search)
    # 
    # 
    # 
    run_again = True
    # 
    while run_again:
        # 
        if var_arguments_1["SearchString"]:
            term_to_search_for = var_arguments_1["SearchString"]
        else:
            term_to_search_for = input('if you want to search for any specific word in the package name, enter it here.\n')
        # 
        # 
        if var_arguments_1["EnableTheApp"]:
            if var_arguments_1["EnableTheApp"] == 'y':
                enable_or_disable = 'e'
            else:
                enable_or_disable = 'd'
        elif var_arguments_1["DisableTheApp"]:
            if var_arguments_1["DisableTheApp"] == 'y':
                enable_or_disable = 'd'
            else:
                enable_or_disable = 'e'
        else:
            enable_or_disable = input('do you want to enable (e) apps or disable (d) them ?')
        # 
        if what_to_search == 's' or what_to_search == 'a':
            if term_to_search_for == "" and enable_or_disable == 'd':
                print('can not run disable command for all system apps. It will put device in a boot-loop.')
                exit()
        # 
        batch_work = True
        if input('do you want to enable/disable by checking each command? y, n') == 'y':
            batch_work = False
        # 
        find_n_disable_enable_apps(list_of_file_names_with_app_package_names, term_to_search_for, enable_or_disable, what_to_search, run_again, batch_work)
        # 
        run_again_raw = input('do you want to run the same process for some other search string? y , n')
        # 
        if run_again_raw != 'y':
            run_again = False
            if input('do you want to reboot your phone? y, n') == 'y':
                os.system('adb reboot')