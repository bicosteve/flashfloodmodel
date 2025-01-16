#!/usr/bin/env python
# coding: utf-8

# # Flash Prediction Model

# Import Libraries

# In[394]:


import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plot
from matplotlib import rcParams
from matplotlib.cm import rainbow

get_ipython().run_line_magic("matplotlib", "inline")
import warnings

warnings.filterwarnings("ignore")

from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score
from sklearn.metrics import recall_score, confusion_matrix, f1_score, accuracy_score
from sklearn import *
from sklearn import model_selection, neighbors

from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# from sklearn.preprocessing import LabelEncoder
# from sklearn.model_selection import cross_val_score

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

print("successful import ;)")


# Read Dataset and preprocess data

# In[44]:


# Loading Data
data = pd.read_csv("./dataset/data.csv")


# In[476]:


data.info()


# In[52]:


data.describe()


# Check the total missing data percentage

# In[54]:


missing_data = data.isnull().sum()
total_percentage = (missing_data.sum() / data.shape[0]) * 100
print(f"Total percentage of missing data is {round(total_percentage,2)}%")

duplicate_data = data[data.duplicated()]
print("Duplicate rows: ")
duplicate_data


# Normalize continuous variables

# In[56]:


scaler = MinMaxScaler()
data[
    [
        "Wind_Speed_kmh",
        "Temperature",
        "Soil_Moisture_%",
        "Humidity_%",
        "Rainfall_mm",
        "River_Discharge_m3s",
        "Elevation_m",
    ]
] = scaler.fit_transform(
    data[
        [
            "Wind_Speed_kmh",
            "Temperature",
            "Soil_Moisture_%",
            "Humidity_%",
            "Rainfall_mm",
            "River_Discharge_m3s",
            "Elevation_m",
        ]
    ]
)


# In[186]:


data.describe()


# Convert categorical variables into numeric using LabelEncoder()

# In[180]:


# Convert categorical variables into numeric using LabelEncoder()

label_encoder = LabelEncoder()

# Converting 'Slope_Position' data into numerical values
label_encoder.fit(data["Slope_Position"])
slope_data_encoded = label_encoder.transform(data["Slope_Position"])
data["Slope_Position"] = slope_data_encoded

# Converting Surface Stoniness into numeric values
label_encoder.fit(data["Surface_stoniness"])
stoniness_data_encoded = label_encoder.transform(data["Surface_stoniness"])
data["Surface_stoniness"] = stoniness_data_encoded

# Converting Erosion Degree into numeric values
label_encoder.fit(data["Erosion_degree"])
erosion_degree_data_encoded = label_encoder.transform(data["Erosion_degree"])
data["Erosion_degree"] = erosion_degree_data_encoded

# Converting 'Sensitivity to capping' into numeric values
label_encoder.fit(data["Sensitivity_to_capping"])
sensitivity_to_capping_data_encoded = label_encoder.transform(
    data["Sensitivity_to_capping"]
)
data["Sensitivity_to_capping"] = sensitivity_to_capping_data_encoded

# Converting 'Land Use Type' into numeric values
label_encoder.fit(data["Land_Use_Type"])
land_use_type_data_encoded = label_encoder.transform(data["Land_Use_Type"])
data["Land_Use_Type"] = land_use_type_data_encoded


# In[489]:


print(land_use_type_data_encoded)


# In[72]:


# Generate Descriptive Statistics
print("DATA DESCRIPTIVE STATISTICS")
print(data.describe())


# In[76]:


print("SLOPE POSITION CATEGORICAL VARIABLES")
print(data["Slope_Position"].value_counts())


# In[78]:


print("SURFACE STONINESS CATEGORICAL VARIABLES")
print(data["Surface_stoniness"].value_counts())


# In[82]:


print("EROSION DEGREE CATEGORICAL VARIABLES")
print(data["Erosion_degree"].value_counts())


# In[84]:


print("SENSITIVITY TO CAPPING CATEGORICAL VARIABLES")
print(data["Sensitivity_to_capping"].value_counts())


# In[86]:


# Summarize categorical variables
print("LAND USE CATEGORICAL VARIABLES")
print(data["Land_Use_Type"].value_counts())


# In[94]:


# Plotting Histograms for continuous variables
continous_variables = [
    "Wind_Speed_kmh",
    "Temperature",
    "Soil_Moisture_%",
    "Humidity_%",
    "Rainfall_mm",
    "River_Discharge_m3s",
    "Elevation_m",
]
data[continous_variables].hist(bins=20, figsize=(15, 20), edgecolor="black")
plot.show()


# In[188]:


# Mapping for Slope Position
slope_position_mapping = {0: "A", 1: "D", 2: "H", 3: "L", 4: "M"}

# Add a new column to the data with mapped values
data["Slope_Label"] = data["Slope_Position"].map(slope_position_mapping)

# Plot using seaborn
plot.figure(figsize=(10, 6))
sns.countplot(data=data, x="Slope_Position", hue="Flood_Occurrence")


# Update the x-axis labels with meaningful names
plot.xticks(
    ticks=range(len(slope_position_mapping)),
    labels=[slope_position_mapping[pos] for pos in range(len(slope_position_mapping))],
)

# Add title and labels
plot.title("Slope_Position Distribution by Flood Occurrence")
plot.xlabel("Slope Position")
plot.ylabel("Frequency")
plot.legend(title="Flood Occurrence", labels=["No Flood", "Flood"])


# Show plot
plot.tight_layout()
plot.show()


# In[116]:


# Mapping Surface_stoniness
surface_stoniness_mapping = {0: "A", 1: "C", 2: "D", 3: "F", 4: "M", 5: "N", 6: "v"}

# Adding New Column with mapped values
data["Surface_Label"] = data["Surface_stoniness"].map(surface_stoniness_mapping)

# Plot using seaborn
plot.figure(figsize=(10, 6))
sns.countplot(data=data, x="Surface_stoniness", hue="Flood_Occurrence")

plot.xticks(
    ticks=range(len(surface_stoniness_mapping)),
    labels=[
        surface_stoniness_mapping[pos] for pos in range(len(surface_stoniness_mapping))
    ],
)

# Add the title and the label
plot.title("Surface_stoniness Distribution by Flood Occurrence")
plot.xlabel("Surface_stoniness")
plot.ylabel("Frequency")
plot.legend(title="Flood Occurance", labels=["No Flood", "Flood"])

# show plot
plot.tight_layout()
plot.show()


# In[118]:


# Mapping for erosion_degree
erosion_degree_mapping = {0: "E", 1: "M", 2: "S", 3: "V"}

# Adding a New Column with mapped values
data["Erosion_Label"] = data["Erosion_degree"].map(erosion_degree_mapping)

# Plot using seaborn
plot.figure(figsize=(10, 6))
sns.countplot(data=data, x="Erosion_degree", hue="Flood_Occurrence")

plot.xticks(
    ticks=range(len(erosion_degree_mapping)),
    labels=[erosion_degree_mapping[pos] for pos in range(len(erosion_degree_mapping))],
)

# Add the title and the label
plot.title("Erosion_degree Distribution by Flood Occurrence")
plot.xlabel("Erosion_degree")
plot.ylabel("Frequency")
plot.legend(title="Flood Occurance", labels=["No flood", "Flood"])

# show plot
plot.tight_layout()
plot.show()


# In[120]:


# Mapping for Sensitivity_to_capping
sensitivity_to_capping_mapping = {0: "M", 1: "N", 2: "S", 3: "W"}

# Adding a New Column with mapped values
data["Capping_Label"] = data["Sensitivity_to_capping"].map(
    sensitivity_to_capping_mapping
)

# Plot using seaborn
plot.figure(figsize=(10, 6))
sns.countplot(data=data, x="Sensitivity_to_capping", hue="Flood_Occurrence")

plot.xticks(
    ticks=range(len(sensitivity_to_capping_mapping)),
    labels=[
        sensitivity_to_capping_mapping[pos]
        for pos in range(len(sensitivity_to_capping_mapping))
    ],
)

# Add the title and the label
plot.title("Sensitivity to Capping Distribution by Flood Occurrence")
plot.xlabel("Sensitivity to Capping")
plot.ylabel("Frequency")
plot.legend(title="Flood Occurance", labels=["No flood", "Flood"])

# show plot
plot.tight_layout()
plot.show()


# In[214]:


# Convert categorical variables into numeric from using LabelEncoder
label_encoder = LabelEncoder()

# Converting 'Slope_Position' data into numerical values
label_encoder.fit(data["Slope_Position"])
slope_data_encoded = label_encoder.transform(data["Slope_Position"])
data["Slope_Position"] = slope_data_encoded


# In[216]:


print(data["Slope_Position"])


# In[218]:


# Convert categorical variables into numeric from using LabelEncoder
label_encoder = LabelEncoder()

# Converting Surface Stoniness into numeric values
label_encoder.fit(data["Surface_stoniness"])
stoniness_data_encoded = label_encoder.transform(data["Surface_stoniness"])
data["Surface_stoniness"] = stoniness_data_encoded


# In[220]:


print(data["Surface_stoniness"])


# In[222]:


# Converting Erosion Degree into numeric values
label_encoder.fit(data["Erosion_degree"])
erosion_degree_data_encoded = label_encoder.transform(data["Erosion_degree"])
data["Erosion_degree"] = erosion_degree_data_encoded


# In[224]:


print(data["Erosion_degree"])


# In[226]:


# Converting 'Sensitivity to capping' into numeric values
label_encoder.fit(data["Sensitivity_to_capping"])
sensitivity_to_capping_data_encoded = label_encoder.transform(
    data["Sensitivity_to_capping"]
)
data["Sensitivity_to_capping"] = sensitivity_to_capping_data_encoded


# In[228]:


print(data["Sensitivity_to_capping"])


# In[230]:


# Converting 'Land Use Type' into numeric values
label_encoder.fit(data["Land_Use_Type"])
land_use_type_data_encoded = label_encoder.transform(data["Land_Use_Type"])
data["Land_Use_Type"] = land_use_type_data_encoded


# In[232]:


print(data["Land_Use_Type"])


# In[236]:


print(data["Slope_Label"])


# In[238]:


print(data["Surface_Label"])


# In[240]:


print(data["Erosion_Label"])


# In[176]:


print(data["Capping_Label"])


# In[244]:


# Columns to drop to get correlation matrix
columns_to_drop = ["Slope_Label", "Surface_Label", "Erosion_Label", "Capping_Label"]


# In[246]:


filtered_data = data.drop(columns=columns_to_drop)


# In[248]:


correlation_matrix = filtered_data.corr()
print(correlation_matrix)


# In[202]:


print(correlation_matrix["Flood_Occurrence"].sort_values(ascending=False))


# In[252]:


# Drop duplicate rows
filtered_data = filtered_data.drop_duplicates()


# In[256]:


# Drop the stubborn Slope_Postion
data_frame = pd.DataFrame(filtered_data)
filtered_data = data_frame.drop("Slope_Postion", axis=1)


# In[260]:


correlation_matrix = filtered_data.corr()
print(correlation_matrix)


# In[431]:


plot.figure(figsize=(8, 8))
sns.heatmap(
    correlation_matrix,
    vmax=1,
    annot=True,
    square=True,
    fmt=".2f",
    cmap="coolwarm",
    cbar=True,
)
plot.title("Correlation Matrix", fontsize=12)
plot.show()


# In[304]:


# Removes the Flood_Occurance from independent variables x-axis
# since it is not a factor in determining
# it is not a a predictor
X = filtered_data.drop(columns=["Flood_Occurrence"])
y = filtered_data["Flood_Occurrence"]


# # Split data into training and testing sets

# In[306]:


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)
print(
    "XTrains->",
    X_train.shape[0],
    "XTest->",
    X_test.shape[0],
    "YTrain->",
    y_test.shape[0],
    "YTest->",
    y_test.shape[0],
)

# Building Models
# # 1. Random Forest

# In[436]:


rmf_model = RandomForestClassifier(max_depth=3, random_state=0)
rmf_classifier = rmf_model.fit(X_train.values, y_train.values)
rmf_classifier


# In[438]:


x_train_std = scaler.fit_transform(X_train)
x_test_std = scaler.transform(X_test)


# In[440]:


# from sklearn.model_selection import cross_val_score
rmf_classiffier_accuracy = cross_val_score(
    rmf_classifier, x_train_std, y_train, cv=3, scoring="accuracy", n_jobs=-1
)


# In[441]:


rmf_classiffier_accuracy


# In[326]:


rf_scores = []
estimators = [10, 20, 100, 200, 500]
for i in estimators:
    rf_classifier = RandomForestClassifier(n_estimators=1, random_state=0)
    rf_classifier.fit(X_train.values, y_train.values)
    rf_scores.append(round(rf_classifier.score(X_test.values, y_test.values), 2))


# In[334]:


colors = rainbow(np.linspace(0, 1, len(estimators)))
plot.bar([i for i in range(len(estimators))], rf_scores, color=colors, width=0.7)
for i in range(len(estimators)):
    plot.text(i, rf_scores[i], rf_scores[i])
plot.xticks(
    ticks=[i for i in range(len(estimators))],
    labels=[str(estimator) for estimator in estimators],
)
plot.xlabel("Number of estimators")
plot.ylabel("Scores")
plot.title("Random Forest Classifier Scores for different number of estimators")
plot.show()


# In[ ]:


# In[336]:


# Replace NaN with column mean
imputer = SimpleImputer(strategy="mean")
X_imputed = imputer.fit_transform(X)


# In[342]:


y_pred = rmf_classifier.predict(X_test)


# In[344]:


# Getting a confusion matrix
print("\naccuracy score:%f" % (accuracy_score(y_test, y_pred) * 100))
print("recall score:%f" % (recall_score(y_test, y_pred) * 100))
print("roc score:%f" % (roc_auc_score(y_test, y_pred) * 100))

# Calculate F1 Score
f1 = f1_score(y_test, y_pred)
print(f"F1 Score: {f1}")

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["No Flood", "Flood"],
    yticklabels=["No Flood", "Flood"],
)
plot.xlabel("Predicted")
plot.ylabel("Actual")
plot.title("Confusion Matrix")
plot.show()


# # 2. K Nearest Neighbours

# In[352]:


# from sklearn import model_selection,neighbors
classifier = neighbors.KNeighborsClassifier()
knn_classifier = classifier.fit(X_train, y_train)


# In[354]:


# Predict chances of flood
y_predict = knn_classifier.predict(X_test)
print("Predicted chances of flood")
print(y_predict)


# In[356]:


# Actual chances of flood
print("Actual values of floods:")
print(y_test)


# In[360]:


knn_accuracy = cross_val_score(
    knn_classifier, X_test, y_test, cv=3, scoring="accuracy", n_jobs=-1
)
knn_accuracy.mean()
print("\naccuracy score:%f" % (accuracy_score(y_test, y_predict) * 100))
print("recall score:%f" % (recall_score(y_test, y_predict) * 100))
print("roc score:%f" % (roc_auc_score(y_test, y_predict) * 100))
# Calculate F1 Score
f1 = f1_score(y_test, y_predict)
print(f"F1 Score: {f1}")

cm = confusion_matrix(y_test, y_predict)
sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["No Flood", "Flood"],
    yticklabels=["No Flood", "Flood"],
)
plot.xlabel("Predicted")
plot.ylabel("Actual")
plot.title("Confusion Matrix")
plot.show()


# # K-Nearest Neighbors Model

# In[382]:


knn_scores = []
for k in range(2, 21):
    knn_classifier = KNeighborsClassifier(n_neighbors=k)
    knn_classifier.fit(X_train.values, y_train.values)
    knn_score = round(knn_classifier.score(X_test.values, y_test.values), 2)
    knn_scores.append(knn_score)


knn_classifier = KNeighborsClassifier(n_neighbors=5)
knn_classifier.fit(X_train, y_train)
knn_score = knn_classifier.predict(X_test)
print(classification_report(y_test, knn_score))


# # KNN Plot

# In[384]:


plot.plot([k for k in range(2, 21)], knn_scores, color="red")
for i in range(2, 21):
    plot.text(i, knn_scores[i - 2], (i, knn_scores[i - 2]))

plot.xticks([i for i in range(2, 21)])
plot.xlabel("Number of Neighbors (K)")
plot.ylabel("Scores")
plot.title("KNN Scores for different K neighbours")
plot.show()


# In[390]:


knn_classifier = KNeighborsClassifier(n_neighbors=11)
knn_classifier.fit(X_train.values, y_train.values)
check_data_bix = np.array([[52, 1, 0, 125, 212, 0, 1, 168, 0, 1, 2, 2, 3]])
prediction_result = knn_classifier.predict(check_data_bix)
print(f"Prediction {prediction_result}")


# # 3. Logistic Regression Model

# In[444]:


logistic_regression_model = LogisticRegression()
logistic_regression_classifier = logistic_regression_model.fit(x_train_std, y_train)
logistic_regression_accuracy = cross_val_score(
    logistic_regression_classifier,
    x_test_std,
    y_test,
    cv=3,
    scoring="accuracy",
    n_jobs=-1,
)


# In[450]:


y_predict = logistic_regression_classifier.predict(x_test_std)


# In[452]:


print("\naccuracy score: %f" % (accuracy_score(y_test, y_predict) * 100))
print("recall score: %f" % (recall_score(y_test, y_predict) * 100))
print("roc score: %f" % (roc_auc_score(y_test, y_predict) * 100))
f1 = f1_score(y_test, y_predict)
print(f"F1 Score: {f1}")


# In[ ]:


# In[461]:


# Define the number of features from your data
# number_of_features = X_train.shape[1]
# model = Sequential([
#     Dense(64, activation='relu', input_dim=number_of_features),
#     Dense(32, activation='relu'),
#     Dense(1, activation='sigmoid')  # Sigmoid for binary classification
# ])


# In[463]:


# model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


# In[465]:


# from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

# early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
# model_checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True)

# history = model.fit(X_train, y_train, validation_data=(X_test, y_test),
#                     epochs=100, batch_size=32, callbacks=[early_stopping, model_checkpoint])


# # Logistic Regression (b)

# In[459]:


# logistic_model = LogisticRegression()
# logistic_model.fit(X_train.values, y_train.values)
# logistic_model_prediction = logistic_model.predict(X_test.values)
# print(accuracy_score(y_test.values, logistic_model_prediction))
# print(classification_report(y_test.values,logistic_model_prediction))


# # Support Vector Machine

# In[457]:


svc_scores = []
kernels = ["linear", "poly", "rbf", "sigmoid"]
for i in range(len(kernels)):
    svc_classifier = SVC(kernel=kernels[i])
    svc_classifier.fit(X_train.values, y_train.values)
    svc_scores.append(round(svc_classifier.score(X_test.values, y_test.values), 2))

support_vector_model = SVC(kernel=kernels[0])
support_vector_model.fit(X_train.values, y_train.values)
svc_prediction_result = support_vector_model.predict(X_test.values)
# print(f"Support Vector Prediction results {svc_prediction_result}")
svc_accuracy = accuracy_score(y_test.values, svc_prediction_result)
print(f"Support Vector Model Accuracy is {svc_accuracy}")


# # Support Vector Plot

# In[406]:


colors = rainbow(np.linspace(0, 1, len(kernels)))
plot.bar(kernels, svc_scores, color=colors)
for i in range(len(kernels)):
    plot.text(i, svc_scores[i], svc_scores[i])
plot.xlabel("Kernels")
plot.ylabel("Scores")
plot.title("SV Model Score Activation Function Wise ...")
plot.show()


# # Artificial Neural Network Model

# In[410]:


ann_model = Sequential()
ann_model.add(Dense(units=64, activation="relu", input_dim=X_train.shape[1]))
ann_model.add(Dense(units=32, activation="relu"))
ann_model.add(Dense(units=1))

# Compile Model
ann_model.compile(optimizer="adam", loss="mean_squared_error")

# Train the model
history = ann_model.fit(
    X_train.values, y_train.values, epochs=100, batch_size=32, validation_split=0.2
)

# Evaluate the model
loss = ann_model.evaluate(X_test.values, y_test.values)
print(f"Test Loss: {loss}")

# Make Predictions
y_predict = ann_model.predict(X_test.values)

print(f"ANN Prediction: {y_predict}")


# # Plotting the ANN Model Results

# In[417]:


plot.figure(figsize=(8, 6))
# plot.subplot(1,2,1)
# plot.plot(history.history["loss"])
# plot.plot(history.history['val_loss'])
# plot.title('Model Loss')
# plot.xlabel('Epoch')
# plot.ylabel('Loss')
# plot.legend(['Train','Validation'])

plot.subplot(1, 2, 2)
plot.scatter(y_test, y_predict)
plot.xlabel("Actual Values")
plot.ylabel("Predicted Values")
plot.title("Actual vs Predicted")

plot.tight_layout()
plot.show()


# ## Add models to a file

# In[469]:


import pickle

all_models = [
    rmf_model,
    knn_classifier,
    logistic_regression_model,
    support_vector_model,
    ann_model,
]
with open("models.pkl", "wb") as files:
    pickle.dump(all_models, files)
print("Success")


# # Save trained models

# In[474]:


open_file = open("models.pkl", "rb")
loaded_list = pickle.load(open_file)
print(loaded_list)
open_file.close()
print("Done")


# In[ ]:
