document.addEventListener('DOMContentLoaded', () =>{
    uploadBtn = document.getElementById('fileupload');

uploadBtn.addEventListener('click', () =>{
    const waitArea = document.getElementById('waitArea');
    uploadBtn.style.display = 'none';
    waitArea.style.display = 'block';
    getIP(filesInArea);
})
});

function getIP(filesInArea){
    fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        sendFiles(filesInArea, data.ip);
    })
    .catch(error => {
        console.log('Error:', error);
    });
};

function sendFiles(filesInArea, ipAddress){
    let formData = new FormData();
    for(let i=0; i<filesInArea.length; i++){
        formData.append('file', filesInArea[i]);
        formData.append('ipAddress', ipAddress);
    }
    fetch(fileURL, {
        method: "POST",
        headers:{
            'X-CSRFToken': csrf
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log('FILE Status: ', data.status);
        location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
};