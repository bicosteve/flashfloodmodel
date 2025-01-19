import pickle
import math as math


import numpy as np
from flask import Flask, flash, request, jsonify, render_template, redirect

from helpers.helpers import (
    validate_slope_position_value,
    validate_surface_stoniness_value,
    validate_affected_area_value,
    validate_erosion_degree_value,
    validate_sensitivity_to_capping_value,
    validate_land_use_type_value,
    validate_continous_variables,
    load_env_vars,
)
from categories.categorize import (
    CategorizeAffectedArea,
    CategorizeErosionDegree,
    CategorizeLandUseType,
    CategorizeSensitivityToCapping,
    CategorizeSlopePosition,
    CategorizeSurfaceStoniness,
)

from database.db import connection


app = Flask(__name__)


try:
    rf_model = pickle.load(open("./models/model.pkl", "rb"))
    svc_model = pickle.load(open("./models/svc_model.pkl", "rb"))
    ann_model = pickle.load(open("./models/ann_model.pkl", "rb"))
    lr_model = pickle.load(open("./models/lr_model.pkl", "rb"))
    env_vars = load_env_vars("env.toml")
    print("Success loading models & variables")
except (pickle.UnpicklingError, TypeError) as e:
    print(f"Error loading model: {e}")


mysql = connection(
    env_vars["HOST"], env_vars["USER"], env_vars["PASSWORD"], env_vars["DATABASE"]
)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/api", methods=["POST"])
def predict_api():
    conn = None
    cursone = None
    try:
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

        rf_res = rf_model.predict(final_features)
        svc_res = svc_model.predict(final_features)
        lr_res = lr_model.predict(final_features)

        rf_output = round(rf_res[0].item(), 2)
        svc_output = round(svc_res[0].item(), 2)
        lr_output = round(lr_res[0].item(), 2)

        average = rf_output + svc_output + lr_output
        predict_text = ""

        accuracy = average / 3

        if accuracy == 1:
            predict_text = "High chances of flash floods"
        elif accuracy > 0.5:
            predict_text = "Medium chances of flash floods"
        else:
            predict_text = "High chances of flash floods"

        return jsonify(
            {
                "random_forest": rf_output,
                "svc_model": svc_output,
                "lr_model": lr_output,
                "accuracy": accuracy,
                "Prediction": predict_text,
            }
        )
    except Exception as e:
        print("all")


@app.route("/add", methods=["POST"])
def predict():
    conn = None
    cursor = None
    try:
        slope_position = request.form["slope-position"]
        surface_stoniness = request.form["surface-stoniness"]
        affected_area = request.form["affected-area"]
        erosion_degree = request.form["erosion-degree"]
        sensitivity_to_capping = request.form["sensitivity-to-capping"]
        wind_speed = request.form["wind-speed"]
        temperature = request.form["temperature"]
        soil_moisture_content = request.form["soil-moisture"]
        humidity = request.form["humidity"]
        rainfall_amount = request.form["rainfall"]
        river_discharge = request.form["river-discharge"]
        land_use = request.form["land-use"]
        elevation = request.form["elevation"]

        slope_position = request.form["slope-position"]
        surface_stoniness = request.form["surface-stoniness"]
        affected_area = request.form["affected-area"]
        erosion_degree = request.form["erosion-degree"]
        sensitivity_to_capping = request.form["sensitivity-to-capping"]
        wind_speed = request.form["wind-speed"]
        temperature = request.form["temperature"]
        soil_moisture_content = request.form["soil-moisture"]
        humidity = request.form["humidity"]
        rainfall_amount = request.form["rainfall"]
        river_discharge = request.form["river-discharge"]
        land_use = request.form["land-use"]
        elevation = request.form["elevation"]

        isValid = validate_slope_position_value(slope_position)
        isValid = validate_erosion_degree_value(erosion_degree)
        isValid = validate_surface_stoniness_value(surface_stoniness)
        isValid = validate_affected_area_value(affected_area)
        isValid = validate_erosion_degree_value(erosion_degree)
        isValid = validate_sensitivity_to_capping_value(sensitivity_to_capping)
        isValid = validate_land_use_type_value(land_use)
        isValid = validate_continous_variables(
            wind_speed,
            temperature,
            soil_moisture_content,
            humidity,
            rainfall_amount,
            river_discharge,
            elevation,
        )

        if isValid and request.method == "POST":

            Erosion_degree = CategorizeErosionDegree(erosion_degree)
            Slope_Position = CategorizeSlopePosition(slope_position)
            Surface_Stoniness = CategorizeSurfaceStoniness(surface_stoniness)
            Area_affected = CategorizeAffectedArea(affected_area)
            Erosion_degree = CategorizeErosionDegree(erosion_degree)
            Sensitivity_to_capping = CategorizeSensitivityToCapping(
                sensitivity_to_capping
            )
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

            rf_res = rf_model.predict(final_features)
            svc_res = svc_model.predict(final_features)
            lr_res = lr_model.predict(final_features)

            rf_output = round(rf_res[0].item(), 2)
            svc_output = round(svc_res[0].item(), 2)
            lr_output = round(lr_res[0].item(), 2)

            average = rf_output + svc_output + lr_output
            predict_text = ""

            accuracy = average / 3

            if accuracy == 1:
                predict_text = "High chances of flash floods"
            elif accuracy > 0.5:
                predict_text = "Medium chances of flash floods"
            else:
                predict_text = "High chances of flash floods"

            q = """
                INSERT INTO flood_data(prediction_text,lr_model,rf_model,svc_model,accuracy) VALUES(%s,%s,%s,%s,%s)
                """
            data = (predict_text, lr_model, rf_model, svc_model, accuracy)

            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(q, data)
            conn.commit()

            flash("Data added successfully!")
            return redirect("/")
        else:
            return "Something went wrong!!"
    except Exception as e:
        print(f"An error {str(e)}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(port=5500, debug=True)
