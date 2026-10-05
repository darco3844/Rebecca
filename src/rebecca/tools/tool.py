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

    def format_result(
        self,
        result,
        user_input="",
    ):
        return None

    def describe_action(
        self,
        kwargs,
    ):
        if not kwargs:
            return (
                f"Voy a ejecutar la herramienta "
                f"'{self.name}'."
            )

        details = []

        for key, value in kwargs.items():
            details.append(
                f"{key}: {value}"
            )

        return (
            f"Voy a ejecutar la herramienta "
            f"'{self.name}' con los siguientes datos:\n"
            + "\n".join(details)
        )

    def describe(self):
        return {
            "name": self.name,
            "description": self.description,
            "permission": self.permission,
        }

