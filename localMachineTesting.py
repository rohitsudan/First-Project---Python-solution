# this code here is written for learning about classes
# learnt from https://www.youtube.com/watch?v=ZDa-Z5JzLYM

# a simple employee class

class Employee:
	pass # pass is put to skip the class for now
	def __init__(self,first_name,last_name,pay):
		self.first_name = first_name
		self.last_name = last_name
		self.pay = pay
		self.email = first_name + '.' + last_name + '@company.com'



emp_1 = Employee('Corey','Scfner',50000)
emp_2 = Employee('rohit','sudan',70000)


print(emp_1.email)
print(emp_2.email)