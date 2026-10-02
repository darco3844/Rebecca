class Plugin:
    name = None
    description = ""
    version = "1.0.0"

    config = None
    secrets = None

    def initialize(self):
        pass

    def shutdown(self):
        pass

    def get_tools(self):
        return []

    def describe(self):
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "tools": [
                tool.describe()
                for tool in self.get_tools()
            ],
        }
