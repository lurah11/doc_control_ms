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
                alert(message);
                window.location.href=redirect_url
            } else {
                let alertMessage = "Please check these issues:\n";
                const errors = JSON.parse(data.errors)
                alertMessage += errors 
                alert(alertMessage)
      
            }
        })
        .catch(error => {
            console.error('Error:', error);  // Log any errors that occur
        });
    });
}