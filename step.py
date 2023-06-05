import collections


class ReturnException(Exception):
    pass


class Step:
    tag = 'undefined'

    def __init__(self, parent=None, attributes=None, text=None):
        if attributes is None:
            attributes = {}
        self.parent = parent
        self.attributes = attributes
        self.text = text
        self.steps = []

    def add_steps(self, steps):
        if steps is not None:
            self.steps.extend(steps) if isinstance(steps, collections.abc.Sequence) else self.steps.append(steps)

    def execute(self, scope):
        try:
            for step in self.steps:
                step.execute(scope)
        except ReturnException:
            pass
