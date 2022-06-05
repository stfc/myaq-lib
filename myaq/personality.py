#!/usr/bin/env python

from bcolors import bcolors
from sysadmin.myshell import run

from myaq.archetype import Archetype


# ============================================================================== 
# NOTE: this class is under development / to be tested
# ============================================================================== 
class PersonalityHandler(object):
    """
    class to create and destroy Personality objects
    """
    def __init__(self):
        self.eon_id = 15 # DCIG by default

    def create(self, name):
        if '/' in name:
            archetypename, name = name.split('/')
            name = name
            archetype = Archetype(archetypename)
        else:
            name = name
            archetype = Archetype('ral-tier1')

        cmd = "/opt/aquilon/bin/aq.py add_personality --personality %s --archetype %s --eon_id %s" %(name, archetype.name, self.eon_id)
        results = run(cmd)
        if results.rc == 0:
            personality = Personality(name)
            return personality
        else:
            return None

    def remove(self, personality):
        """
        remove the Personality
        """
        name = personality.name
        archetype = personality.archetype
        cmd = "/opt/aquilon/bin/aq.py del_personality --personality %s --archetype %s" %(name, archetype.name)
        results = run(cmd)
        self.info = results.out
        return self.info

    def clone(self, personality, name):
        """
        clone existing Personality "personality" into a new one with name "name"
        """
        new_personality = self.create(name)
        new_personality.copy_features(personality)
        return new_personality
        

class Personality(object):
    def __init__(self, name):
        if '/' in name:
            archetypename, name = name.split('/')
            self.name = name
            self.archetype = Archetype(archetypename)
        else:
            self.name = name
            self.archetype = Archetype('ral-tier1')
        self.info = None
        self.eon_id = 15 # DCIG by default

    def __str__(self):
        """
        Human friendly representation of this Personality
        """
        out = ""
        out += '\n' + bcolors.WARNING + 'personality: ' + bcolors.ENDC + self.name
        out += '\n' + bcolors.WARNING + 'archetype:   ' + bcolors.ENDC + self.archetype.name
        out += '\n' + bcolors.WARNING + 'owner:       ' + bcolors.ENDC + self.owner
        if len(self.features):
            out += '\n' + bcolors.WARNING + 'features:    ' + bcolors.ENDC + self.features[0].name
            for feature in self.features[1:]:
                out += '\n' + '             ' + feature.name
        else:
            out += '\n' + bcolors.WARNING + 'features:       ' + bcolors.ENDC
        if len(self.hosts):
            out += '\n' + bcolors.WARNING + 'hosts:       ' + bcolors.ENDC + self.hosts[0].name
            for host in self.hosts[1:]:
                out += '\n' + '             ' + host.name
        else:
            out += '\n' + bcolors.WARNING + 'hosts:       ' + bcolors.ENDC
        return out

    def _show_personality(self):
        cmd = "/opt/aquilon/bin/aq.py show_personality --personality %s" %self.name
        results = run(cmd)
        self.info = results.out
        return self.info

    @property
    def features(self):
        """
        get the Features bound to this Personality
        """
        from myaq.feature import Feature
        if not self.info:
            self._show_personality()
        out = []
        for line in self.info.split('\n'):
            if 'Host Feature' in line:
                featurename = line.split()[2]
                feature = Feature(featurename)
                out.append(feature)
        return out

    @property
    def hosts(self):
        """
        get the list of hosts bound to this personality
        """
        from myaq.host import Host, HostList
        cmd = 'aq search_host --personality %s' %self.name
        results = run(cmd)
        # FIXME
        # check rt == 0, otherwise raise an Exception
        hostlist = HostList()
        for name in results.out.split():
            host = Host(name)
            hostlist.append(host)
        return hostlist

    #@property 
    #def archetype(self):
    #    """
    #    get the archetype str for this Personality
    #    """
    #    if not self.info:
    #        self._show_personality()
    #    for line in self.info.split('\n'):
    #        if 'Archetype' in line:
    #            archetype_name = line.split()[-1].strip()
    #            return Archetype(archetype_name)

    @property 
    def owner(self):
        """
        get the owner str for this Personality
        """
        if not self.info:
            self._show_personality()
        for line in self.info.split('\n'):
            if 'Owned by GRN' in line:
                owner = line.split(':')[1].strip()
                return owner 

    def create(self):
        """
        create the Personality.
        Assume archetype is 'ral-tier1'
        """
        cmd = "/opt/aquilon/bin/aq.py add_personality --personality %s --archetype %s --eon_id %s" %(self.name, self.archetype.name, self.eon_id)
        results = run(cmd)
        self.info = results.out
        return self.info

    def remove(self):
        """
        remove the Personality
        """
        cmd = "/opt/aquilon/bin/aq.py del_personality --personality %s --archetype %s" %(self.name, self.archetype.name)
        results = run(cmd)
        self.info = results.out
        return self.info

    def copy_features(self, source):
        """
        makes this Personality to be a copy from another one.
        Assume archetype is 'ral-tier1'
        :param Personality source: personality to copy from
        """
        #self.info = None # just in case
        #cmd = "/opt/aquilon/bin/aq.py add_personality --personality %s --archetype %s --eon_id %s --copy_from %s" %(self.name, self.archetype.name, self.eon_id, source.name)
        #results = run(cmd)
        #self.info = results.out
        #return results
        feature_list = source.features
        self.bind(feature_list)

    def bind(self, feature_l):
        """
        bind a list of Features to this Personality
        """
        results = []
        for feature in feature_l:
            r = self.bind_feature(feature)
            results.append(r)
        return results

    def bind_feature(self, feature):
        """
        bind a single Feature to this Personality
        """
        cmd = 'aq bind_feature --personality %s --feature %s --justification tcm=00000' %(self.name, feature.name)
        results = run(cmd)
        self.info = results.out
        return results

    def unbind(self, feature_l):
        """
        unbind a list of Features to this Personality
        """
        results = []
        for feature in feature_l:
            r = self.unbind_feature(feature)
            results.append(r)
        return results

    def unbind_feature(self, feature):
        """
        unbind a single Feature to this Personality
        """
        cmd = 'aq unbind_feature --personality %s --feature %s --justification tcm=00000' %(self.name, feature.name)
        results = run(cmd)
        self.info = results.out
        return results


class PersonalityList(list):

    def __str__(self):
        out = ""
        for p in self.__iter__():
            out += str(p)
            out += '\n'
        return out

    @property
    def hosts(self):
        from myaq.host import HostList 
        host_l = HostList()
        for personality in self.__iter__():
            host_l += personality.hosts
        return host_l

    def set(self, name_l):
        for name in name_l:
            self.append(Personality(name))

    def create(self):
        for personality in self.__iter__():
            personality.create()

    def bind(self, feature_l):
        for personality in self.__iter__():
            personality.bind(feature_l)

    def bind_feature(self, feature):
        for personality in self.__iter__():
            personality.bind_feature(feature)

    def unbind(self, feature_l):
        for personality in self.__iter__():
            personality.unbind(feature_l)

    def unbind_feature(self, feature):
        for personality in self.__iter__():
            personality.unbind_feature(feature)

