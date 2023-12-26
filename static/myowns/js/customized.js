document.getElementById('updateButton').addEventListener('click', async function() {
    // Send POST request to Flask endpoint
    await fetch('/update-database', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        // Include any necessary data in the request body
        body: JSON.stringify({ /* Your data here */ })
    });

    // Show "Processing..." message immediately
    document.getElementById('status').innerText = 'Processing...';

    // After 10 seconds, update the status to "Completed"
    setTimeout(() => {
        document.getElementById('status').innerText = 'Completed';
        document.getElementById('status').style.color = 'green';
    }, 10000); // 10 seconds in milliseconds
});
