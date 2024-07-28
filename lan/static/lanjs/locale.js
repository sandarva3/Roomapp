document.addEventListener("DOMContentLoaded", ()=> {
    const loading = document.getElementById('loading');
    const done = document.getElementById('done');
    loading.style.display = "none";
    done.style.display = "none";

    //WHEN CHANGES ARE MADE IN TEXTAREA
    let textBox = document.getElementById('textBox');
    const debouncedCheckIP = debounce(checkIP, 650);

    textBox.addEventListener("input", function(){
        done.style.display = "none";
        loading.style.display = "block";
    const textValue = textBox.value;
    // checkIP(textValue);
    debouncedCheckIP(textValue);
});


// COPY THE TEXT OF TEXTAREA
    let copytext = document.getElementById('copyBtn');
    copytext.addEventListener("click", () => {
    const texts = document.getElementById('textBox').value;
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

    


let filesInArea = [];




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
        document.getElementById('loading').style.display = "none";
        document.getElementById('done').style.display = "block";
        // console.log(data.reply);
        // console.log(data.network);
        // console.log(data.device);
        // console.log(data.latest);
    })
}