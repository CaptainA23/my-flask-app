from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the pre-trained model and necessary components
with open('bmi_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('scaler.pkl', 'rb') as file:
    scaler = pickle.load(file)

with open('le_gender.pkl', 'rb') as file:
    le_gender = pickle.load(file)

with open('le_bmi_category.pkl', 'rb') as file:
    le_bmi_category = pickle.load(file)

# Function to provide BMI recommendations
def get_bmi_recommendation(bmi):
    if bmi < 18.5:
        return "Underweight: You should consider gaining weight through a balanced diet and regular exercise."
    elif 18.5 <= bmi < 24.9:
        return "Normal weight: Keep up the good work! Maintain a balanced diet and regular exercise."
    elif 25 <= bmi < 29.9:
        return "Overweight: Consider adopting a healthier diet and increasing physical activity."
    else:
        return "Obesity: It's important to consult with a healthcare provider for personalized advice."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict_bmi', methods=['POST'])
def predict_bmi():
    try:
        data = request.json
        age = data.get('age')
        height = data.get('height')
        weight = data.get('weight')
        gender = data.get('gender')

        # Validate input
        if age is None or height is None or weight is None or gender is None:
            return jsonify({'error': 'Invalid input'}), 400

        # Convert input to appropriate types
        age = float(age)
        height = float(height)
        weight = float(weight)
        gender = gender

        # Convert gender to numerical value
        gender_encoded = le_gender.transform([gender])[0]

        # Prepare data for prediction
        features = np.array([[age, height, weight, gender_encoded]])
        
        # Standardize the features
        features_scaled = scaler.transform(features)

        # Predict BMI category
        prediction = model.predict(features_scaled)[0]
        bmi_category = le_bmi_category.inverse_transform([prediction])[0]
        
        # Calculate BMI for recommendation
        bmi = (weight / (height / 100) ** 2)

        # Get BMI recommendation
        recommendation = get_bmi_recommendation(bmi)

        # Return the prediction and recommendation as JSON
        return jsonify({'bmi': bmi, 'bmi_category': bmi_category, 'recommendation': recommendation})
    except Exception as e:
        # Log the error and return a generic error message
        print(f"Error: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True)
