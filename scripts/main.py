#!/usr/bin/env python
    
import sys
import getpass
import os
from os import path

hosts_file = "/etc/hosts"
hostie_dirs = path.expanduser(path.join("~", ".config/hostie")) + '/'

START_TOKEN = "################# added by hostie"
END_TOKEN   = "################# end of hostie"

def exit_with_message(message):
    print(message)
    exit(1)

def flush():
    try:
        os.system('killall -HUP mDNSResponder')
    except:
        exit_with_message("you need refresh dns cache")

def write(profile):

    file = hostie_dirs + profile

    if os.path.exists(file) == False:
        exit_with_message( "Oops! \"" + file + "\" Not Found...")

    try:
        file = open(file)

        lines = file.readlines()
        hosts_file_handle = reset(True)

        hosts_file_handle.writelines(START_TOKEN + '\n')
        for line in lines:
            hosts_file_handle.writelines(line)
        hosts_file_handle.writelines(END_TOKEN + '\n')

        close(file)
        close(hosts_file_handle)
        flush()
        
        exit_with_message(" Set Successfully...")        
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
    for file in os.listdir(hostie_dirs):
        message.append(file)

    if len(message) == 0:
        message.append("Currently No Profile Available")
    else:
        message.insert(0, "############ hostie Profile List")
        message.append("############ hostie Profile List")

    message = "\n".join(message)
    exit_with_message(message)

def main():

    if os.path.exists(hostie_dirs) == False:
        exit_with_message("You need checkout `README.md` first.")

    elif len(sys.argv) != 2:
        exit_with_message("Usage: sudo hostie [argv|reset|show|list]")

    elif sys.argv[1] == 'show':
        show()

    elif sys.argv[1] == 'list': 
        list()

    elif getpass.getuser() != "root": 
        exit_with_message("Oops... Please run it as *root* user.")

    if(sys.argv[1] == 'reset'):
        reset(False)
    else:
        write(sys.argv[1])

if __name__ == "__main__":
    main()
