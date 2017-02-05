# this code here is written for learning about classes
# learnt from https://www.youtube.com/watch?v=ZDa-Z5JzLYM

# a simple employee class

# class Employee:
# 	pass # pass is put to skip the class for now
# 	def __init__(self,first_name,last_name,pay):
# 		self.first_name = first_name
# 		self.last_name = last_name
# 		self.pay = pay
# 		self.email = first_name + '.' + last_name + '@company.com'



# emp_1 = Employee('Corey','Scfner',50000)
# emp_2 = Employee('rohit','sudan',70000)


# print(emp_1.email)
# print(emp_2.email)

import xml.etree.ElementTree as ET
from Packages import *
import codecs
import os
import shutil

def main():
	tree = ET.parse(os.getcwd() + '\XMLfiles\pm5300masterFile.xml', OrderedXMLTreeBuilder())
	root = tree.getroot()
	for idx,node in enumerate(root):
		if len(node.attrib.values()) > 2:
			if node.attrib.values()[2] == '408906':	
				node.set("ModbusAddress","408905")
				print node.attrib.values()[2]

   	ET.register_namespace("", "x-schema:modbus-schema.xml")
   	tree.write(os.getcwd() + '\XMLfiles\PM5300.xml' ,encoding = "utf-8", xml_declaration=True)
   	f = open(os.getcwd() + '\XMLfiles\PM5300.xml','r')
   	p = open(os.getcwd() + '\XMLfiles\PM5300_back.xml','w')
   	num_lines = sum(1 for line in open(os.getcwd() + '\XMLfiles\PM5300.xml'))
   	print(num_lines)
   	i=1
   	while(i<=num_lines):
   		print >> p , f.readline()
   		i=i+1
   	
   	f.close()
   	p.close()

   	#trying to read that file in codecs and remove the extra spaces
   	f = codecs.open(os.getcwd()+'\XMLfiles\PM5300_back.xml','r','utf-8')
   	p = codecs.open(os.getcwd() + '\XMLfiles\PM5300_back_back.xml','w','utf-8')
   	
   	
   	num_lines = sum(1 for line in open(os.getcwd() + '\XMLfiles\PM5300_back.xml'))
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
   	os.remove(os.getcwd() + '\XMLfiles\PM5300_back.xml')
   	os.remove(os.getcwd()+'\XMLfiles\PM5300.xml')
   	prevName = os.getcwd() + '\XMLfiles\PM5300_back_back.xml'
   	newName = os.getcwd() + '\XMLfiles\PM5300.xml'
	os.rename(prevName , newName )

    


   	
   	
if __name__ == '__main__':
	main()