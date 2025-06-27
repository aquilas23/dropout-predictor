
from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle

# Load the model
with open("dropout_model.pkl", "rb") as f:
    model = pickle.load(f)

# Define the order of features
FEATURES = ['At Risk', 'Economically Disadvantage', 'English Language Learner',
            'Homeless Student IND', 'Gender', 'Student With Disablity', 'Race']

app = Flask(__name__, template_folder='.')

@app.route('/')
def home():
    return render_template("dropout.html")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form
        input_data = [int(data.get(feature, 0)) for feature in FEATURES]
        df = pd.DataFrame([input_data], columns=FEATURES)
        pred = int(model.predict(df)[0])
        prob = float(model.predict_proba(df)[0][1])

        result = "Likely to Drop Out" if pred == 1 else "Not Likely to Drop Out"
        return f'''
            <html>
                <body>
                    <h2>{result}</h2>
                    <p>Probability of Dropout: {prob:.2%}</p>
                    <br><a href="/">Back to Form</a>
                </body>
            </html>
        '''
    except Exception as e:
        return f"<p>Error: {str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)
