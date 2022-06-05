#!/usr/bin/env python

import subprocess

class Results(object):
    def __init__(self, cmd, out, err, rc):
        self.cmd = cmd
        self.out = out
        self.err = err
        self.rc = rc

    @property
    def succeeded(self):
        return self.out == 0

    @property 
    def faled(self):
        return not self.succeeded

def run(cmd):
    try:
        # python 3
        subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    except:
        # python 2
        subproc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = subproc.communicate()
    st = subproc.returncode
    results = Results(cmd, out.strip(), err.strip(), st)
    return results


def remote_run(cmd, host, user='root'):
    cmd = "ssh -oStrictHostKeyChecking=no -oCheckHostIP=no %s@%s '%s'" %(user, host, cmd)
    return run(cmd)


def call(cmd):
    subprocess.call(cmd, shell=True)


def scpto(source_dir='./', source='*', user='root', dest_host='', dest_dir='/tmp/'):
    """
    copy, with scp, one or more files from localhost to a remote host
    """
    # FIXME
    if not dest_host:
        # abort
        return None
    cmd = 'scp %s/%s %s@%s:%s' %(source_dir, source, user, dest_host, dest_dir)
    results = run(cmd)
    return results


def scpfrom(user='root', source_host='', source_dir='/tmp/', source='*', dest_dir='/tmp/'):
    """
    copy, with scp, one or more files from a remote host to localhost
    """
    # FIXME
    if not source_host:
        # abort
        return None
    cmd = 'scp %s@%s:%s/%s %s' %(user, source_host, source_dir, source, dest_dir)
    results = run(cmd)
    return results


