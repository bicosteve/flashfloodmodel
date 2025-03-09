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


app = Flask(__name__)


try:
    rf_model = pickle.load(open("./models/rf_model.pkl", "rb"))
    svc_model = pickle.load(open("./models/svc_model.pkl", "rb"))
    lr_model = pickle.load(open("./models/lr_model.pkl", "rb"))
    print("Success loading models")
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
                predict_text = "Low chances of flash floods"

            works = db.add_data(
                predict_text, lr_output, rf_output, svc_output, accuracy
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

    models = ["Random Forest", "Support Vector", "Logistic Regression", "Average"]
    rf_prediction = flood_details.get("rf_model")
    lr_prediction = flood_details.get("lr_model")
    svc_prediction = flood_details.get("svc_model")
    acurracy = flood_details.get("accuracy")
    text = flood_details.get("prediction_text")
    probabilities = [rf_prediction, svc_prediction, lr_prediction, acurracy]

    plot.figure(figsize=(8, 4))
    plot.bar(models, probabilities, color=["blue", "green", "red", "grey"])
    plot.title("Flash Flood Prediction Probabilities")
    plot.ylabel("Probability")
    plot.ylim(0, 1)

    buf = io.BytesIO()
    plot.savefig(buf, format="png")
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode("utf8")

    values = [rf_prediction, lr_prediction, svc_prediction, acurracy, text]

    print("Flood details on app ------->", values)

    return render_template("results.html", plot_url=plot_url, values=values)


if __name__ == "__main__":
    app.secret_key = "you will never know"
    app.run(port=5500, debug=True)
