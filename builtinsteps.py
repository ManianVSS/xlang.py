from scope import Scope
from step import Step, ReturnException
from utils import type_utils


class Echo(Step):
    tag = 'echo'

    def execute(self, scope):
        print(type_utils.replace_variables(self.attributes["message"], scope.variables))


class FunctionDefinition(Step):
    tag = 'func'

    def execute(self, scope):
        function_name = self.attributes['name']
        if function_name in scope.functions:
            raise Exception('Function already defined ' + function_name)
        scope.functions[function_name] = self.steps


class VariableDefinition(Step):
    tag = 'var'

    # noinspection PyAttributeOutsideInit
    def execute(self, scope):
        self.name = self.attributes['name'] if 'name' in self.attributes else None
        self.type = self.attributes['type'] if 'type' in self.attributes else None
        self.value = self.attributes['value'] if 'value' in self.attributes else self.text
        self.expr = self.attributes['expr'] if 'expr' in self.attributes else None
        self.from_attribute = self.attributes['fromAttribute'] if 'fromAttribute' in self.attributes else None
        self.from_text = bool(self.attributes['fromText']) if 'fromText' in self.attributes else None

        if self.from_attribute and self.parent and self.parent.attributes:
            self.value = self.parent.attributes[self.from_attribute]
        elif self.from_text and self.parent:
            self.value = self.parent.text
        elif self.expr:
            self.value = type_utils.replace_variables(self.expr, scope.variables)
        self.value = type_utils.convert_from_string(self.type, self.value)

        scope.variables[self.name] = self.value


class FunctionCall(Step):
    tag = 'call'

    # noinspection PyAttributeOutsideInit
    def execute(self, scope):
        self.name = self.attributes['name'] if 'name' in self.attributes else None
        self.input_params = [s.strip() for s in (self.attributes['inputParameters'].split(',') if
                                                 'inputParameters' in self.attributes else [])]
        self.output_params = [s.strip() for s in (self.attributes['outputParameters'].split(',') if
                                                  'outputParameters' in self.attributes else [])]

        if not self.name:
            raise Exception("Function name missing for call")
        function = scope.get_function(self.name)
        if not function:
            raise Exception('Function not defined: ' + self.name)
        function_scope = Scope(scope)

        # Copy in input parameters to function scope
        for param in self.input_params:
            if param in scope.variables:
                function_scope.variables[param] = scope.variables[param]

        # Run the function steps
        try:
            for function_step in function:
                function_step.execute(function_scope)
        except ReturnException:
            pass

        # Copy out output parameters from function scope
        for param in self.output_params:
            if param in function_scope.variables:
                scope.variables[param] = function_scope.variables[param]


class Return(Step):
    tag = 'return'

    def execute(self, scope):
        raise ReturnException
