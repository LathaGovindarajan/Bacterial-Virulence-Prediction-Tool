from flask import Flask, render_template, request, jsonify, send_file
import subprocess
import pandas as pd
import os
import joblib
from openpyxl import Workbook
from Bio import SeqIO
import io

app = Flask(__name__)

# Function to extract features using iFeature
def extract_features_from_sequence(header, sequence, feature_types):
    features = []
    with open("tmp.fasta", "w") as f:
        f.write(f">{header}\n{sequence}\n")  # Open in text mode by default
    for feature_type in feature_types:
        command = ["python3", "iFeature/iFeature.py", "--file", "tmp.fasta", "--type", feature_type, "--out", "tmp.csv"]
        result = subprocess.run(command, capture_output=True, text=True)

        if not os.path.isfile("tmp.csv"):
            error_message = f"iFeature script failed for feature type '{feature_type}'. Output: {result.stdout}, Error: {result.stderr}"
            raise FileNotFoundError(error_message)
        
        features_df = pd.read_csv("tmp.csv", sep='\t')
        features += [float(x) for x in features_df.values[0][1:]]
        os.remove("tmp.csv")
    os.remove("tmp.fasta")
    return features

# Function to extract features from sequence windows
def extract_features_from_windows(header, sequence, feature_types, window_size=20, step_size=10):
    windows = [sequence[i:i+window_size] for i in range(0, len(sequence) - window_size + 1, step_size)]
    window_features = []
    for window in windows:
        window_features.append(extract_features_from_sequence(header, window, feature_types))
    return windows, window_features

# Endpoint to handle feature extraction and prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        sequences = []
        headers = []
        
        # Check if a file or sequence is provided
        if 'file' in request.files:
            file = request.files['file']
            file_content = file.read().decode('utf-8')  # Read the file content as text
            for record in SeqIO.parse(io.StringIO(file_content), "fasta"):
                headers.append(record.id)
                sequences.append(str(record.seq))
        elif 'sequence' in request.form:
            sequence_text = request.form['sequence'].strip()
            if sequence_text:
                headers.append("sequence_1")
                sequences.append(sequence_text)
            else:
                return jsonify({'error': 'No sequence provided'}), 400
        else:
            return jsonify({'error': 'No FASTA file or sequence provided'}), 400

        feature_types = ["AAC", "DPC", "CTDC", "CTDT"]
        results = []

        # Load the saved model
        model_path = "/Applications/XAMPP/xamppfiles/htdocs/app/header_new_trained_model.joblib"  # Update this to the correct path
        loaded_model = joblib.load(model_path)

        # Extract features and predict for each sequence
        for header, seq in zip(headers, sequences):
            windows, window_features = extract_features_from_windows(header, seq, feature_types)

            # Convert features to DataFrame for prediction
            df = pd.DataFrame(window_features)

            # Predict using the loaded model
            predictions = loaded_model.predict(df)

            # Identify virulent parts
            virulent_parts = [windows[i] for i in range(len(windows)) if predictions[i] == 1]

            result = {
                'header': header,
                'sequence': seq,
                'prediction': 'Virulent' if any(predictions) else 'Non-virulent',
                'virulent_parts': virulent_parts if virulent_parts else ['N/A']
            }
            results.append(result)

        # Create an XLS file
        wb = Workbook()
        ws = wb.active
        ws.append(['Header', 'Sequence', 'Prediction', 'Virulent Parts'])

        for result in results:
            ws.append([result['header'], result['sequence'], result['prediction'], ', '.join(result['virulent_parts'])])

        output_path = 'prediction_results.xlsx'
        wb.save(output_path)

        return jsonify({'status': 'success', 'predictions': results, 'file_path': output_path})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('Latha.html')

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
