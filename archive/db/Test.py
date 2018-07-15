from DB import database
import os
import shutil
from DBObject import person

#shutil.rmtree(os.path.join(path,("db." + name)))


path = os.path.dirname(os.path.realpath(__file__))
print(path)
name = "example"
db = database(name,path)
# db.newClass("AppData")
# db.newClass("AddressBook","AppData")
# db.newClass("A",("AppData","AddressBook"))

#print(len(["Albert Liu",(412,414,6478)]))

#albert = person("Albert Liu",*("Albert Liu",(412,414,6478)))
#print(albert.getContent())
#db.createFile("Albert Liu",('AppData',"AddressBook","A"),*albert.getContent())

db.createFile("albert",())
