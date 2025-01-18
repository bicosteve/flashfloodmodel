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
    validate_continous_variables,
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
    # print("Success", model)
except (pickle.UnpicklingError, TypeError) as e:
    print(f"Error loading model: {e}")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def predict():

    data = request.get_json()

    slope_position = data["slope-position"]
    surface_stoniness = data["surface-stoniness"]
    affected_area = data["affected-area"]
    erosion_degree = data["erosion-degree"]
    sensitivity_to_capping = data["sensitivity-to-capping"]
    wind_speed = data["wind-speed"]
    temperature = data["temperature"]
    soil_moisture_content = data["soil-moisture"]
    humidity = data["humidity"]
    rainfall_amount = data["rainfall"]
    river_discharge = data["river-discharge"]
    land_use = data["land-use"]
    elevation = data["elevation"]

    isValid = validate_slope_position_value(slope_position)
    if not isValid:
        return jsonify({"message": "Slope position is not valid"})

    isValid = validate_erosion_degree_value(erosion_degree)
    if not isValid:
        return jsonify({"msg": "Invalid erosion degree"})

    isValid = validate_surface_stoniness_value(surface_stoniness)
    if not isValid:
        return jsonify({"message": f"Surface stoniness value is not valid"})

    isValid = validate_affected_area_value(affected_area)
    if not isValid:
        return jsonify({"message": f"Affected area value is not valid"})

    isValid = validate_erosion_degree_value(erosion_degree)
    if not isValid:
        return jsonify({"message": f"Erosion degree value is not valid"})

    isValid = validate_sensitivity_to_capping_value(sensitivity_to_capping)
    if not isValid:
        return jsonify({"message": f"Sensitivity to capping is not valid"})

    isValid = validate_land_use_type_value(land_use)
    if not isValid:
        return jsonify({"message": f"Land use value is not valid"})

    isValid = validate_continous_variables(
        wind_speed,
        temperature,
        soil_moisture_content,
        humidity,
        rainfall_amount,
        river_discharge,
        elevation,
    )

    if not isValid:
        return jsonify({"message": "Invalid continues variables"})

    # soil_moisture_content = request.form["soil-moisture"]
    # rainfall_amount = request.form["rainfall-amount"]
    # river_discharge = request.form["river-discharge"]
    # erosion_degree = request.form["erosion-degree"]

    Erosion_degree = CategorizeErosionDegree(erosion_degree)
    Slope_Position = CategorizeSlopePosition(slope_position)
    Surface_Stoniness = CategorizeSurfaceStoniness(surface_stoniness)
    Area_affected = CategorizeAffectedArea(affected_area)
    Erosion_degree = CategorizeErosionDegree(erosion_degree)
    Sensitivity_to_capping = CategorizeSensitivityToCapping(sensitivity_to_capping)
    Land_Use_Type = CategorizeLandUseType(land_use)

    Wind_Speed_kmh = float(wind_speed)
    Temperature = float(temperature)
    Soil_Moisture = float(soil_moisture_content)
    Humidity = float(humidity)
    Rainfall_mm = float(rainfall_amount)
    River_Discharge_m3s = float(river_discharge)
    Elevation_m = float(elevation)
    Soil_Moisture = float(soil_moisture_content)
    Rainfall_mm = float(rainfall_amount)

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

    final_features = np.array([features])

    res = model.predict(final_features)
    print("res=", res[0], type(res))

    output = round(res[0].item(), 2)

    return {"results": output}

    # return render_template("results.html", predictions=output)


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
