def validate_slope_position_value(value):
    slope_position_accepted_values = ["A", "D", "H", "L", "M"]
    """
    1. Cleans the slope position value,
    2. validates if it is in the accepted values and return a boolean
    """

    clean_string = value.strip()
    if len(clean_string) < 1:
        return False

    clean_string = clean_string.upper()

    return value in slope_position_accepted_values


def validate_surface_stoniness_value(value):
    surface_stoniness_accepted_values = ["A", "C", "D", "F", "M", "N", "V"]
    clean_string = value.strip()
    if len(clean_string) < 1:
        return False

    clean_string = clean_string.upper()

    return value in surface_stoniness_accepted_values


def validate_affected_area_value(value):
    area_affected_accepted_values = ["1", "2", "3", "4", "5"]
    clean_string = value.strip()
    if len(clean_string) < 1:
        return False

    clean_string = clean_string.upper()

    return value in area_affected_accepted_values


def validate_erosion_degree_value(value):
    erosion_degree_accepted_values = ["E", "M", "S", "V"]
    clean_string = value.strip()
    if len(clean_string) < 1:
        return False

    clean_string = clean_string.upper()

    return value in erosion_degree_accepted_values


def validate_sensitivity_to_capping_value(value):
    sensitivity_to_capping_accepted_values = ["M", "N", "S", "W"]
    clean_string = value.strip()
    if len(clean_string) < 1:
        return False

    clean_string = clean_string.upper()

    return value in sensitivity_to_capping_accepted_values


def validate_land_use_type_value(value):
    land_use_type_accepted_values = ["Forest", "Agriculture", "Urban", "Wetland"]

    clean_string = value.strip()
    if len(clean_string) < 1:
        return False

    clean_string = clean_string.upper()
    return value in land_use_type_accepted_values
