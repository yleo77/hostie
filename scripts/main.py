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

def write(file):

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

def reset(type):
    hosts_file_handle = open(hosts_file, "r+")
    lines = hosts_file_handle.readlines()
    startIndex = -1
    endIndex   = -1
    
    for index, line in enumerate(lines):
        if line.strip() == START_TOKEN:
            startIndex = index
        if line.strip() == END_TOKEN:
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

def close(file):
    file.close()

def main():

    if os.path.exists(hostie_dirs) == False:
        exit_with_message("You need checkout `README.md` first.")

    if len(sys.argv) != 2:
        exit_with_message("Usage: sudo hostie [argv|reset]")

    if getpass.getuser() != "root": 
        exit_with_message(" Oops... Please run it as *root* user.")

    if(sys.argv[1] == 'reset'):
        reset(False)
        exit_with_message("Reset Successfully.")

    filename = hostie_dirs + sys.argv[1]

    if os.path.exists(filename):
        write(filename)
    else:
        exit_with_message( " Oops! " + filename + "Not Found...")


if __name__ == "__main__":
    main()
