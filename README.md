# credit-default-whatsapp-bot
ML model predicting credit card default, deployed as a live WhatsApp chatbot via Twilio
# Credit Card Default Prediction + WhatsApp Bot

A machine learning project that predicts whether a credit card customer will default on their payment, deployed as a live WhatsApp chatbot using Twilio.

## What It Does
A user sends customer features (age, credit limit, payment history etc.) via WhatsApp. The Flask backend receives the message, runs it through the trained model, and instantly replies with a **Default** or **No Default** prediction.

## Project Structure
| File | Description |
|---|---|
| `Assignment3.ipynb` | Full ML pipeline: EDA, preprocessing, model training & evaluation |
| `app.py` | Flask app handling Twilio webhook and model inference |
| `model.pkl` | Saved trained Logistic Regression model |
| `scaler.pkl` | Saved StandardScaler for feature normalization |

## Tech Stack
- **Python** — Pandas, NumPy, Scikit-learn, Matplotlib, Seaborn
- **Flask** — webhook server
- **Twilio API** — WhatsApp Sandbox integration
- **Ngrok** — local server tunneling

## ML Pipeline
- Dataset: UCI Credit Card Default (30,000 records, 23 features)
- Handled class imbalance (22% default / 78% no default) via stratified split
- Preprocessed: fixed undocumented category values, one-hot encoding, StandardScaler
- Trained 5 models: Logistic Regression, KNN, SVM, Decision Tree, Neural Network
- Best performer: **SVM (RBF kernel)** — F1: 0.52, Recall: 0.57
- Deployed model: **Logistic Regression** (lightweight, fast inference for real-time bot)

## How to Run
1. Install dependencies:
pip install flask scikit-learn pandas numpy twilio
2. Set up Twilio WhatsApp Sandbox and get your credentials
3. Run the Flask app:
python app.py
4. Use Ngrok to expose your local server:
ngrok http 5000
5. Paste the Ngrok URL into your Twilio webhook settings
6. Send customer features via WhatsApp and get predictions instantly
