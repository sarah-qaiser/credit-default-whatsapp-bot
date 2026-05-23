import joblib
import numpy as np
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

model  = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')

# User sends these 23 raw values
RAW_FEATURES = [
    'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
    'PAY_1', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1',  'PAY_AMT2',  'PAY_AMT3',  'PAY_AMT4',  'PAY_AMT5',  'PAY_AMT6'
]

# Only these get scaled — same as your notebook
CONTINUOUS_COLS = [
    'LIMIT_BAL', 'AGE',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1',  'PAY_AMT2',  'PAY_AMT3',  'PAY_AMT4',  'PAY_AMT5',  'PAY_AMT6'
]

# Final 27 features the model expects
MODEL_FEATURES = [
    'LIMIT_BAL', 'AGE',
    'PAY_1', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1',  'PAY_AMT2',  'PAY_AMT3',  'PAY_AMT4',  'PAY_AMT5',  'PAY_AMT6',
    'SEX_2',
    'EDUCATION_1', 'EDUCATION_2', 'EDUCATION_3', 'EDUCATION_4',
    'MARRIAGE_2', 'MARRIAGE_3'
]

EXPECTED_FEATURES = 23

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.form.get('Body', '').strip()
    resp = MessagingResponse()
    msg  = resp.message()

    # Step 1: Split
    raw_values = [v.strip() for v in incoming_msg.split(',')]

    # Step 2: Validate count
    if len(raw_values) != EXPECTED_FEATURES:
        msg.body(
            f"Invalid input. Please send exactly {EXPECTED_FEATURES} "
            f"comma-separated numeric values.\n"
            f"You sent {len(raw_values)} value(s)."
        )
        return str(resp)

    # Step 3: Parse to floats
    try:
        features = [float(v) for v in raw_values]
    except ValueError:
        msg.body(
            "Could not parse your input. "
            "Make sure all values are numbers (e.g. 50000,25,1,0,...)"
        )
        return str(resp)

    # Step 4: Map to dict
    d = dict(zip(RAW_FEATURES, features))

    # Step 5: Scale only the 14 continuous columns
    cont_vals = [[d[col] for col in CONTINUOUS_COLS]]
    scaled    = scaler.transform(cont_vals)[0]
    for i, col in enumerate(CONTINUOUS_COLS):
        d[col] = scaled[i]

    # Step 6: One-hot encode SEX, EDUCATION, MARRIAGE
    d['SEX_2']       = 1.0 if d['SEX'] == 2.0 else 0.0
    d['EDUCATION_1'] = 1.0 if d['EDUCATION'] == 1.0 else 0.0
    d['EDUCATION_2'] = 1.0 if d['EDUCATION'] == 2.0 else 0.0
    d['EDUCATION_3'] = 1.0 if d['EDUCATION'] == 3.0 else 0.0
    d['EDUCATION_4'] = 1.0 if d['EDUCATION'] == 4.0 else 0.0
    d['MARRIAGE_2']  = 1.0 if d['MARRIAGE'] == 2.0 else 0.0
    d['MARRIAGE_3']  = 1.0 if d['MARRIAGE'] == 3.0 else 0.0

    # Step 7: Build final 27-feature array in correct order
    input_array = np.array([[d[col] for col in MODEL_FEATURES]])

    # Step 8: Predict
    prediction  = model.predict(input_array)[0]
    probability = model.predict_proba(input_array)[0]

    label      = "Default" if prediction == 1 else "No Default"
    confidence = probability[int(prediction)] * 100

    reply = (
        f"Credit Default Prediction\n"
        f"---------------------------\n"
        f"Name       : Sarah Qaiser Sahaf\n"
        f"Reg No     : SP24-BBD-128\n"
        f"---------------------------\n"
        f"Result     : {prediction} ({label})\n"
        f"Confidence : {confidence:.1f}%\n"
        f"P(Default) : {probability[1]*100:.1f}%"
    )
    msg.body(reply)
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)