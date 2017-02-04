import codecs
import os
import shutil
import xml.etree.ElementTree as ET
#calling the dependencies required for parsing the XML without the attribute sorting function
from Packages import *

#parsing the xml file and wrting the file into XML folder
tree = ET.parse(os.getcwd() + '\XMLfiles\pm5300masterFile.xml', OrderedXMLTreeBuilder())
root = tree.getroot()
for idx,node in enumerate(root):
    if len(node.attrib.values()) > 2:
        if node.attrib.values()[2] == '408906':
            node.set("ModbusAddress","408905")
            print node.attrib.values()[2]


ET.register_namespace("", "x-schema:modbus-schema.xml")
# # print(tree.findall(.//ModbusInfo/..[@ModbusAddress='408906']))

tree.write(os.getcwd() + '\XMLfiles\PM5300.xml',encoding = "utf-8")

# i have implemented by own version of a xml formatter

f = open(os.getcwd() + '\XMLfiles\PM5300.xml')
p = open(os.getcwd() + '\XMLfiles\PM5300_back.xml','w')

num_lines = sum(1 for line in open(os.getcwd() + '\XMLfiles\PM5300.xml'))

i=1
while(i<=num_lines):
	print >> p , f.readline()
	i=i+1

f.close()
p.close()













    
        
            
            







