import pickle
import math as math


import numpy as np
from flask import Flask, flash, request, render_template, redirect, url_for

from helpers.helpers import (
    load_env_vars,
    validate_erosion_degree,
    validate_continous_variables,
)
from categories.categorize import CategorizeErosionDegree
from database.db import db_connection


app = Flask(__name__)


try:
    rf_model = pickle.load(open("./models/rf_model.pkl", "rb"))
    svc_model = pickle.load(open("./models/svc_model.pkl", "rb"))
    lr_model = pickle.load(open("./models/lr_model.pkl", "rb"))
    env_vars = load_env_vars("env.toml")
    print("Success loading models & variables")
except (pickle.UnpicklingError, TypeError) as e:
    print(f"Error loading model: {e}")


mysql = db_connection(
    env_vars["HOST"], env_vars["USER"], env_vars["PASSWORD"], env_vars["DATABASE"]
)


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        soil_moisture_content = request.form["soil-moisture"]
        rainfall_amount = request.form["rainfall"]
        river_discharge = request.form["river-discharge"]
        erosion_degree = request.form["erosion-degree"]

        is_valid_erosion_degree = validate_erosion_degree(erosion_degree)
        is_valid_continuous_vars = validate_continous_variables(
            soil_moisture_content, rainfall_amount, river_discharge
        )

        if is_valid_erosion_degree and is_valid_continuous_vars:
            Erosion_degree = CategorizeErosionDegree(erosion_degree)
            Soil_Moisture = float(soil_moisture_content)
            Rainfall_mm = float(rainfall_amount)
            River_Discharge_m3s = float(river_discharge)

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

            accuracy = average / 3

            if accuracy == 1:
                predict_text = "High chances of flash floods"
            elif accuracy > 0.5:
                predict_text = "Medium chances of flash floods"
            else:
                predict_text = "High chances of flash floods"

            cursor = mysql.cursor()

            q = """
                INSERT INTO flood_data(prediction_text,lr_model,rf_model,svc_model,accuracy) VALUES(%s,%s,%s,%s,%s)
                """
            data = (predict_text, lr_output, rf_output, svc_output, accuracy)

            print(data)

            cursor.execute(q, data)
            mysql.commit()

            flash("Data added successfully!")
            return redirect("/results")
        else:
            print("invalid results")
    return render_template("index.html")


@app.route("/results")
def results():
    try:
        cursor = mysql.cursor()
        rows = cursor.execute("SELECT * FROM flood_data")
        if rows > 0:
            flood_details = cursor.fetchall()
            return render_template("results.html", details=flood_details)
        return "An error occurred while fetching results"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        mysql.close()


if __name__ == "__main__":
    app.secret_key = "you will never know"
    app.run(port=5500, debug=True)
