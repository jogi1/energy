
class Options():
    def __init__(self):
        self.variables = {}

    def add(self, key, value):
        self.variables[key] = {}
        self.variables[key]['value'] = value
        self.variables[key]['defaultValue'] = value

    def get(self, key):
        if key in self.variables:
            return self.variables[key]['value']
        else:
            raise AttributeError

    def set(self, key, value):
        if key in self.variables:
            self.variables[key]['value'] = value
        else:
            raise AttributeError

    def getAll(self):
        return self.variables

    def getAllNameValue(self):
        r = {}
        for x in self.variables:
            r[x] = self.variables[x]['value']
        return r



