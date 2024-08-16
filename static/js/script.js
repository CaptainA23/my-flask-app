document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript is loaded and running');  // This should appear in the console when the page loads
});

document.getElementById('bmiForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from submitting the traditional way
    alert('Form submitted!');  // This should trigger when you click the "Predict" button

    let age = document.getElementById('age').value;
    let height = document.getElementById('height').value;
    let weight = document.getElementById('weight').value;
    let gender = document.getElementById('gender').value;

    console.log('Age:', age);
    console.log('Height:', height);
    console.log('Weight:', weight);
    console.log('Gender:', gender);
    
    // Validate input values
    if (!age || !height || !weight || !gender || isNaN(age) || isNaN(height) || isNaN(weight)) {
        alert('Please enter valid numbers for age, height, and weight, and select your gender.');
        return;
    }

    // Send data to Flask backend
    fetch('/predict_bmi', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ age: age, height: height, weight: weight, gender: gender }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // Parse the JSON response
    })
    .then(data => {
        console.log('Received data:', data);  // Debugging line to check response
        if (data.bmi && data.bmi_category) {
            document.getElementById('result').innerHTML = `
                <p><strong>Predicted BMI:</strong> ${data.bmi.toFixed(2)}</p>
                <p><strong>BMI Category:</strong> ${data.bmi_category}</p>
                <p><strong>Recommendation:</strong> ${data.recommendation}</p>
            `;
            var resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
            resultModal.show();  // Show the modal
        } else if (data.error) {
            document.getElementById('result').textContent = `Error: ${data.error}`;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('result').textContent = 'Error predicting BMI.';
    });
});
