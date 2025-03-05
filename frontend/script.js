document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formElements = this.elements;
    for (let i = 0; i < formElements.length; i++) {
        formElements[i].disabled = true;
    }
    
    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    // Show the loading indicator
    document.getElementById('loading').style.display = 'block';

    try {
        const response = await fetch('http://127.0.0.1:5000/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            // Handle non-200 HTTP responses
            const result = await response.json();
            document.getElementById('result').innerText = 'Error: ' + (result.error || 'Unknown error');
        } else {
            // Handle successful response
            const result = await response.json();
            if (result.prediction !== undefined) {
                document.getElementById('result').innerText = 'Predicted Price: ' + result.prediction;
            } else {
                document.getElementById('result').innerText = 'Unexpected response format';
            }
        }
    } catch (error) {
        // Handle network or other errors
        document.getElementById('result').innerText = 'Error: ' + error.message;
    } finally {
        // Hide the loading indicator
        document.getElementById('loading').style.display = 'none';
        // Show the modal
        document.getElementById('result-modal').style.display = 'block';
        // Clear the form
        document.getElementById('prediction-form').reset();
    }
});

// Close the modal when the user clicks on the close button
document.querySelector('.close-button').addEventListener('click', function() {
    document.getElementById('result-modal').style.display = 'none';
});

// Close the modal when the user clicks outside of the modal
window.addEventListener('click', function(event) {
    if (event.target === document.getElementById('result-modal')) {
        document.getElementById('result-modal').style.display = 'none';
    }
});
