import codecs
import os
from xml.dom import minidom
import shutil
import xml.etree.ElementTree as ET
def _serialize_xml(write, elem, encoding, qnames, namespaces):
    tag = elem.tag
    text = elem.text
    if tag is ET.Comment:
        write("<!--%s-->" % ET._encode(text, encoding))
    elif tag is ET.ProcessingInstruction:
        write("<?%s?>" % ET._encode(text, encoding))
    else:
        tag = qnames[tag]
        if tag is None:
            if text:
                write(ET._escape_cdata(text, encoding))
            for e in elem:
                _serialize_xml(write, e, encoding, qnames, None)
        else:
            write("<" + tag)
            items = elem.items()
            if items or namespaces:
                if namespaces:
                    for v, k in sorted(namespaces.items(),
                                       key=lambda x: x[1]):  # sort on prefix
                        if k:
                            k = ":" + k
                        write(" xmlns%s=\"%s\"" % (
                            k.encode(encoding),
                            ET._escape_attrib(v, encoding)
                            ))
                #for k, v in sorted(items):  # lexical order
                for k, v in items: # Monkey patch
                    if isinstance(k, ET.QName):
                        k = k.text
                    if isinstance(v, ET.QName):
                        v = qnames[v.text]
                    else:
                        v = ET._escape_attrib(v, encoding)
                    write(" %s=\"%s\"" % (qnames[k], v))
            if text or len(elem):
                write(">")
                if text:
                    write(ET._escape_cdata(text, encoding))
                for e in elem:
                    _serialize_xml(write, e, encoding, qnames, None)
                write("</" + tag + ">")
            else:
                write(" />")
    if elem.tail:
        write(ET._escape_cdata(elem.tail, encoding))

ET._serialize_xml = _serialize_xml

from collections import OrderedDict

class OrderedXMLTreeBuilder(ET.XMLTreeBuilder):
    def _start_list(self, tag, attrib_in):
        fixname = self._fixname
        tag = fixname(tag)
        attrib = OrderedDict()
        if attrib_in:
            for i in range(0, len(attrib_in), 2):
                attrib[fixname(attrib_in[i])] = self._fixtext(attrib_in[i+1])
        return self._target.start(tag, attrib)


PME_path1 = 'C:/Program Files (x86)/Schneider Electric/Power Monitoring Expert/system/translators'
PME_path2 = 'C:/Program Files (x86)/Schneider Electric/Power Monitoring Expert/config/translators'

PME_file1 = 'C:/Program Files (x86)/Schneider Electric/Power Monitoring Expert/system/translators/pm5300.xml'
PME_file2 = 'C:/Program Files (x86)/Schneider Electric/Power Monitoring Expert/config/translators/pm5300.xml'
PME_ion1 = 'C:/Program Files (x86)/Schneider Electric/Power Monitoring Expert/system/translators/pm5300.ion'
PME_ion2 = 'C:/Program Files (x86)/Schneider Electric/Power Monitoring Expert/config/translators/pm5300.ion'

#copying the file to local desktop
Des = os.getcwd()
Des_name = os.getcwd() + '\pm5300.xml'
Des_rename = os.getcwd() + '\pm5300_CustNumber.xml'
Des_ion = os.getcwd() +'\pm5300.ion'
Des_ion_rename = os.getcwd() + '\pm5300_CustNumber.ion'

#backup the xml file in system->translators
shutil.copy2(PME_file1 , Des)
os.rename(Des_name,Des_rename)
shutil.copy2(Des_rename , PME_path1)

#backup the ion file in system translators
shutil.copy2(PME_ion1 , Des)
os.rename(Des_ion,Des_ion_rename)
shutil.copy2(Des_ion_rename , PME_path1)

#now shutting down the SITE service of the program
###############

#Replacing the existing ION file with the new MODBUS address

tree = ET.parse(PME_file1, OrderedXMLTreeBuilder())
root = tree.getroot()
for idx,node in enumerate(root):
    if len(node.attrib.values()) > 2:
        if node.attrib.values()[2] == '408906':
            node.set("ModbusAddress","402401")
            print node.attrib.values()[2]


ET.register_namespace("", "x-schema:modbus-schema.xml")
# # print(tree.findall(.//ModbusInfo/..[@ModbusAddress='408906']))

tree.write(PME_file1,encoding = "utf-8", xml_declaration=True)
os.remove(Des_rename)
os.remove(Des_ion_rename)

# #now process the file for identation (NOTEPAD support)
f = open(PME_file1,'r')
p = open(PME_path1 + '/pm5300_back.xml','w')
num_lines = sum(1 for line in open(PME_file1))
print(num_lines)
i=1
while(i<=num_lines):
    print >> p , f.readline()
    i=i+1
    
f.close()
p.close()

#trying to read that file in codecs and remove the extra spaces
f = codecs.open(PME_path1 + '/pm5300_back.xml','r','utf-8')
p = codecs.open(PME_path1 + '/pm5300_back_back.xml','w','utf-8')
    
    
num_lines = sum(1 for line in open(PME_path1 + '/pm5300_back.xml'))
print(num_lines)
i=1
while(i<=num_lines):
    a = f.readline()
    if not [ord(c.decode('utf-8')) for c in a] == [13,10]:
        # print([ord(c.decode('utf-8')) for c in a])
        print >> p , a
    i = i+1
    
f.close()
p.close()   
os.remove(PME_path1 + '/pm5300_back.xml')
os.remove(PME_file1)
prevName = PME_path1 + '/pm5300_back_back.xml'
newName = PME_file1
os.rename(prevName , newName )

#now remove the files from the destination
#os.remove(Des_rename)
#os.remove(Des_ion_rename)


# doing the replacing in config- translator

if os.path.exists(PME_file2) == True:
    print("found file")
    #taking a backup of the xml file there
    shutil.copy2(PME_file2 , Des)
    os.rename(Des_name,Des_rename)
    shutil.copy2(Des_rename , PME_path2)

    #taking a backup of the ion file there
    shutil.copy2(PME_ion2 , Des)
    os.rename(Des_ion,Des_ion_rename)
    shutil.copy2(Des_ion_rename , PME_path2)

    tree = ET.parse(PME_file2, OrderedXMLTreeBuilder())
    root = tree.getroot()
    for idx,node in enumerate(root):
        if len(node.attrib.values()) > 2:
            if node.attrib.values()[2] == '408906':
                node.set("ModbusAddress","402401")
                print node.attrib.values()[2]
    ET.register_namespace("", "x-schema:modbus-schema.xml")
    # print(tree.findall(.//ModbusInfo/..[@ModbusAddress='408906']))
    tree.write(PME_file2,encoding = "utf-8", xml_declaration=True)

    #now process the file for identation (NOTEPAD support)
    f = open(PME_file2,'r')
    p = open(PME_path2 + '/pm5300_back.xml','w')
    num_lines = sum(1 for line in open(PME_file2))
    print(num_lines)
    i=1
    while(i<=num_lines):
        print >> p , f.readline()
        i=i+1
    
    f.close()
    p.close()

    #trying to read that file in codecs and remove the extra spaces
    f = codecs.open(PME_path2 + '/pm5300_back.xml','r','utf-8')
    p = codecs.open(PME_path2 + '/pm5300_back_back.xml','w','utf-8')
    
    
    num_lines = sum(1 for line in open(PME_path2 + '/pm5300_back.xml'))
    print(num_lines)
    i=1
    while(i<=num_lines):
        a = f.readline()
        if not [ord(c.decode('utf-8')) for c in a] == [13,10]:
            # print([ord(c.decode('utf-8')) for c in a])
            print >> p , a
    	i = i+1
    
    f.close()
    p.close()   
    os.remove(PME_path2 + '/pm5300_back.xml')
    os.remove(PME_file2)
    prevName = PME_path2 + '/pm5300_back_back.xml'
    newName = PME_file2
    os.rename(prevName , newName )
    
    
    os.remove(Des_rename)
    os.remove(Des_ion_rename)
    exit()

else:
    exit()










    
        
            
            







