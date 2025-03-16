import pickle
import math as math
import io
import base64


import numpy as np
from flask import Flask, flash, request, render_template, redirect, url_for
import matplotlib.pyplot as plot
import matplotlib

matplotlib.use("agg")


from database.db import DB
from helpers.envs import ENV
from helpers.helpers import Helpers
from categories.categorize import Graph


app = Flask(__name__)


try:
    rf_model = pickle.load(open("./models/rf_model.pkl", "rb"))
    svc_model = pickle.load(open("./models/svc_model.pkl", "rb"))
    lr_model = pickle.load(open("./models/lr_model.pkl", "rb"))
    x_train = pickle.load(open("./dataset/X_train.pkl", "rb"))
    print("Success loading models and data")
except (pickle.UnpicklingError, TypeError) as e:
    print(f"Error loading model: {e}")


env_vars = ENV("env.toml").load_env()
db = DB(env_vars["HOST"], env_vars["USER"], env_vars["PASSWORD"], env_vars["DATABASE"])


@app.route("/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        soil_moisture_content = request.form["soil-moisture"]
        rainfall_amount = request.form["rainfall"]
        river_discharge = request.form["river-discharge"]
        erosion_degree = request.form["erosion-degree"]

        helpers = Helpers(
            erosion_degree, soil_moisture_content, rainfall_amount, river_discharge
        )

        is_valid_erosion_degree = helpers.validate_erosion_degree()
        is_valid_continuous_vars = helpers.validate_continous_variables()

        if is_valid_erosion_degree and is_valid_continuous_vars:
            Erosion_degree = helpers.categorize_erosion_degree()
            Soil_Moisture = float(soil_moisture_content)
            Rainfall_mm = float(rainfall_amount)
            River_Discharge_m3s = float(river_discharge)

            features = [
                Erosion_degree,
                Soil_Moisture,
                Rainfall_mm,
                River_Discharge_m3s,
            ]

            X_predict = np.array([features])

            rf_res = rf_model.predict(X_predict)
            svc_res = svc_model.predict(X_predict)
            lr_res = lr_model.predict(X_predict)

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
                predict_text = "Low chances of flash floods"

            works = db.add_data(
                Erosion_degree,
                Soil_Moisture,
                Rainfall_mm,
                River_Discharge_m3s,
                rf_output,
                lr_output,
                svc_output,
                accuracy,
                predict_text,
            )

            if works:
                flash(f"Inserted value {works}")
                return redirect(url_for("results"))
            else:
                flash(f"Insertation is {works}")
                return redirect(url_for("predict"))

        else:
            error = "Invalid input data"
            flash(f"{error}", "error")
            return redirect(url_for("predict"))
    return render_template("index.html")


@app.route("/results")
def results():
    flood_details = db.get_data()

    rf_prediction = flood_details.get("rf_model", 0)
    lr_prediction = flood_details.get("lr_model", 0)
    svc_prediction = flood_details.get("svc_model", 0)
    acurracy = flood_details.get("accuracy", 0)
    text = flood_details.get("prediction", 0)

    erosion_degree = flood_details.get("erosion_degree", 0)
    soil_moisture = flood_details.get("soil_moisture", 0)
    rainfall = flood_details.get("rainfall", 0)
    river_discharge = flood_details.get("river_discharge", 0)

    input_features = [erosion_degree, soil_moisture, rainfall, river_discharge]
    feature_names = ["Erosion Degree", "Soil Moisture", "Rainfall", "River Discharge"]

    graph = Graph(input_features, feature_names)

    rf_plot = graph.generate_plot(str(rf_prediction))
    lr_plot = graph.generate_plot(str(lr_prediction))
    svc_plot = graph.generate_plot(str(svc_prediction))

    values = [rf_prediction, lr_prediction, svc_prediction, acurracy, text]

    return render_template(
        "results.html",
        rf_plot=rf_plot,
        lr_plot=lr_plot,
        svc_plot=svc_plot,
        values=values,
    )


if __name__ == "__main__":
    app.secret_key = "you will never know"
    app.run(port=5500, debug=True)
