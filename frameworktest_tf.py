from tensorflow.keras.callbacks import Callback
import json
import os
import time
from datetime import datetime

import matplotlib.pyplot as plt
import json
import os
from matplotlib.backends.backend_pdf import PdfPages

# Benutzerdefinierter Callback zum Speichern von Daten in JSON
class FrameworkLogger():
    def __init__(self, train_images, train_labels, test_images, test_labels, epochs, model, model_name="my_custom_model_2", log_dir="logs"):
        self.train_images = train_images
        self.train_labels = train_labels
        self.test_images = test_images
        self.test_labels = test_labels
        self.epoch_num = epochs
        self.model = model
        self.model_name = model_name
        self.log_dir = log_dir

    class JSONLogger(Callback):
        def __init__(self, model_name="model", log_dir="logs"):
            self.model_name = model_name
            self.log_dir = log_dir
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
            train_start_time = datetime.now().strftime('%Y%m%d-%H%M%S')
            self.filepath = os.path.join(log_dir, f"metrics_{train_start_time}.json")
            self.metrics_data = {
                "name": model_name,
                "timestamp": train_start_time
            }
            self.log_start_time = time.time()
            self.log_end_time = None

        def on_epoch_end(self, epoch, logs=None):
            self.log_end_time = time.time()
            epoch_duration = self.log_end_time - self.log_start_time
            print(f"Epoch {epoch} took {epoch_duration:.2f} seconds")
            self.log_start_time = self.log_end_time
            logs = logs or {}
            if "epochs" not in self.metrics_data:
                self.metrics_data["epochs"] = []
                self.metrics_data["epoch_duration"] = []
                for key in logs:
                    self.metrics_data[key] = []
            self.metrics_data["epochs"].append(epoch)
            self.metrics_data["epoch_duration"].append(epoch_duration)
            for key, value in logs.items():
                self.metrics_data[key].append(value)
            self.dump_json()

        def dump_json(self):
            with open(self.filepath, 'w') as json_file:
                json.dump(self.metrics_data, json_file)
    def train_model(self):

        # Modell trainieren
        logger = self.JSONLogger(model_name=self.model_name, log_dir=self.log_dir)
        start_time = time.time()
        self.model.fit(self.train_images, self.train_labels, epochs=self.epoch_num, validation_data=(self.test_images, self.test_labels), callbacks=[logger])
        end_time = time.time()
        training_duration = end_time - start_time

        # Modellgröße protokollieren
        self.model.save("temp_model.keras")
        model_size = os.path.getsize("temp_model.keras") / (1024)  # Convert bytes to kilobytes
        os.remove("temp_model.keras")  # Delete the temporary file
        logger.metrics_data["model_size_KB"] = model_size
        logger.metrics_data["num_epochs"] = self.epoch_num
        logger.metrics_data["training_data_size"] = len(self.train_images)

        logger.metrics_data["training_time"] = training_duration
        logger.dump_json()
        print(f"Training time: {training_duration:.2f} seconds")

        # Inferenz durchführen und Zeit aufzeichnen
        infer_start_time = time.time()
        predictions = self.model.predict(self.test_images)
        infer_end_time = time.time()
        inference_duration = infer_end_time - infer_start_time

        logger.metrics_data["inference_time"] = inference_duration
        logger.dump_json()
        print(f"Inference time for {len(self.test_images)} samples: {inference_duration:.2f} seconds")
    
    def generate_statistics(self):
        log_dir = "logs"
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.json')]
        all_metrics = []
        for log_file in log_files:
            with open(os.path.join(log_dir, log_file), "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    all_metrics.append(data)

        train_start_time = datetime.now().strftime('%Y%m%d-%H%M%S')
        if not os.path.exists("pdf"):
            os.makedirs("pdf")

        pdf_path = f"pdf/results_{train_start_time}.pdf"
        with PdfPages(pdf_path) as pdf:
            for metric in ["accuracy", "loss", "epoch_duration"]:
                self.plot_metrics(metric, all_metrics)
                pdf.savefig()
                plt.close()

    def plot_metrics(self, metric_name, all_metrics):
        for metrics in all_metrics:
            if isinstance(metrics, dict) and "epochs" in metrics and metric_name in metrics:
                plt.plot(metrics["epochs"], metrics[metric_name], label=metrics.get("name", "Unknown Model"))
            else:
                print(f"Warning: Invalid metrics data encountered: {metrics}")

            plt.title(metric_name)
            plt.xlabel('Epochs')
            plt.legend()
