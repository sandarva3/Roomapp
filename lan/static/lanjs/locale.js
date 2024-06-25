document.addEventListener("DOMContentLoaded", ()=> {
    const loading = document.getElementById('loading');
    const done = document.getElementById('done');
    loading.style.display = "none";
    done.style.display = "none";
    form3 = document.getElementById('form3');
    console.log("FORM 3");

    //WHEN CHANGES ARE MADE IN TEXTAREA
    let textInput = document.getElementById('textinput');
    textInput.addEventListener("input", function(){
        done.style.display = "none";
        loading.style.display = "block";
    const textValue = textInput.value;
    checkIP(textValue);

});

    form3.addEventListener('submit', function(event){
    event.preventDefault();
    getIP();
    setTimeout(() => {
        this.submit();
    }, (700));
});

// COPY THE TEXT OF TEXTAREA
    let copytext = document.getElementById('copyBtn');
    copytext.addEventListener("click", () => {
    const texts = document.getElementById('textinput').value;
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
    

function getIP(){
    fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        document.getElementById('addr').value = data.ip;
    })
    .catch(error => {
        console.log('Error:', error);
    });
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
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify({
            'data':"Here I'm trying to send IP address",
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