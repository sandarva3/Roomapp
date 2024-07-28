document.addEventListener("DOMContentLoaded", ()=> {
    console.log("LOCALE");

    //WHEN CHANGES ARE MADE IN TEXTAREA
    let textBox = document.getElementById('textBox3');
    console.log("TEXTBOX FOUND:", textBox.value);
    const debouncedCheckIP = debounce(checkIP, 650);

    textBox.addEventListener("input", function(){
        console.log("Textbox Triggered");

    const textValue = textBox.value;
    // checkIP(textValue);
    debouncedCheckIP(textValue);
});



console.log("FILES IN AREAA AAA");

let fileinput = document.getElementById('fileinput');
fileinput.addEventListener('change', function(event){
    document.getElementById('fileinput').style.display = "inline-block";
    document.getElementById('selectFileBtn').style.display = "none";
    document.getElementById('fileupload').style.display = "inline";

    let filesInArea = [];
    console.log("THE FILES ARE WWW: ", fileinput.files);
    console.log("FILE INPUT TRIGGERED");
    let area = document.getElementById('area');
    let files = event.target.files;
    area.textContent = '';
    for(let i=0; i<(files.length); i++){
        filesInArea.push(files[i]);
        let filename = document.createElement('p');
        filename.textContent ='- ' + files[i].name;
        filename.style.color = 'gray';
        filename.style.margin = '5px';
        filename.style.fontSize = '15px';
        area.appendChild(filename);
    }
    console.log("FILES IN AREA: ", filesInArea);
} );




// COPY THE TEXT OF TEXTAREA
    let copytext = document.getElementById('copyBtn');
    copytext.addEventListener("click", () => {
    const texts = document.getElementById('textBox3').value;
    navigator.clipboard.writeText(texts).then(() => {
        copytext.textContent = "text copied!";
        setTimeout(() =>{
            copytext.textContent = "Copy text";
        }, 3000);
    }).catch(err => {
        console.error('Failed to copy link: ', err);
    });
});




});


function debounce(func, delay) {
    let timeoutId; // Variable to store the timeout ID
    return function(...args) { // Return a new function that will be called in place of the original function
      clearTimeout(timeoutId); // Clear any previously set timeout to reset the delay
      timeoutId = setTimeout(() => { // Set a new timeout
        func.apply(this, args); // Call the original function with the context and arguments
      }, delay); // Delay in milliseconds
    };
  };






//GET THE PUBLIC IP ADDRESS

/* async function checkIP(){
    try{
        let response = await fetch('https://api.ipify.org?format=json');
        let data = await response.json();
        let thisAddress = data.ip;
        return thisAddress;
    }
    catch(error){
        console.error("THE ERROR: ", error);
    }
    
} */

 function checkIP(text){
    console.log("CheckIP TRIGGERD");
    fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        sendIP(data.ip, text);
    })
    .catch(error => {
        console.log('Error:', error);
    });
};

//SEND TEXT AND IP TO SERVER
function sendIP(address, text){
    fetch(ip_url, {
        method : "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken3,
        },
        body: JSON.stringify({
            'ip':address,
            'text':text,
        })
    })
    .then( response => response.json() )
    .then(data => {
        // console.log(data.reply);
        // console.log(data.network);
        // console.log(data.device);
        // console.log(data.latest);
    })
}