function sendReq(code){
    console.log("THE file ID is:", code);
    fetch(ajaxUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        body: JSON.stringify(
            {
                'data':'This is data sent from client.',
                'code': code,
            })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response from server:', data['response']);
        console.log('The name of clicked file is: ', data['filename']);
        document.getElementById('jsonresponse').innerHTML = data['file'];
    })
    .catch(error => {
        console.error('Error happened: ',error);
    });
}