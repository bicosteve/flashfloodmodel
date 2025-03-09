import toml


class ENV:
    def __init__(self, file_path):
        self.file_path = file_path
        self.env_vars = {}
        self.config = {}
        try:
            with open(self.file_path, "r") as f:
                self.config = toml.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"TOML file not found: {self.file_path}")
        except toml.TomlDecodeError as e:
            raise ValueError(f"Errod decoding TOML file {e}")

    def load_env(self) -> dict[str, str]:
        for key, value in self.config.items():
            self.env_vars[key] = str(value)

        return self.env_vars
