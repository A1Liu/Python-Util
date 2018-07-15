import os #Functions to handle operating system
from Files import createPath, createFile, checkExist

#Database class based off of a file system. Folders hold a named 'class' of data. Will need to add support for subfolders later. Maybe all subfolders start with '.' or something similar
class database:
    #The name of the file that holds the directory of folders
    _DIRECTORY = ".fpaths.txt"

    def __init__(self, name, abspath):
        if not (isinstance(abspath, str) and abspath):
            raise TypeError("path must be a non-empty string!")
        if not (isinstance(name, str) and name):
            raise TypeError("db name must be a non-empty string!")
        self._name = "db." + name
        self._dir = os.path.realpath(os.path.join(abspath, self._name))
        if not os.path.exists(self._dir):
            os.makedirs(self._dir)
            self._folders = []
            self.emptyFile(self._DIRECTORY)#change this to a formatted file, and then add the ability to create the DB object based on the file
        elif os.path.exists(os.path.join(self._dir,self._DIRECTORY)):
            self._folders = []
            with open(os.path.join(self._dir,self._DIRECTORY),"r") as f:
                file = f.read().split("\n")
                file = file[:-1]
                for line in file:
                    pathtuple = tuple(line.split(","))
                    if len(pathtuple) == 1:
                        if not self.restoreClass(pathtuple[0]):
                            self._folders.append((pathtuple[0]))
                    else:
                        if not self.restoreClass(pathtuple[len(pathtuple)-1],pathtuple[:-1]):
                            self._folders.append((*pathtuple,))
        else:
            raise ValueError("db name is already taken by another item in file system!")

    #Creates a new folder, with the ability to nest the folder in an existing one
    def newClass(self, name, localdir = ()):
        if not (isinstance(name, str) and name):
            raise TypeError("Name must be a non-empty string!")
        localdir = self.dirTuple(localdir)
        if not checkExist(createPath(self._dir,localdir)):
            raise ValueError("Folder doesn't exist!")
        newpath = createPath(self._dir,localdir, name)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            self._folders.append((*localdir,name))
            file = open(os.path.join(self._dir,self._DIRECTORY),"a")
            if not len(localdir) == 0:
                local = ""
                for item in localdir:
                    local =  local + "," + item
                name = local + "," +  name
                name = name[1:]
            file.write(name + "\n")
            file.close()
            return True
        else:
            return False

    def delClass(self, name, localdir = ()):
        pass

    def createFile(self, name, localdir, *content):#content is by line
        localdir = self.dirTuple(localdir)
        if not checkExist(createPath(self._dir,localdir)):
            raise ValueError("Folder doesn't exist!")
        newpath = createPath(self._dir,localdir, name)
        return createFile(name, createPath(self._dir,localdir), *content)

    def writeFile(self, name, localdir, *content):
        pass

    def readFile(self, name, localdir = ()):
        
        pass

    def delFile(self, name, localdir = ()):
        pass

    def restoreClass(self, name, localdir = ()):
        if not (isinstance(name, str) and name):
            raise TypeError("Name must be a non-empty string!")
        localdir = self.dirTuple(localdir)
        if not checkExist(createPath(self._dir,localdir)):
            raise ValueError("Folder doesn't exist!")
        newpath = createPath(self._dir,localdir, name)
        if not os.path.exists(newpath):
            os.makedirs(newpath)
            self._folders.append((*localdir,name))
            return True
        else:
            return False

    def dirTuple(self, dirtuple):
        if isinstance(dirtuple, tuple):
            return dirtuple
        else:
            return (dirtuple,)
