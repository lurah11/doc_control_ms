function redirectResponse(elementid,redirect_url,message){
    document.getElementById(elementid).addEventListener('submit', function(event) {
        event.preventDefault();  

        let form = this;
        let formData = new FormData(form);  // Collect form data

        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',  // Indicates it's an AJAX request
            },
        })
        .then(response => response.json())  // Parse the JSON response
        .then(data => {
            if (data['success']) {
                // If the response is successful, show a success message
                alert(message);
                window.location.href=redirect_url
            } else {
                // Handle validation errors
                alert('There was an error. Please check your input.');
                console.error(data.errors);  // You can also display the errors on the form
            }
        })
        .catch(error => {
            console.error('Error:', error);  // Log any errors that occur
        });
    });
}