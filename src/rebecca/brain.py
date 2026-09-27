import subprocess


class Brain:
    def __init__(self, model_path="models/Qwen3-4B-Q4_K_M.gguf"):
        self.model_path = model_path

    def ask(self, prompt):
        command = [
            "llama-cli",
            "-m", self.model_path,
            "-c", "2048",
            "-t", "4",
            "-n", "256",
            "--reasoning", "off",
            "--simple-io",
            "--no-display-prompt",
            "--single-turn",
            "-p", prompt,
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        if result.returncode != 0:
            return f"Error del cerebro: {result.stderr.strip()}"

        return result.stdout.strip()
