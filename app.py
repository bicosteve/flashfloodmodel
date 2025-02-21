import pickle
import math as math
import traceback


import numpy as np
from flask import Flask, flash, request, jsonify, render_template, redirect, url_for

from helpers.helpers import (
    validate_erosion_degree_value,
    validate_continous_variables,
    load_env_vars,
)
from categories.categorize import CategorizeErosionDegree


from database.db import connection


app = Flask(__name__)


try:
    rf_model = pickle.load(open("./models/rf_model.pkl", "rb"))
    svc_model = pickle.load(open("./models/svc_model.pkl", "rb"))
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
    return jsonify({"msg": "This is test"})


@app.route("/api", methods=["GET", "POST"])
def predict_api():
    try:
        data = request.get_json()
        erosion_degree = data["erosion-degree"]
        rainfall_amount = data["rainfall"]
        river_discharge = data["river-discharge"]
        soil_moisture_content = data["soil-moisture"]

        isValid = validate_erosion_degree_value(erosion_degree)
        if not isValid:
            return jsonify({"msg": "Invalid erosion degree"})
        isValid = validate_erosion_degree_value(erosion_degree)
        if not isValid:
            return jsonify({"message": f"Erosion degree value is not valid"})

        isValid = validate_continous_variables(
            soil_moisture_content,
            rainfall_amount,
            river_discharge,
        )

        if not isValid:
            return jsonify({"message": "Invalid continues variables"})

        Erosion_degree = CategorizeErosionDegree(erosion_degree)
        Soil_Moisture = float(soil_moisture_content)
        Rainfall_mm = float(rainfall_amount)
        River_Discharge_m3s = float(river_discharge)
        Soil_Moisture = float(soil_moisture_content)
        Rainfall_mm = float(rainfall_amount)

        features = [
            Erosion_degree,
            Soil_Moisture,
            Rainfall_mm,
            River_Discharge_m3s,
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

        accuracy = average / 3  # -----> maintain the result of each.NB 3 is also ok

        if accuracy == 1:
            predict_text = "High chances of flash floods"
        elif accuracy > 0.5:
            predict_text = "Medium chances of flash floods"
        else:
            predict_text = "Low chances of flash floods"

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
        error_details = {
            "error_type": type(e).__name__,  # Name of the exception class
            "error_message": str(e),  # Error message
            "stack_trace": traceback.format_exc(),  # Full stack trace as a string
        }
        print("all")
        return jsonify({"msg": error_details})


@app.route("/add", methods=["POST"])
def predict():
    conn = None
    cursor = None
    try:
        if request.method == "POST":
            erosion_degree = request.form["erosion-degree"]
            soil_moisture_content = request.form["soil-moisture"]
            rainfall_amount = request.form["rainfall"]
            river_discharge = request.form["river-discharge"]

            # Validate the inputs
            is_valid_erosion_degree = validate_erosion_degree_value(erosion_degree)
            is_valid_continuous_vars = validate_continous_variables(
                soil_moisture_content, rainfall_amount, river_discharge
            )

            if is_valid_erosion_degree and is_valid_continuous_vars:
                Erosion_degree = CategorizeErosionDegree(erosion_degree)
                Soil_Moisture = float(soil_moisture_content)
                Rainfall_mm = float(rainfall_amount)
                River_Discharge_m3s = float(river_discharge)
                Soil_Moisture = float(soil_moisture_content)
                Rainfall_mm = float(rainfall_amount)

                features = [
                    Erosion_degree,
                    Soil_Moisture,
                    Rainfall_mm,
                    River_Discharge_m3s,
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
                return redirect(url_for("index"))
        else:
            results = cursor.execute("SELECT * FROM flood_data")
            if results > 0:
                flood_details = cursor.fetchall()
                return render_template("index.html", details=flood_details)
            return render_template("index.html")
    except Exception as e:
        print(f"An error {str(e)}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    app.run(port=5500, debug=True)
