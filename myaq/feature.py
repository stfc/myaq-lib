#!/usr/bin/env python

from bcolors import bcolors
from sysadmin.myshell import run
from myaq.personality import Personality, PersonalityList

# ============================================================================== 
# NOTE: this class is under development / to be tested
# ============================================================================== 
class FeatureHandler(object):
    """
    class to create and remove Features
    """
    def create(self, name):
        cmd = '/opt/aquilon/bin/aq.py add_feature --feature %s --type host' %name
        results = run(cmd)
        if results.rc == 0:
            feature = Feature(name)
            return feture
        else:
            return None

    def remove(self, feature):
        """
        removes a Feature
        """
        cmd = '/opt/aquilon/bin/aq.py del_feature --feature %s --type host' %self.feature.name
        results = run(cmd)
        return results
        

class Feature(object):
    def __init__(self, name):
        self.name = name 
        self.info = None

    def __str__(self):
        """
        Human friendly representation of this Feature
        """
        template = self.template
        personalities = self.personalities

        out = bcolors.WARNING + 'name:                ' + bcolors.ENDC + self.name
        out += '\n' + bcolors.WARNING + 'template:            ' + bcolors.ENDC + template
        if personalities:
            out += '\n' + bcolors.WARNING + 'personalities:       ' + bcolors.ENDC + personalities[0].name
            for personality in personalities[1:]:
                out += '\n' + '                     ' + personality.name
        else:
            out += '\n' + bcolors.WARNING + 'personalities:       ' + bcolors.ENDC
        out += '\n'
        return out

    def _show_feature(self):
        cmd = "/opt/aquilon/bin/aq.py show_feature --feature %s --type host" %self.name
        results = run(cmd)
        self.info = results.out
        return self.info

    @property
    def exists(self):
        """
        checks if the Feature actually exists in Aquilon or not
        """
        cmd = "/opt/aquilon/bin/aq.py show_feature --feature %s --type host" %self.name
        r = run(cmd)
        return r.rc == 0

    @property
    def template(self):
        if not self.info:
            self._show_feature()
        for line in self.info.split('\n'):
            if 'Template' in line:
                # FIXME !! use class Template
                template = line.split(':')[1].strip()
                return template

    @property
    def personalities(self):
        """
        gets the Personalities binding this Feature
        """
        if not self.info:
            self._show_feature()
        personalities = PersonalityList()
        for line in self.info.split('\n'):
            line = line.strip()
            if line.startswith('Bound to'):
                personality_name = line.split('/')[-1]
                p = Personality(personality_name)
                personalities.append(p)
        return personalities

    def create(self):
        """
        create this Feature
        """
        cmd = '/opt/aquilon/bin/aq.py add_feature --feature %s --type host' %self.name
        results = run(cmd)
        return results

    def remove(self):
        """
        remove this Feature
        """
        cmd = '/opt/aquilon/bin/aq.py del_feature --feature %s --type host' %self.name
        results = run(cmd)
        return results


class FeatureList(list):

    def __str__(self):
        out = ""
        for f in self.__iter__():
            out += str(f)
            out += '\n'
        return out

    def set(self, name_l):
        if name_l:
            # just in case a client calls this method with value None
            for name in name_l:
                self.append(Feature(name))

    def create(self):
        for feature in self.__iter__():
            feature.create()

    def remove(self):
        for feature in self.__iter__():
            feature.remove()

