document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('uploadForm');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                resultsDiv.innerHTML = '<p>Prediction results:</p>';
                data.predictions.forEach(prediction => {
                    resultsDiv.innerHTML += `
                        <p>Sequence: ${prediction.sequence}</p>
                        <p>Prediction: ${prediction.prediction}</p>
                        <p>Virulent Parts: ${prediction.virulent_parts.join(', ')}</p>
                        <hr>
                    `;
                });

                // Download link for Excel file
                resultsDiv.innerHTML += `<a href="${data.file_path}" download>Download Excel</a>`;
            } else {
                resultsDiv.innerHTML = `<p>Error: ${data.message}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultsDiv.innerHTML = '<p>Error predicting sequences.</p>';
        });
    });
});
