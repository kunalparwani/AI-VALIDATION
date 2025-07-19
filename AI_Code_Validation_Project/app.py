from flask import Flask, render_template, request
from keras.models import load_model
from scripts.ml_module import predict_vulnerability
from scripts.preprocessing import preprocess_code_sliding_window
from scripts.non_ml_module import run_bandit
from scripts.aggregator import aggregate_results_all
from scripts import myutils

from transformers import RobertaModel
import torch

app = Flask(__name__)

# Load GraphCodeBERT model once at startup for efficiency
embedding_model = RobertaModel.from_pretrained("microsoft/graphcodebert-base")

# Load all vulnerability models at startup for efficiency
models = {
    "command_injection": load_model("models/LSTM_model_command_injection_gcbt.h5",
        custom_objects={
        'f1_loss': myutils.f1_loss,
        'f1': myutils.f1
    }),
    "remote_code_execution": load_model("models/LSTM_model_remote_code_execution_gcbt.h5",
        custom_objects={
        'f1_loss': myutils.f1_loss,
        'f1': myutils.f1
    }),
    "sql_injection": load_model("models/LSTM_model_sql_gcbt.h5",
      custom_objects={
        'f1_loss': myutils.f1_loss,
        'f1': myutils.f1
    }),
    "xss": load_model("models/LSTM_model_xss_gcbt.h5",  
        custom_objects={
        'f1_loss': myutils.f1_loss,
        'f1': myutils.f1
    })
}



@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code_text = request.form.get("code")

        if not code_text or code_text.strip() == "":
            return "No code provided."

        # Save code to temp file
        filepath = "temp_code.py"
        with open(filepath, "w") as f:
            f.write(code_text)

        chunks, tokeniser = preprocess_code_sliding_window(filepath, maxlen=200, stride=100)
        embedded_chunks = []
        for chunk in chunks:
            input_ids_tensor = torch.tensor([chunk])  # shape (1, 200)
            with torch.no_grad():
                outputs = embedding_model(input_ids_tensor)
                embedding = outputs.last_hidden_state.squeeze(0).numpy()  # shape (200, 768)
            embedded_chunks.append(embedding)


        # Run all ML models
        ml_results = {}
        for vuln_type, model in models.items():
            vuln_detected = False

            for embedding in embedded_chunks:
                input_chunk = embedding.reshape(1, 200, 768)  # match model input shape

                label = predict_vulnerability(model, input_chunk)

                if label == "vulnerable":
                    vuln_detected = True
                    break  # Stop checking further chunks if vulnerability is already found

            ml_results[vuln_type] = {
                "label": "vulnerable" if vuln_detected else "secure",
                "vulnerability_type": vuln_type if vuln_detected else None
            }

        # Run Non-ML tools
        non_ml_result = run_bandit(filepath)

        # Aggregate results
        final_result = aggregate_results_all(ml_results, non_ml_result)

        return render_template("result.html", result=final_result)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False, port=5050)
