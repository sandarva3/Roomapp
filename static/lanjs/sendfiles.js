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
    let fileSize = 100 * 1024 * 1024;
    let perFile = (100/files.length);
    let largeFiles = [];
    let smallFiles = [];

    for(let i=0; i<files.length; i++){
        if(files[i].size > fileSize){
            largeFiles.push(files[i]);
        }
        else{
            smallFiles.push(files[i]);
        }
    }

    fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        sendFiles(smallFiles, data.ip, perFile, largeFiles.length);
        if(largeFiles.length != 0){
        sendLargeFiles(largeFiles, data.ip, perFile);
        }
    })
    .catch(error => {
        console.log('Error:', error);
    });
};



async function sendLargeFiles(files, ipAddress, perFile){
    const totalLargeFiles = files.length;
    const _filePromises = [];
    const chunkSize = 10 * 1024 * 1024; //setting the size of 10 MB

    for(let i=0; i< totalLargeFiles; i++){
        let currentFile = files[i];
        console.log("CURRENT FILE: ", currentFile.name);

        let currentFileSize = currentFile.size;
        console.log("CURRENT FILE SIZE: ", currentFileSize);

        let totalChunks = Math.ceil(currentFileSize / chunkSize);
        console.log("TOTAL CHUNKS: ", totalChunks);

        const _chunkPromises = []; //We're using const here cause these variables aren't meant to be reassigned some different value. 
        //We want it to hold promise objects not other values.

        for(let chunkIndex=0; chunkIndex<totalChunks; chunkIndex++){
            console.log("current CHUNK number: ", chunkIndex);
            //get starting point and ending point in file size for chunk
            let start = chunkIndex*chunkSize;
            let end = Math.min(currentFileSize, start + chunkSize);
            //cut the file from start to end to make it a chunk.
            let chunk = currentFile.slice(start, end);
            console.log("CHUNK: ", chunk);

            let formData = new FormData();
            formData.append('chunkIndex', chunkIndex);
            formData.append('totalChunks', totalChunks);
            formData.append('filename', currentFile.name);
            formData.append('ipAddress', ipAddress);
            formData.append('chunkFile', chunk);

            let chunkPromise = fetch(largeFileURL, {
                method: "POST",
                headers:{
                    'X-CSRFToken': csrfToken3
                },
                body:formData
            }).then(response => {
                let chunkProgress = (perFile/totalChunks);
                updateProgress(chunkProgress);
            });
            //Push every chunkPromise object into array
            _chunkPromises.push(chunkPromise);
        }
        let filePromise = Promise.all(_chunkPromises);
        _filePromises.push(filePromise);
    }

    try{
        await Promise.all(_filePromises);
        console.log("ALL LARGE FILES HAVE BEEN UPLOADED");
        document.getElementById('progressPercent').innerText = "100 %";
        location.reload();
    }
    catch(error){
        console.error("AN ERROR OCCURED: ", error);
    }

}



async function sendFiles(files, ipAddress, perFile, largeFilesLength){
    const _filesPromises = [];
    const totalSmallFiles = files.length;

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
            updateProgress(perFile);
        });
        _filesPromises.push(_filePromise);
    }
    try {
        const responses = await Promise.all(_filesPromises);
        console.log("HOGAYA BHAI.. SMALL FILES");
        if(largeFilesLength === 0){
            location.reload();
        }
        //location.reload();
    } catch (error) {
        console.error("NAHI HUA BHAI...", error);
    }
};

//Logic to set a global progress variable to update progress bar.
let globalProgress = 0;
function updateProgress(increment){
    globalProgress += increment;
    console.log("GLOBAL Progress: ", globalProgress);
    let progressBar = document.getElementById('progressBar');
    let progressPercent = document.getElementById('progressPercent');
    progressBar.style.width= `${globalProgress}%`;
    progressPercent.innerText = `${Math.floor(globalProgress)} %`;
}