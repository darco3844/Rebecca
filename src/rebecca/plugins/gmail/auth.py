import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


class GmailAuth:
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.readonly"
    ]

    SECRET_KEY = "oauth_token"

    def __init__(
        self,
        secret_manager,
        credentials_path="data/config/gmail_credentials.json",
        plugin_name="gmail",
    ):
        self.secret_manager = secret_manager
        self.credentials_path = Path(
            credentials_path
        )
        self.plugin_name = plugin_name

    def get_credentials(self):
        credentials = (
            self._load_saved_credentials()
        )

        if credentials is not None:
            if credentials.valid:
                return credentials

            if (
                credentials.expired
                and credentials.refresh_token
            ):
                credentials.refresh(
                    Request()
                )

                self._save_credentials(
                    credentials
                )

                return credentials

        credentials = self._authorize()

        self._save_credentials(
            credentials
        )

        return credentials

    def clear_credentials(self):
        self.secret_manager.delete(
            self.plugin_name,
            self.SECRET_KEY,
        )

    def _load_saved_credentials(self):
        token_data = self.secret_manager.get(
            self.plugin_name,
            self.SECRET_KEY,
        )

        if not token_data:
            return None

        try:
            token_info = json.loads(
                token_data
            )

            return (
                Credentials.from_authorized_user_info(
                    token_info,
                    self.SCOPES,
                )
            )

        except (
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ):
            return None

    def _authorize(self):
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                "No se encontró el archivo de "
                f"credenciales de Gmail: "
                f"{self.credentials_path}"
            )

        flow = (
            InstalledAppFlow
            .from_client_secrets_file(
                str(self.credentials_path),
                self.SCOPES,
            )
        )

        return flow.run_local_server(
            port=0
        )

    def _save_credentials(
        self,
        credentials,
    ):
        self.secret_manager.set(
            self.plugin_name,
            self.SECRET_KEY,
            credentials.to_json(),
        )
