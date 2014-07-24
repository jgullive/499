#
# Reads the xml recipies outputted from beersmith
#

import sys
from xml.dom import minidom

class XmlParse():
    def __init__(self):
        self.path = "no_path"
        self.grain_weight = 0
        self.hops = []
    
    def read_xml(self, path):
        
        self.path = path
        self.xmlFile = minidom.parse(self.path)

    def parse_xml(self, recipe_profile):

        # Boil length
        for boil_time in self.xmlFile.getElementsByTagName('BOIL_TIME'):
            recipe_profile.boil_time = boil_time.firstChild.toxml()

        # Fermentable data
        for fermentables in self.xmlFile.getElementsByTagName('FERMENTABLES'):
            for kg in fermentables.getElementsByTagName('AMOUNT'):
                self.grain_weight += (float(kg.firstChild.toxml())*2.20462)
        recipe_profile.grain_weight =  self.grain_weight

        # Mash data
        # Note that there is currently no support for a multi-step mash
        for step_time in self.xmlFile.getElementsByTagName('STEP_TIME'):
            recipe_profile.mash_time = step_time.firstChild.toxml()
        for step_temp in self.xmlFile.getElementsByTagName('STEP_TEMP'):
            recipe_profile.mash_temp = float(step_temp.firstChild.toxml())*9/5 + 32
        for sparge_temp in self.xmlFile.getElementsByTagName('SPARGE_TEMP'):
            recipe_profile.lauter_temp = float(sparge_temp.firstChild.toxml())*9/5 + 32

        # Hop data
        for hops in self.xmlFile.getElementsByTagName('HOPS'):
            for time in hops.getElementsByTagName('TIME'):
                self.hops.append(float(time.firstChild.toxml()))
        self.hops.sort(reverse = True)
        length = len(self.hops)

        if length >= 1:
            recipe_profile.hops1 = self.hops[0]
        if length >= 2:
            recipe_profile.hops2 = self.hops[1]
        if length >= 3:
            recipe_profile.hops3 = self.hops[2]
        if length >= 4:
            recipe_profile.hops4 = self.hops[3]

