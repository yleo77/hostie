#!/usr/bin/env python
    
import sys
import getpass
import os
import subprocess
from os import path

from colorful import *

hosts_file = "/etc/hosts"

hostie_dirs = [
    path.expanduser(path.join("~", ".config/hostie")) + '/',
    sys.path[0] + "/profiles/"
]
profiles = {}
for file in os.listdir(hostie_dirs[0]):
    profiles[file] = hostie_dirs[0] + file

for file in os.listdir(hostie_dirs[1]):
    profiles[file] = hostie_dirs[1] + file

START_TOKEN = "################# added by hostie"
END_TOKEN   = "################# end of hostie"

def exit_with_message(message = '', type = 'default'):
    if len(message) > 0:
        print(colorful(message, type))
    exit(0)

def flush():
    
    try:
        subprocess.call('sudo killall -HUP mDNSResponder', shell=True)
    except:
        exit_with_message("You need Refresh DNS Cache", 'warn')

def write(profile):
    if privilege() == False:
        exit_with_message("Oops... Please run it as *root* user.", "error")    

    if check(profile) == False:
        exit_with_message( "Oops... Profile: \"" + profile + "\" Not Found...", "warn")

    file = profiles[profile]

    if os.path.exists(file) == False:
        exit_with_message( "Oops... \"" + file + "\" Not Found...", "warn")

    try:
        file = open(file)

        lines = file.readlines()
        hosts_file_handle = reset(True)

        hosts_file_handle.writelines(START_TOKEN + "\n")
        for line in lines:
            hosts_file_handle.writelines(line)

        hosts_file_handle.writelines("\n################# current profile: \"" +
                profile + "\"\n")
        hosts_file_handle.writelines(END_TOKEN + "\n")

        close(file)
        close(hosts_file_handle)
        flush()
        
        exit_with_message( "\"" + profile +"\" Profile Added in /etc/hosts.", 'info')
    except Exception, e:
        exit_with_message("Error...") 

def reset(type = False):

    if privilege() == False:
        exit_with_message("Oops... Please run it as *root* user.", 'error')    

    hosts_file_handle = open(hosts_file, "r+")
    lines = hosts_file_handle.readlines()
    startIndex = -1
    endIndex   = -1
    
    for index, line in enumerate(lines):
        if line.strip() == START_TOKEN:
            startIndex = index
        elif line.strip() == END_TOKEN:
            endIndex = index

    if startIndex > -1:
        slines = lines[0:startIndex]
        elines = lines[endIndex+1:index+1]

        slines.extend(elines)

        hosts_file_handle.seek(0)
        hosts_file_handle.write(''.join(slines))
        hosts_file_handle.truncate()
    
    if type:
        return hosts_file_handle 
    else:
        hosts_file_handle.close()
        flush()
        exit_with_message("Reset Successfully.", "info")

def close(file):
    file.close()

def show():

    hosts_file_handle = open(hosts_file, "r")
    lines = hosts_file_handle.readlines()
    startIndex = -1
    endIndex   = -1
    log_type = 'default'
    
    for index, line in enumerate(lines):
        if line.strip() == START_TOKEN:
            startIndex = index
        elif line.strip() == END_TOKEN:
            endIndex = index
            break

    if startIndex > -1:
        message = ''.join(lines[startIndex:endIndex+1])
    else:
        message = "No Profile in " + hosts_file
        log_type = 'info'

    exit_with_message(message, log_type)

def list():

    message = []
    log_type = 'default' 
    if len(profiles) == 0:
        message.append("Currently No Profile Available")
        log_type = 'info'
    else:
        for profile in profiles:
            message.append( "  " +profile )
        message.insert(0, "Available Profiles:")

    message = "\n".join(message)
    exit_with_message(message, log_type)

def check(profile = False):

    if profile != False:
        return profiles.has_key(profile)
    else:
        return False

def info(profile = False):
    message = []
    log_type = 'default'
    if profile != False:
        if check(profile) != False:
            message.append("Profile: \"" + profile + "\"\n")
            message.append("---------------------------------\n")
            file = open(profiles[profile], "r")
            lines = file.readlines()
            for line in lines:
                message.append(line)

            message.append("---------------------------------\n")
            message.append("Path: " + profiles[profile])
        else:
            message.append("Oops... Profile: \"" + profile + "\" Not Found...")
            log_type = 'warn'
    else:
        message.append(str(len(profiles)) + " profile" + ("s" if len(profiles)>1 else ""))
        log_type = 'info'

    message = ''.join(message) 
    exit_with_message(message, log_type)

def rm(profile = False):

    message = []
    log_type = 'default'
    if check(profile):
        try:
            op = raw_input("Type Y to Remove \""+ profile +"\" Profile: ")
            if op == "Y" or op == "y":
                os.remove(profiles[profile])
                message.append('Remove Successfully!')
                log_type = 'info'
        except KeyboardInterrupt:
            message.append("")        
    else:
        message.append("Please Enter a valid profile")
        log_type = 'warn'

    message = ''.join(message)
    exit_with_message(message, log_type)

def host():
    os.system('cat ' + hosts_file)
    exit_with_message()

def add(profile = False):

    if profile == False or check(profile):
        exit_with_message('profile name is null or already exist.', 'warn')
    else:
        subprocess.call(['vi', hostie_dirs[1] + profile])

def edit(profile = False):

    if profile != False:
        if check(profile):
            subprocess.call(['vi', profiles[profile]])
        else:
            exit_with_message( "Oops... Profile: \"" + profile + "\" Not Found...", "warn")
    else:
        subprocess.call(['vi', hosts_file])
    exit_with_message()

def privilege():
    return True if getpass.getuser() == "root" else False

def help():
    message = ['Usage:']
    message.append('Require Root Privilege')
    message.append('  sudo hostie [profile]\t\t\t# Quickly switch host')
    message.append('  sudo hostie reset \t\t\t# Reset hostfile to the original\n')

    message.append('  hostie show \t\t\t\t# Show your current profile')
    message.append('  hostie host \t\t\t\t# Show system host \n')

    message.append('  hostie list \t\t\t\t# List your hostie profiles')
    message.append('  hostie add  [profile] \t\t# Add a profile to your profiles list')
    message.append('  hostie info [profile] \t\t# Display infomation about profile')
    message.append('  hostie edit [profile] \t\t# Edit ...')
    message.append('  hostie rm   [profile] \t\t# Remove ...\n')
    message.append('See More in README.md about How to ...')

    exit_with_message('\n'.join(message))    

def main():

    if len(sys.argv) < 2:
        help()

    fn_map = {
        '__default__': write,

        'help': help,
        
        's': show,
        'show': show,

        'l': list,
        'list': list,

        'h': host,
        'host': host,

        'e': edit,
        'edit': edit,

        'add': add,

        'r': reset,
        'reset': reset,
        
        'i': info,
        'info': info,

        'flush': flush,

        'rm': rm
    }        

    if len(profiles) == 0:
        print(colorful("Maybe You Need Create A Profile First.", 'warn'))
     
    if sys.argv[1] in fn_map:
        if len(sys.argv) > 2:
            fn_map[sys.argv[1]](sys.argv[2])
        else:
            fn_map[sys.argv[1]]()
    else:
        fn_map['__default__'](sys.argv[1])

if __name__ == "__main__":
    main()
