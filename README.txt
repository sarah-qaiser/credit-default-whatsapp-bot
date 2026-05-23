Project: Credit Card Default Prediction WhatsApp Bot
Student: Sarah Qaiser Sahaf
Reg No : SP24-BBD-128

## Model Used
Logistic Regression

## Why Used This Model?
- Fast prediction
- Good for binary classification
- Supports probability/confidence scores
- Easy to deploy with Flask


FEATURE ORDER (exactly 23 comma-separated values):
1.  LIMIT_BAL   - Credit limit
2.  SEX         - 1=Male, 2=Female
3.  EDUCATION   - 1=Graduate, 2=University, 3=High School, 4=Other
4.  MARRIAGE    - 1=Married, 2=Single, 3=Other
5.  AGE         - Age in years
6.  PAY_1       - Repayment status Sep (-1=on time, 1-9=months delayed)
7.  PAY_2       - Repayment status Aug
8.  PAY_3       - Repayment status Jul
9.  PAY_4       - Repayment status Jun
10. PAY_5       - Repayment status May
11. PAY_6       - Repayment status Apr
12. BILL_AMT1   - Bill amount Sep
13. BILL_AMT2   - Bill amount Aug
14. BILL_AMT3   - Bill amount Jul
15. BILL_AMT4   - Bill amount Jun
16. BILL_AMT5   - Bill amount May
17. BILL_AMT6   - Bill amount Apr
18. PAY_AMT1    - Payment amount Sep
19. PAY_AMT2    - Payment amount Aug
20. PAY_AMT3    - Payment amount Jul
21. PAY_AMT4    - Payment amount Jun
22. PAY_AMT5    - Payment amount May
23. PAY_AMT6    - Payment amount Apr

EXPECTED COUNT: 23 values
CLASS LABELS: 0 = No Default, 1 = Default

HOW TO RUN:
1. python app.py (Terminal 1)
2. ngrok http 5000
3. Paste ngrok URL + /webhook into Twilio Sandbox Settings