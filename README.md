# Bacterial Virulence Prediction Tool

## Overview

The Bacterial Virulence Prediction Tool is a web application designed to analyze protein sequences and predict their virulence using machine learning. Users can either enter protein sequences manually or upload FASTA files. The tool processes the sequences, extracts features, and predicts whether they are virulent or non-virulent. Results can be downloaded in an Excel format.

## Features

- **Sequence Input**: Enter protein sequences directly into a text box.
- **FASTA File Upload**: Upload FASTA files for sequence analysis.
- **Feature Extraction**: Extract features from sequences using iFeature.
- **Machine Learning Prediction**: Predict virulence using a trained model.
- **Results Download**: Download the results in an Excel file.

## Technology Stack

- **Flask**: Micro web framework for Python.
- **Python**: Programming language used for backend processing.
- **iFeature**: Script for extracting features from protein sequences.
- **OpenPyXL**: Library for working with Excel files.
- **BioPython**: Library for biological computation and sequence handling.
- **Joblib**: Library for loading and saving machine learning models.

## Installation

### Prerequisites

Ensure you have Python 3.x installed on your machine. You will also need to install the following libraries:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/LathaGovindarajan/Bacterial-Virulence-Prediction-Tool.git
    cd your-repository
    ```

2. **Create and activate a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure iFeature is available**:
   Download and place iFeature in the project directory or adjust paths in `app.py` accordingly.

## Usage

1. **Run the Flask application**:
    ```bash
    python app.py
    ```

2. **Open your browser** and go to `http://localhost:5001`.

3. **Enter sequences or upload FASTA files** in the provided form. The fasta format is the ">" symbol followed by the header and in the next line the sequence should be present in an single line.Submit to see the predictions.


4. **Download results** from the Results section.

## File Structure

- `app.py`: Main application script.
- `requirements.txt`: Python dependencies.
- `static/`: Contains static files like images.
- `templates/`: Contains HTML files like `Latha.html`.

## Contributing

1. **Fork the repository** and create a new branch.
2. **Make your changes** and test them.
3. **Submit a pull request** with a clear description of your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact:

- **Name**: Latha Govindarajan
- **Email**: lathamythili2000@gmail.com

---

Thank you for using the Bacterial Virulence Prediction Tool
