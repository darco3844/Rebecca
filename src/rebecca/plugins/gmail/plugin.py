from src.rebecca.plugins.plugin import (
    Plugin,
)

from src.rebecca.plugins.gmail.auth import (
    GmailAuth,
)

from src.rebecca.plugins.gmail.service import (
    GmailService,
)

from src.rebecca.plugins.gmail.tools import (
    GmailSearchTool,
    GmailReadTool,
)


class GmailPlugin(Plugin):
    name = "gmail"

    description = (
        "Integración de Rebecca con Gmail."
    )

    version = "1.0.0"

    def __init__(self):
        self.auth = None
        self.service = None

        self.tools = [
            GmailSearchTool(),
            GmailReadTool(),
        ]

    def initialize(self):
        if self.secrets is None:
            raise RuntimeError(
                "Gmail necesita SecretManager."
            )

        self.auth = GmailAuth(
            secret_manager=self.secrets,
            plugin_name=self.name,
        )

        self.service = GmailService(
            auth=self.auth,
        )

        gmail_service = (
            self.service.get_service()
        )

        for tool in self.tools:
            tool.gmail_service = (
                gmail_service
            )

    def shutdown(self):
        for tool in self.tools:
            tool.gmail_service = None

        self.tools = []
        self.service = None
        self.auth = None

    def get_tools(self):
        return self.tools

    def get_api_service(self):
        if self.service is None:
            raise RuntimeError(
                "El plugin de Gmail no está "
                "inicializado."
            )

        return self.service.get_service()

    def authenticate(self):
        return self.get_api_service()

    def list_labels(self):
        if self.service is None:
            raise RuntimeError(
                "El plugin de Gmail no está "
                "inicializado."
            )

        return self.service.list_labels()


PLUGIN_CLASS = GmailPlugin

