#!/usr/bin/env python

from bcolors import bcolors
from sysadmin.myshell import run


class Cluster(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        """
        Human friendly representation of this Cluster
        """
        out = ""
        out += '\n' + bcolors.WARNING + 'cluster name:     ' + bcolors.ENDC + self.name
        hosts = self.hosts
        if hosts[0].location.category == "Domain":
            out += '\n' + bcolors.WARNING + 'domain:           ' + bcolors.ENDC + hosts[0].location.name
        if hosts[0].location.category == "Sandbox":
            out += '\n' + bcolors.WARNING + 'sandbox:          ' + bcolors.ENDC + hosts[0].location.name
        out += '\n' + bcolors.WARNING + 'Hosts             ' + bcolors.ENDC + hosts[0].name
        for host in hosts[1:]:
            out += '\n' + '                  ' + host.name
        out += "\n"
        return out

    @property
    def hosts(self):
        """
        return the list of Host (as a HostList) included in this Cluster
        """
        from myaq.host import Host, HostList
        cmd = "/opt/aquilon/bin/aq.py search_host --cluster %s" %self.name
        results = run(cmd)
        # FIXME
        # check rt == 0, otherwise raise an Exception
        hostlist = HostList()
        for name in results.out.split():
            host = Host(name)
            hostlist.append(host)
        return hostlist

    def add_host(self, host):
        cmd = "/opt/aquilon/bin/aq.py cluster --hostname %s --cluster %s" %(host.name, self.name)
        results = run(cmd)
        self.info = results.out
        return self.info

    def remove_host(self, host):
        cmd = "/opt/aquilon/bin/aq.py uncluster --hostname %s --cluster %s" %(host.name, self.name)
        results = run(cmd)
        self.info = results.out
        return self.info

    def remove(self):
        """
        delete this cluster
        """
        cmd = "/opt/aquilon/bin/aq.py del_cluster --cluster %s" %self.name
        results = run(cmd)
        return results

