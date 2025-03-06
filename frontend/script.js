document.getElementById('prediction-form').addEventListener('submit', async function(event) {
    event.preventDefault();

    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    try {
        const response = await fetch("/api/predict", { // <-- No need to specify full URL
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.ok) {
            document.getElementById('result').innerText = 'Predicted Price: ' + result.prediction;
        } else {
            document.getElementById('result').innerText = 'Error: ' + result.error;
        }

        document.getElementById('result-modal').style.display = 'block';
    } catch (error) {
        document.getElementById('result').innerText = 'Error: ' + error.message;
        document.getElementById('result-modal').style.display = 'block';
    }
});
