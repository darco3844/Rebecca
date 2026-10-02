import keyring


class SecretManager:
    SERVICE_NAME = "rebecca"

    def __init__(
        self,
        service_name=None,
    ):
        if service_name is not None:
            self.service_name = service_name
        else:
            self.service_name = (
                self.SERVICE_NAME
            )

    def set(
        self,
        plugin_name,
        key,
        value,
    ):
        if not plugin_name:
            raise ValueError(
                "El plugin debe tener un nombre."
            )

        if not key:
            raise ValueError(
                "La clave secreta debe tener un nombre."
            )

        if value is None:
            raise ValueError(
                "El valor secreto no puede ser None."
            )

        username = self._build_username(
            plugin_name,
            key,
        )

        keyring.set_password(
            self.service_name,
            username,
            str(value),
        )

    def get(
        self,
        plugin_name,
        key,
    ):
        username = self._build_username(
            plugin_name,
            key,
        )

        return keyring.get_password(
            self.service_name,
            username,
        )

    def has(
        self,
        plugin_name,
        key,
    ):
        return (
            self.get(
                plugin_name,
                key,
            )
            is not None
        )

    def delete(
        self,
        plugin_name,
        key,
    ):
        username = self._build_username(
            plugin_name,
            key,
        )

        try:
            keyring.delete_password(
                self.service_name,
                username,
            )

        except keyring.errors.PasswordDeleteError:
            return False

        return True

    def _build_username(
        self,
        plugin_name,
        key,
    ):
        return (
            f"plugin:{plugin_name}:"
            f"{key}"
        )
