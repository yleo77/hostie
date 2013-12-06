#!/usr/bin/env python

import re

def colorful(message = '', type = 'default'):

    template = {
        'info': '\033[32m[INFO] {{msg}} \033[0m',
        'error': '\033[31m[ERROR] {{msg}} \033[0m',
        'warn': '\033[33m[WARN] {{msg}} \033[0m',
        'default': '{{msg}}'
    }
    if template.has_key(type) == False:
        type = 'default'

    return re.sub('{{msg}}', message, template[type])