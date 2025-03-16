import io
import base64


import numpy as np
import matplotlib.pyplot as plot


class Graph:
    def __init__(self, input_features, feature_names):
        self.input_features = input_features
        self.feature_names = feature_names

    def generate_plot(self, model_prediction):

        x = np.arange(len(self.input_features))

        fig, axs = plot.subplots(2, 2, figsize=(8, 6))
        fig.suptitle("Features vs Prediction")

        for i in range(len(self.input_features)):
            row = i // 2
            col = i % 2
            axs[row, col].bar(
                [self.feature_names[i], "Prediction"],
                [self.input_features[i], model_prediction],
            )
            axs[row, col].set_title(self.feature_names[i] + " & Prediction")
            axs[row, col].set_ylabel("Value")

        plot.tight_layout(rect=[0, 0.03, 1, 0.95])

        img = io.BytesIO()
        plot.savefig(img, format="png")
        img.seek(0)
        plot.close(fig)
        plot_url = base64.b64encode(img.getvalue()).decode("utf8")

        return plot_url
