// API Base URL
const API_URL = 'http://localhost:8000';

// Load stats on page load
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadModelPerformance();
});

// Load statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_URL}/api/appointments/stats`);
        const data = await response.json();
        
        document.getElementById('totalAppointments').textContent = data.total_appointments;
        document.getElementById('totalPatients').textContent = data.total_patients;
        document.getElementById('totalNoshows').textContent = data.total_noshows;
        document.getElementById('noshowRate').textContent = data.noshow_rate;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Prediction form submission
document.getElementById('predictionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const patientCode = document.getElementById('patientCode').value;
    const date = document.getElementById('appointmentDate').value;
    const time = document.getElementById('appointmentTime').value;
    const type = document.getElementById('appointmentType').value;
    
    const datetime = `${date} ${time}:00`;
    
    try {
        const response = await fetch(
            `${API_URL}/api/appointments/predict-risk?patient_code=${patientCode}&appointment_datetime=${encodeURIComponent(datetime)}&appointment_type=${type}`,
            { method: 'POST' }
        );
        
        const data = await response.json();
        
        if (data.success) {
            displayPrediction(data);
        } else {
            alert('Error making prediction: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error making prediction. Make sure the model is trained.');
    }
});

// Display prediction result
function displayPrediction(data) {
    const resultDiv = document.getElementById('predictionResult');
    resultDiv.style.display = 'block';
    
    const riskScore = data.prediction.risk_score;
    const riskLevel = data.prediction.risk_level;
    
    document.getElementById('riskScore').textContent = riskScore;
    document.getElementById('riskLevel').textContent = riskLevel.toUpperCase();
    document.getElementById('resultPatient').textContent = data.patient_code;
    document.getElementById('resultDateTime').textContent = data.appointment_datetime;
    document.getElementById('resultProbability').textContent = 
        (data.prediction.probability * 100).toFixed(1) + '%';
    document.getElementById('resultRecommendation').textContent = data.recommendation;
    
    // Update circle color
    const circle = document.getElementById('scoreCircle');
    circle.className = 'score-circle ' + riskLevel;
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// CSV Import
document.getElementById('importForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const fileInput = document.getElementById('csvFile');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('Please select a CSV file');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    const resultDiv = document.getElementById('importResult');
    resultDiv.innerHTML = '<p>Importing...</p>';
    
    try {
        const response = await fetch(`${API_URL}/api/appointments/import-csv`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            resultDiv.innerHTML = `
                <div class="success-message">
                    <strong>✅ Import Successful!</strong><br>
                    Imported: ${data.appointments_imported} appointments<br>
                    New patients: ${data.patients_created}
                </div>
            `;
            loadStats(); // Refresh stats
        } else {
            resultDiv.innerHTML = `<div class="error-message">Import failed: ${data.message}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
    }
});

// Train Model
document.getElementById('trainButton').addEventListener('click', async () => {
    const resultDiv = document.getElementById('trainResult');
    const button = document.getElementById('trainButton');
    
    button.disabled = true;
    button.textContent = 'Training...';
    resultDiv.innerHTML = '<p>Training model, please wait...</p>';
    
    try {
        const response = await fetch(`${API_URL}/api/appointments/train-model`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            const metrics = data.metrics;
            resultDiv.innerHTML = `
                <div class="success-message">
                    <strong>✅ Model Trained Successfully!</strong><br>
                    Accuracy: ${(metrics.accuracy * 100).toFixed(1)}%<br>
                    Precision: ${(metrics.precision * 100).toFixed(1)}%<br>
                    Recall: ${(metrics.recall * 100).toFixed(1)}%<br>
                    Training samples: ${data.training_samples}
                </div>
            `;
            loadModelPerformance(); // Refresh chart
        } else {
            resultDiv.innerHTML = `<div class="error-message">Training failed: ${data.message}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
    } finally {
        button.disabled = false;
        button.textContent = 'Train Model';
    }
});

// Load and display model performance chart
async function loadModelPerformance() {
    // For now, we'll create a simple chart with dummy data
    // In a real app, you'd store training history in the database
    const ctx = document.getElementById('performanceChart');
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Accuracy', 'Precision', 'Recall', 'F1 Score'],
            datasets: [{
                label: 'Model Performance',
                data: [86.7, 77.8, 63.6, 70.0],
                backgroundColor: [
                    'rgba(102, 126, 234, 0.8)',
                    'rgba(118, 75, 162, 0.8)',
                    'rgba(102, 126, 234, 0.6)',
                    'rgba(118, 75, 162, 0.6)'
                ],
                borderColor: [
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)',
                    'rgba(102, 126, 234, 1)',
                    'rgba(118, 75, 162, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}