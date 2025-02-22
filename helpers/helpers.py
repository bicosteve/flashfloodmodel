import toml


def load_env_vars(file_path):
    try:
        with open(file_path, "r") as f:
            config = toml.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"TOML file not found: {file_path}")
    except toml.TomlDecodeError as e:
        raise ValueError(f"Errod decoding TOML file {e}")

    env_vars = {}
    for key, value in config.items():
        env_vars[key] = str(value)

    return env_vars


def validate_erosion_degree(value):
    accepted_values = ["E", "M", "S", "V"]
    clean_string = value.strip()
    if len(clean_string) < 1 and value not in accepted_values:
        return False
    return True


def validate_continous_variables(soil, rainfall, river):
    soil = int(soil)
    rainfall = int(rainfall)
    river = int(river)

    if soil < 1 and rainfall < 1 and river < 1:
        return False

    return True
