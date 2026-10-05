from googleapiclient.discovery import build


class GmailService:
    def __init__(
        self,
        auth,
    ):
        self.auth = auth
        self._service = None

    def get_service(self):
        if self._service is None:
            credentials = (
                self.auth.get_credentials()
            )

            self._service = build(
                "gmail",
                "v1",
                credentials=credentials,
            )

        return self._service

    def list_labels(self):
        service = self.get_service()

        response = (
            service.users()
            .labels()
            .list(userId="me")
            .execute()
        )

        return response.get(
            "labels",
            [],
        )

