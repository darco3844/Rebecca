class Tool:
    name = None
    description = ""
    permission = "read"

    def prepare_arguments(
        self,
        user_input,
        file_path_extractor=None,
    ):
        return {}

    def run(self, **kwargs):
        raise NotImplementedError(
            "La herramienta debe implementar run()."
        )

    def describe(self):
        return {
            "name": self.name,
            "description": self.description,
            "permission": self.permission,
        }
