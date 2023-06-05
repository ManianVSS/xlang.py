from step import Step


class Echo(Step):
    tag = 'echo'

    def execute(self):
        print(self.attributes["message"])
