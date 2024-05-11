# CAPTCHA Solver with Flask and Tampermonkey

## Overview

This project provides a solution for solving CAPTCHA images using a machine learning model hosted on a Flask server. A Tampermonkey script is used to automatically fetch CAPTCHA images from a specified web page, send them to the Flask server for prediction, and fill the results into the web page's input field.

## Features

- **Model Training**: Train a CNN model to recognize CAPTCHA images.
- **Model Compression**: Convert the Keras model to TensorFlow Lite for reduced size.
- **Flask Server**: Serve the model for prediction through a REST API.
- **Tampermonkey Script**: Automatically interact with web pages to solve and input CAPTCHA.

## Installation

### Prerequisites

- Python 3.x
- Pip
- Node.js and npm (for Tampermonkey script testing)
- [Tampermonkey Extension](https://www.tampermonkey.net/) installed in your browser

### Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/bluegitter/captcha-solver.git
    cd captcha-solver
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Download or generate CAPTCHA dataset**:
   - Place your dataset in the `data/` directory.
   - Ensure images are named according to their CAPTCHA text (e.g., `abcd1.jpeg`).

5. **Train the model**:

    ```bash
    python train_model.py  # Assuming you have a script to train the model
    ```

6. **Run the Flask server**:

    ```bash
    python app.py
    ```

7. **Set up the Tampermonkey script**:
   - Create a new script in Tampermonkey and paste the content from `captcha_solver.user.js`.

## Usage

1. **Start the Flask server**:

    Ensure the Flask server is running:

    ```bash
    python app.py
    ```

2. **Visit the target web page**:

    Open the web page where the CAPTCHA needs to be solved (e.g., `http://192.168.63.56:9090/#/login`).

3. **Tampermonkey script**:

    The Tampermonkey script will automatically:
    - Extract the CAPTCHA image.
    - Send it to the Flask server.
    - Receive the predicted text and input it into the CAPTCHA field.

## Flask API Endpoints

- **`POST /predict`**: Accepts a CAPTCHA image file and returns the predicted text.
  - **Request**: Multipart form-data with key `file` containing the image.
  - **Response**: JSON with the predicted label.

## File Structure

