import toml


class Helpers:
    def __init__(self, erosion_degree, soil, rainfall, river):
        self.erosion_degree = erosion_degree
        self.soil_moisture = soil
        self.rainfall_amount = rainfall
        self.river_discharge = river

    def validate_erosion_degree(self):
        accepted_values = ["E", "M", "S", "V"]
        clean_string = self.erosion_degree.strip()
        if len(clean_string) < 1 and self.erosion_degree not in accepted_values:
            return False
        return True

    def categorize_erosion_degree(self):
        category = 0
        if self.erosion_degree == "E":
            category = 0
        elif self.erosion_degree == "M":
            category = 1
        elif self.erosion_degree == "S":
            category = 2
        elif self.erosion_degree == "V":
            category = 3
        return category

    def validate_continous_variables(self):
        soil = float(self.soil_moisture)
        rainfall = float(self.rainfall_amount)
        river = float(self.river_discharge)
        if soil <= 0 and rainfall <= 0 and river <= 0:
            return False
        return True
