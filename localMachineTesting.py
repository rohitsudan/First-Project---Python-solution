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

tree.write(os.getcwd() + '\XMLfiles\PM5300.xml',encoding = "utf-8", xml_declaration=True,default_namespace="xmlns",method="xml")










    
        
            
            







