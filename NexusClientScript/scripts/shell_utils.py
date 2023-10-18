#!/bin/python3

import subprocess

class Shell:
    @staticmethod
    def readlink(filepath):
        readlink_cmd = "readlink -f {}".format(filepath)
        readlink_prc = subprocess.run([readlink_cmd], shell=True, stdout=subprocess.PIPE)
        readlink_out = readlink_prc.stdout.decode('utf-8').strip()
        return readlink_out 

