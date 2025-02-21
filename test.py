import pickle

try:
    rf_model = pickle.load(open("model.pkl", "rb"))
    svc_model = pickle.load(open("svc_model.pkl", "rb"))
    ann_model = pickle.load(open("ann_model.pkl", "rb"))
    print("success")
except (pickle.UnpicklingError, TypeError) as e:
    print(f"Error loading model: {e}")
