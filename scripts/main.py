#!/usr/bin/env python
    
import sys
import getpass
import os
from os import path

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

def exit_with_message(message):
    print(message)
    exit(1)

def flush():
    try:
        os.system('killall -HUP mDNSResponder')
    except:
        exit_with_message("You need Refresh DNS Cache")

def write(profile):

    if profiles.has_key(profile) == False:
        exit_with_message( "Oops! Profile: \"" + profile + "\" Not Found...")

    file = profiles[profile]

    if os.path.exists(file) == False:
        exit_with_message( "Oops! \"" + file + "\" Not Found...")

    try:
        file = open(file)

        lines = file.readlines()
        hosts_file_handle = reset(True)

        hosts_file_handle.writelines(START_TOKEN + "\n")
        for line in lines:
            hosts_file_handle.writelines(line)

        hosts_file_handle.writelines("\n################# current profile: `" + profile + '`\n')
        hosts_file_handle.writelines(END_TOKEN + "\n")

        close(file)
        close(hosts_file_handle)
        flush()
        
        exit_with_message( "`" + profile +"` Profile Added in /etc/hosts.")
    except Exception, e:
        exit_with_message("Error...") 

def reset(type):
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
        exit_with_message('Reset Successfully.')

def close(file):
    file.close()

def show():

    hosts_file_handle = open(hosts_file, "r")
    lines = hosts_file_handle.readlines()
    startIndex = -1
    endIndex   = -1
    
    for index, line in enumerate(lines):
        if line.strip() == START_TOKEN:
            startIndex = index
        elif line.strip() == END_TOKEN:
            endIndex = index
            break

    message = ''.join(lines[startIndex:endIndex+1]) if startIndex > -1 else "No Profile in \"/etc/hosts\"."            
    exit_with_message(message)    

def list():

    message = []    
    if len(profiles) == 0:
        message.append("Currently No Profile Available")
    else:
        for profile in profiles:
            message.append( "  " +profile )
        message.insert(0, "Available Profiles:")

    message = "\n".join(message)
    exit_with_message(message)

def info(profile):
    message = []
    if profile != False:
        if profiles.has_key(profile) == False:
            message.append("Oops! Profile: \"" + profile + "\" Not Found...")
        else:
            message.append("Profile: \"" + profile + "\"\n")
            message.append("---------------------------------\n")
            file = open(profiles[profile], "r")
            lines = file.readlines()
            for line in lines:
                message.append(line)

            message.append("---------------------------------\n")
            message.append("Path: " + profiles[profile])
    else:
        message.append(str(len(profiles)) + " profile" + ("s" if len(profiles)>1 else ""))

    message = ''.join(message) 
    exit_with_message(message)

def main():

    if len(sys.argv) < 2:
        exit_with_message("Usage: sudo hostie [profile|reset|show|list|info]\nSee More in `README.md` about How to ...")

    if len(profiles) == 0:
        print("Maybe You Need Create A Profile First.")     

    if sys.argv[1] == 'show':
        show()

    elif sys.argv[1] == 'list': 
        list()

    elif sys.argv[1] == 'info':
        if len(sys.argv) > 2:
            info(sys.argv[2])
        else:
            info(False)

    elif getpass.getuser() != "root": 
        exit_with_message("Oops... Please run it as *root* user.")

    if(sys.argv[1] == 'reset'):
        reset(False)
    else:
        write(sys.argv[1])

if __name__ == "__main__":
    main()
