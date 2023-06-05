class Scope:
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
        self.functions = {}

        # Inherit scope from parent
        if self.parent:
            for variable in self.parent.variables:
                self.variables[variable] = self.parent.variables[variable]
            for function in self.parent.functions:
                self.functions[function] = self.parent.functions[function]

    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        elif self.parent:
            return self.parent.get_variable(name)
        else:
            return None

    def get_function(self, name):
        if name in self.functions:
            return self.functions[name]
        elif self.parent:
            return self.parent.get_function(name)
        else:
            return None
