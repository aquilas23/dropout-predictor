

from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd

with open("dropout_model.pkl", "rb") as f:
    model = pickle.load(f)

FEATURES = ['At Risk', 'Economically Disadvantage', 'English Language Learner',
            'Homeless Student IND', 'Gender', 'Student With Disablity', 'Race']

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("dropout.html")  # Loads your HTML file

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        input_data = [data[feature] for feature in FEATURES]
        df = pd.DataFrame([input_data], columns=FEATURES)
        prediction = int(model.predict(df)[0])
        probability = float(model.predict_proba(df)[0][1])

        return jsonify({
            "prediction": prediction,
            "dropout_probability": round(probability, 4)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)


