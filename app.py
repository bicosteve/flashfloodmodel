import re
import pickle
import math as math

import numpy as np
from flask import Flask, request, jsonify, render_template, redirect

from helpers.helpers import (
    validate_slope_position_value,
    validate_surface_stoniness_value,
    validate_affected_area_value,
    validate_erosion_degree_value,
    validate_sensitivity_to_capping_value,
    validate_land_use_type_value,
)

from categories.categorize import (
    CategorizeAffectedArea,
    CategorizeErosionDegree,
    CategorizeLandUseType,
    CategorizeSensitivityToCapping,
    CategorizeSlopePosition,
    CategorizeSurfaceStoniness,
)

app = Flask(__name__)

try:
    model = pickle.load(open("model.pkl", "rb"))
    print("Success", model)
except (pickle.UnpicklingError, TypeError) as e:
    print(f"Error loading model: {e}")


@app.route("/test", methods=["GET", "POST"])
def hello():
    return jsonify({"message": "Hello, there testing"})


@app.route("/api", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        slope_position_data = data["slope_position"]
        surface_stoniness_data = data["surface_stoniness"]
        area_affected_data = data["area_affected"]
        erosion_degree_data = data["erosion_degree"]
        sensitivity_to_capping_data = data["capping_sensitivity"]
        land_use_type_data = data["land_use"]
        wind_speed_kmh_data = data["wind_speed"]
        temperature_data = data["temperature"]
        soil_moisture_data = data["soil_moisture"]
        humidity_data = data["humidity"]
        rainfall_mm_data = data["rainfall"]
        river_discharge_m3s_data = data["river_discharge"]
        elevation_m_data = data["elevation"]

        isValid = validate_slope_position_value(slope_position_data)
        if not isValid:
            return jsonify(
                {"message": f"Slope position {slope_position_data} is not valid"}
            )

        isValid = validate_surface_stoniness_value(surface_stoniness_data)
        if not isValid:
            return jsonify(
                {
                    "message": f"Surface stoniness value {surface_stoniness_data} is not valid"
                }
            )

        isValid = validate_affected_area_value(area_affected_data)
        if not isValid:
            return jsonify(
                {"message": f"Affected area value  {area_affected_data} is not valid"}
            )

        isValid = validate_erosion_degree_value(erosion_degree_data)
        if not isValid:
            return jsonify(
                {"message": f"Erosion degree value {erosion_degree_data} is not valid"}
            )

        isValid = validate_sensitivity_to_capping_value(sensitivity_to_capping_data)
        if not isValid:
            return jsonify(
                {
                    "message": f"Sensitivity to capping {sensitivity_to_capping_data} is not valid"
                }
            )

        isValid = validate_land_use_type_value(land_use_type_data)
        if not isValid:
            return jsonify(
                {"message": f"Land use value {land_use_type_data} is not valid"}
            )

        if len(wind_speed_kmh_data) < 1:
            return jsonify(
                {"message": f"Wind speed value {wind_speed_kmh_data} is not valid"}
            )

        if int(wind_speed_kmh_data) < 1:
            return jsonify(
                {"message": f"Wind speed value {wind_speed_kmh_data} is not valid"}
            )

        if len(temperature_data) < 1:
            return jsonify(
                {"message": f"Temperature value {temperature_data} is not valid"}
            )

        if int(temperature_data) < 1:
            return jsonify(
                {"message": f"Temperature value {temperature_data} is not valid"}
            )

        if len(soil_moisture_data) < 1:
            return jsonify(
                {"message": f"Soil moisture value {soil_moisture_data} is not valid"}
            )

        if int(soil_moisture_data) < 1:
            return jsonify(
                {"message": f"Soil moisture value {soil_moisture_data} is not valid"}
            )

        if len(humidity_data) < 1:
            return jsonify({"message": f"Humidity value {humidity_data} is not valid"})

        if int(humidity_data) < 1:
            return jsonify({"message": f"Humidity value {humidity_data} is not valid"})

        if len(rainfall_mm_data) < 1:
            return jsonify(
                {"message": f"Rainfall value {rainfall_mm_data} is not valid"}
            )

        if int(rainfall_mm_data) < 1:
            return jsonify(
                {"message": f"Rainfall value {rainfall_mm_data} is not valid"}
            )

        if len(river_discharge_m3s_data) < 1:
            return jsonify(
                {
                    "message": f"River discharge value {river_discharge_m3s_data} is not valid"
                }
            )

        if int(river_discharge_m3s_data) < 1:
            return jsonify(
                {
                    "message": f"River discharge value {river_discharge_m3s_data} is not valid"
                }
            )

        if len(elevation_m_data) < 1:
            return jsonify(
                {"message": f"Elevation value {elevation_m_data} is not valid"}
            )

        if int(elevation_m_data) < 1:
            return jsonify(
                {"message": f"Elevation value {elevation_m_data} is not valid"}
            )

        Slope_Position = CategorizeSlopePosition(slope_position_data)
        Surface_Stoniness = CategorizeSurfaceStoniness(surface_stoniness_data)
        Area_affected = CategorizeAffectedArea(area_affected_data)
        Erosion_degree = CategorizeErosionDegree(erosion_degree_data)
        Sensitivity_to_capping = CategorizeSensitivityToCapping(
            sensitivity_to_capping_data
        )
        Wind_Speed_kmh = int(wind_speed_kmh_data)
        Temperature = int(temperature_data)
        Soil_Moisture = int(soil_moisture_data)
        Humidity = int(humidity_data)
        Rainfall_mm = int(rainfall_mm_data)
        River_Discharge_m3s = int(river_discharge_m3s_data)
        Land_Use_Type = CategorizeLandUseType(land_use_type_data)
        Elevation_m = int(elevation_m_data)

        features = [
            Slope_Position,
            Surface_Stoniness,
            Area_affected,
            Erosion_degree,
            Sensitivity_to_capping,
            Wind_Speed_kmh,
            Temperature,
            Soil_Moisture,
            Humidity,
            Rainfall_mm,
            River_Discharge_m3s,
            Land_Use_Type,
            Elevation_m,
        ]

        res = model.predict([features])
        print("res=", res[0], type(res))

        output = round(res[0], 4)

        return jsonify({"messsage": res, "response": output})

    except Exception as e:
        return jsonify({"message": e})


if __name__ == "__main__":
    app.run(port=5500, debug=True)


"""
   # if res[0] == 1:
        #     dict[model] = "High chance of flash flood"
        # else:
        #     dict[model] = "Low chance of flash flood"

        # avg += res

        # print("Average = ", type(avg))

        # # accuracy = avg[0] / 5
        # # accuracy = round(accuracy, 4)

        # for result in dict:
        #     print("Result", result)

        # prediction = model.predict([features])

        # response = [dict, accuracy]
"""
