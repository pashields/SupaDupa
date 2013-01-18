class SupaDupaClassDef:
    def __init__(self, name):
        self.name = name
        self.properties = {}
        self.dependencies = []

    def addProperty(self, name, typeInfo):
        self.properties[name] = typeInfo

    def addDependency(self, name):
        self.dependencies.append(name)
