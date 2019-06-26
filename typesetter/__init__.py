#!/usr/bin/env python3


import sys
import subprocess


def typeset(file: str) -> bool:
    try:
        subprocess.Popen()
        return True
    except Exception as e:
        sys.stderr.write(str(e) + '\n')
        return False


def run(args: list) -> None:
    pass
