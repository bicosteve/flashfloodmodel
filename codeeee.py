# Mapping for Sensitivity_to_capping
# sensitivity_to_capping_mapping = {0:"M",1:"N",2:"S",3:"W"}

# # Adding a New Column with mapped values
# data["Capping_Label"] = data["Sensitivity_to_capping"].map(sensitivity_to_capping_mapping)

# #Plot using seaborn
# plot.figure(figsize=(10,6))
# sns.countplot(data=data,x="Sensitivity_to_capping", hue="Flood_Occurrence")

# plot.xticks(ticks=range(len(sensitivity_to_capping_mapping)),labels=[sensitivity_to_capping_mapping[pos] for pos in range(len(sensitivity_to_capping_mapping))])

# #Add the title and the label
# plot.title("Sensitivity to Capping Distribution by Flood Occurrence")
# plot.xlabel("Sensitivity to Capping")
# plot.ylabel("Frequency")
# plot.legend(title="Flood Occurance", labels=["No flood","Flood"])

# #show plot
# plot.tight_layout()
# plot.show()


# # Plotting Histograms for continuous variables
# continous_variables = ['Wind_Speed_kmh','Temperature','Soil_Moisture_%','Humidity_%','Rainfall_mm','River_Discharge_m3s','Elevation_m']
# data[continous_variables].hist(bins=20, figsize=(15,20), edgecolor='black')
# plot.show()


# # Mapping for Slope Position
# slope_position_mapping = {0:"A",1:"D",2:"H",3:"L",4:"M"}

# # Add a new column to the data with mapped values
# data['Slope_Label'] = data["Slope_Position"].map(slope_position_mapping)

# # Plot using seaborn
# plot.figure(figsize=(10,6))
# sns.countplot(data=data,x="Slope_Position", hue="Flood_Occurrence")


# # Update the x-axis labels with meaningful names
# plot.xticks(ticks=range(len(slope_position_mapping)),labels=[slope_position_mapping[pos] for pos in range(len(slope_position_mapping))])

# #Add title and labels
# plot.title("Slope_Position Distribution by Flood Occurrence")
# plot.xlabel("Slope Position")
# plot.ylabel("Frequency")
# plot.legend(title="Flood Occurrence",labels=["No Flood","Flood"])


# #Show plot
# plot.tight_layout()
# plot.show()


# #Mapping Surface_stoniness
# surface_stoniness_mapping = {0:"A",1:"C",2:"D",3:"F",4:"M",5:"N",6:"v"}

# # Adding New Column with mapped values
# data["Surface_Label"] = data["Surface_stoniness"].map(surface_stoniness_mapping)

# #Plot using seaborn
# plot.figure(figsize=(10,6))
# sns.countplot(data=data,x="Surface_stoniness", hue="Flood_Occurrence")

# plot.xticks(ticks=range(len(surface_stoniness_mapping)),labels=[surface_stoniness_mapping[pos] for pos in range(len(surface_stoniness_mapping))])

# #Add the title and the label
# plot.title("Surface_stoniness Distribution by Flood Occurrence")
# plot.xlabel("Surface_stoniness")
# plot.ylabel("Frequency")
# plot.legend(title="Flood Occurance", labels=["No Flood","Flood"])

# #show plot
# plot.tight_layout()
# plot.show()


# Mapping for erosion_degree
# erosion_degree_mapping = {0:"E",1:"M",2:"S",3:"V"}

# # Adding a New Column with mapped values
# data["Erosion_Label"] = data["Erosion_degree"].map(erosion_degree_mapping)

# #Plot using seaborn
# plot.figure(figsize=(10,6))
# sns.countplot(data=data,x="Erosion_degree", hue="Flood_Occurrence")

# plot.xticks(ticks=range(len(erosion_degree_mapping)),labels=[erosion_degree_mapping[pos] for pos in range(len(erosion_degree_mapping))])

# #Add the title and the label
# plot.title("Erosion_degree Distribution by Flood Occurrence")
# plot.xlabel("Erosion_degree")
# plot.ylabel("Frequency")
# plot.legend(title="Flood Occurance", labels=["No flood","Flood"])

# #show plot
# plot.tight_layout()
# plot.show()


# colors = rainbow(np.linspace(0, 1, len(estimators)))
# plot.bar([i for i in range(len(estimators))], rf_scores, color=colors, width=0.7)
# for i in range(len(estimators)):
#     plot.text(i, rf_scores[i], rf_scores[i])
# plot.xticks(
#     ticks=[i for i in range(len(estimators))],
#     labels=[str(estimator) for estimator in estimators],
# )
# plot.xlabel("Number of estimators")
# plot.ylabel("Scores")
# plot.title("Random Forest Classifier Scores for different number of estimators")
# plot.show()


# rf_scores = []
# estimators = [10,20,100,200,500]
# for i in estimators:
#     rf_classifier = RandomForestClassifier(n_estimators=1, random_state = 0)
#     rf_classifier.fit(X_train.values, y_train.values)
#     rf_scores.append(round(rf_classifier.score(X_test.values, y_test.values),2))


# colors = rainbow(np.linspace(0,1,len(estimators)))
# plot.bar([i for i in range(len(estimators))],rf_scores, color=colors, width = 0.7)
# for i in range(len(estimators)):
#     plot.text(i, rf_scores[i], rf_scores[i])
# plot.xticks(ticks = [i for i in range(len(estimators))], labels = [str(estimator) for estimator in estimators])
# plot.xlabel('Number of estimators')
# plot.ylabel('Scores')
# plot.title('Random Forest Classifier Scores for different number of estimators')
# plot.show()

# Support Vector Machine Plot
# colors = rainbow(np.linspace(0,1, len(kernels)))
# plot.bar(kernels, svc_scores, color = colors)
# for i in range(len(kernels)):
#     plot.text(i, svc_scores[i], svc_scores[i])
# plot.xlabel("Kernels")
# plot.ylabel("Scores")
# plot.title("SVM Model Score Activation Function Wise ")
# # plot.show()


# ANN Model Results Plot
# plot.figure(figsize=(8,6))
# plot.subplot(1,2,2)
# plot.scatter(y_test, y_predict)
# plot.xlabel('Actual Values')
# plot.ylabel('Predicted Values')
# plot.title('Actual vs Predicted')

# plot.tight_layout()
# plot.show()
