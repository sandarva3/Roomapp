document.addEventListener('DOMContentLoaded', () =>{
    uploadBtn = document.getElementById('fileupload');

uploadBtn.addEventListener('click', () =>{
    const waitArea = document.getElementById('waitArea');
    uploadBtn.style.display = 'none';
    waitArea.style.display = 'block';
    getIP(filesInArea);
});
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


async function sendFiles(filesInArea, ipAddress){
    const _filesPromises = [];
    for(let i=0; i<filesInArea.length; i++){
        let formData = new FormData();
        formData.append('file', filesInArea[i]);
        formData.append('ipAddress', ipAddress);

        const _filePromise = fetch(fileURL, {
            method: "POST",
            headers:{
                'X-CSRFToken': csrfToken3
            },
            body: formData
        });
        _filesPromises.push(_filePromise);
    }

    try {
        const responses = await Promise.all(_filesPromises);
        console.log("HOGAYA BHAI..");
        location.reload();
    } catch (error) {
        console.error("NAHI HUA BHAI...", error);
    }
};




/*  function sendFiles(filesInArea, ipAddress){
    let formData = new FormData();
    for(let i=0; i<filesInArea.length; i++){
        formData.append('file', filesInArea[i]);
        formData.append('ipAddress', ipAddress);
    }
    fetch(fileURL, {
        method: "POST",
        headers:{
            'X-CSRFToken': csrfToken3
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
};  */