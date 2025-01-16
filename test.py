import pickle
from flask import jsonify


with open("models.pkl", "rb") as file:
    try:
        loaded_data = pickle.load(file)
    except Exception as e:
        print(jsonify({"error": str(e)}))


print(loaded_data)
