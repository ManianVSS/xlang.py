import collections


class Step:
    tag = 'undefined'

    def __init__(self, attributes, text):
        self.attributes = attributes
        self.text = text
        self.steps = []

    def add_steps(self, steps):
        if steps is not None:
            self.steps.extend(steps) if isinstance(steps, collections.abc.Sequence) else self.steps.append(steps)

    def execute(self):
        print("Step with tag: ", self.tag, ", attributes: ", self.attributes, " and body text ", str(self.text))
        for step in self.steps:
            step.execute()
