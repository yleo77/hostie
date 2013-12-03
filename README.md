# hostie

Switch hosts by Using Command Line

## Installation
    
    $ git clone git@github.com:yleo77/hostie.git

## Quick Start

### Setting

Put your custom hosts file in this dir: `_REPO_DIR_/profiles`, and remeber the filename. (Of course, `~/.config/hostie/` also works.)
    
### Usage
    
Before you use it , make sure it is executable.

#### Add your custom host file to `/etc/hosts`.

    # azure is your created host file name in `_REPO_DIR_/profiles`
    $ sudo hostie azure 

#### Reset your hosts file.

    # reset your hosts file to the original
    $ sudo hostie reset  

#### Show your current profile.

    $ hostie show  

#### List your hostie profiles.

    $ hostie list          

#### Display infomation about profile

    $ hostie info [profile]
    
Maybe you could alias a command like this:

    alias h="sudo _REPO_DIR_/hostie".


## TODO

    
