#
# Reads the xml recipies outputted from beersmith
#

import sys
from xml.dom import minidom

class XmlParse():
    def __init__(self):
        self.path = "no_path"
        self.grain_weight = 0
    
    def read_xml(self, path):
        
        self.path = path
        self.xmlFile = minidom.parse(self.path)

    def parse_xml(self):
        for fermentables in self.xmlFile.getElementsByTagName('FERMENTABLES'):
            for kg in fermentables.getElementsByTagName('AMOUNT'):
                self.grain_weight += (float(kg.firstChild.toxml())*2.20462)
        return self.grain_weight
