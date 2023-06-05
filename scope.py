class Scope:
    def __init__(self):
        self.parent = None
        self.variables = {}
        self.functions = {}

    # def has_local_variable(self, name):
    #     return name in self.variables

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            return None

    # def put_variable(self, name, value):
    #     self.variables[name] = value
