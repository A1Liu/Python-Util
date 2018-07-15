#Need to make metaclass to create specific db objects, and then a file on DB to say what kind of db objects can be put in what folder
class dbObject:

    '''
    The following must be implemented in child classes:

        #Contains names for the fields
        _fieldNames = (...)
        #Contains type constraints for the fields
        _fieldTypes = (...)
    '''

    def __init__(self, name, *data):

        if not isinstance(name, str):
            raise TypeError("Name must be a string!")

        if not name:
            raise ValueError("Name cannot be empty!")

        try:
            if len(self._fieldNames) == 0:
                raise NotImplementedError("Tuple '_fieldNames' needs to have values")
        except AttributeError:
            raise NotImplementedError("Tuple '_fieldNames' needs to have values")

        try:
            if len(self._fieldTypes) == 0:
                raise NotImplementedError("Tuple '_fieldTypes' needs to have values")
        except AttributeError:
            raise NotImplementedError("Tuple '_fieldTypes' needs to have values")

        if len(self._fieldTypes) != len(self._fieldNames):
            raise NotImplementedError("Tuples '_fieldNames' and '_fieldTypes' need to have same lengths")

        if len(data) != len(self._fieldNames):
            raise TypeError("Data must be compatible with established fields!")

        for x in range(0,len(self._fieldTypes)):
            if not isinstance(data[x],self._fieldTypes[x]):
                raise TypeError("Data must be compatible with established field types!")

        self.data = [*data]

    def getContent(self):
        list = []
        for x in range(0,len(self._fieldNames)):
            list.append(self._fieldNames[x] + ": " + str(self.data[x]))
        return list


#This implementation works, may not have to use metaclasses?
class person(dbObject):

    #Contains names for the fields
    _fieldNames = ("Name","Phone Number")
    #Contains type constraints for the fields
    _fieldTypes = (str,tuple)
