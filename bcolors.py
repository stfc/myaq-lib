#!/usr/bin/env python


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def colorprint(*msg_l):
    """
    items n msg_l are either tuples or strings.
    For each tuple:
        1. First field is the text
        2. Second field, if existing, is the color code.
    """
    out = ''
    for i in msg_l:
        if type(i) is tuple:
            msg, code = i
            out += code + str(msg) + bcolors.ENDC + " "
        else:
            out += i + " "
    out = out.strip()
    print(out)

def printerror(msg):
    colorprint((msg, bcolors.FAIL))

def printwarning(msg):
    colorprint((msg, bcolors.WARNING))
