import json
import subprocess
import urllib.request


class Brain:
    def __init__(
        self,
        server_url="http://127.0.0.1:8080",
    ):
        self.server_url = server_url

    def ask(self, prompt):
        url = f"{self.server_url}/v1/chat/completions"

        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            "temperature": 0.7,
            "max_tokens": 256,
        }

        request = urllib.request.Request(
            url,
            data=json.dumps(data).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request) as response:
                result = json.loads(response.read().decode("utf-8"))

            return result["choices"][0]["message"]["content"].strip()

        except Exception as error:
            return f"Error del cerebro: {error}"
