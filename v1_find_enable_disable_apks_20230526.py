import re # regex
import os


def crteate_file_with_app_package_name(what_to_search):
    if what_to_search == 'a':
        # list all installed apps
        file_to_save_app_list = 'dump_all_apps.txt'
        os.system(f"adb shell pm list packages > {file_to_save_app_list} --user 0")
    elif what_to_search == 'd':
        # list all disabled apps
        file_to_save_app_list = 'dump_all_disabled_apps.txt'
        os.system(f"cd /Volumes/14TB_EXOS_28102020/UserDataForMac/Documents/Github/adb-package_blocker && adb shell pm list packages > {file_to_save_app_list} --user 0 -d")
    elif what_to_search == 'u':
        # list all 3rd pary apps.
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



def find_n_disable_enable_apps(list_of_file_names_with_app_package_names, term_to_search_for, enable_or_disable):
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
    # run command file.
    os.system('./search-output.command')
    # delete all generate file.
    os.remove(f'{list_of_file_names_with_app_package_names[0]}')
    os.remove('./search-output.command')


if __name__ == "__main__":
    what_to_search = input('Do you want to search only user apps (u) , only system apps (s) , all apps (a) , disabled apps (d) , enabled apps (e) ?')

    list_of_file_names_with_app_package_names = crteate_file_with_app_package_name(what_to_search)

    term_to_search_for = input('if you want to search for any specific word in the package name, enter it here.\n')

    enable_or_disable = input('do you want to enable (e) apps or disable (d) them ?')

    find_n_disable_enable_apps(list_of_file_names_with_app_package_names, term_to_search_for, enable_or_disable)