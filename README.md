# hostie

Switch hosts by Using Command Line

## Installation
    
    $ git clone git@github.com:yleo77/hostie.git

## Quick Start

### Setting

Put your custom hosts file in this dir: `~/.config/hostie`, and remeber the filename.
    
### Usage
    
Before you use it , make sure it is executable.

#### Add your custom host file to `/etc/hosts`

    # azure is your created host file name in `~/.config/hostie`
    $ sudo hostie azure 

#### Reset your hosts file.

    # reset your hosts file to the original
    $ sudo hostie reset  

#### Show your current config.

    $ hostie show  

#### List your hostie Profile in ~/.config/hostie.

    $ hostie list          

Maybe you could alias a command like this:

    alias h="sudo _REPO_DIR_/hostie".


## TODO

    
