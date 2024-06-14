function sendReq(code){
    console.log("THE file ID is:", code);
    console.log("THE URL IS : ", ajaxUrl);
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
        downloadFile(data['file'], data['filename']);
        console.log('Response from server:', data['response']);
        console.log('The name of clicked file is: ', data['filename']);
        document.getElementById('jsonresponse').innerHTML = data['file'];
    })
    .catch(error => {
        console.error('Error happened: ',error);
    });
}

function downloadFile(url, filename){
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function allFile(total){
    for(let i=0; i<(total.length); i++){
        console.log('FILE ID:', total[i]);
        sendReq(total[i]);
    }
}