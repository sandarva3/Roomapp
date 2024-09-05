document.addEventListener('DOMContentLoaded', () =>{
    uploadBtn = document.getElementById('fileupload');

uploadBtn.addEventListener('click', () =>{
    uploadBtn.style.display = 'none';
    document.getElementById('progressSection').style.display = "block";
    let files = document.getElementById('fileinput').files;

    getIP(files);
});
});

function getIP(files){
    fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        sendFiles(files, data.ip);
    })
    .catch(error => {
        console.log('Error:', error);
    });
};


async function sendFiles(files, ipAddress){
    let progressBar = document.getElementById('progressBar');
    progressBar.style.width="0%";
    const _filesPromises = [];
    let progressPercent = document.getElementById('progressPercent');
    const totalFiles = files.length;
    const perFile = (100/totalFiles);
    let count = 0;
    for(let i=0; i<files.length; i++){
        let formData = new FormData();
        formData.append('file', files[i]);
        formData.append('ipAddress', ipAddress);

        const _filePromise = fetch(fileURL, {
            method: "POST",
            headers:{
                'X-CSRFToken': csrfToken3
            },
            body: formData
        }).then(response => {
            count += perFile;
            progressBar.style.width = `${count}%`;
            progressPercent.innerText = `${Math.round(count)} %`;
            console.log("THE COUNT IS: ", count);
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