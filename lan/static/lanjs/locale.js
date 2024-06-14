document.addEventListener("DOMContentLoaded", ()=> {
    const loading = document.getElementById('loading');
    const done = document.getElementById('done');
    loading.style.display = "none";
    done.style.display = "none";
    let textInput = document.getElementById('textinput');
    textInput.addEventListener("input", function(){
        done.style.display = "none";
        loading.style.display = "block";
    const textValue = textInput.value;
    checkIP(textValue)
})
// console.log('value = ', hello);
})

// document.addEventListener('DOMContentLoaded', ()=> {
//     getLocalIP(function(ip){
//         sendLocalIP(ip);
//     }) 
// })

// function sendLocalIP(address, text){
//     fetch(ip_url, {
//         method : "POST",
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrf,
//         },
//         body: JSON.stringify({
//             'data':"Here I'm trying to send IP address",
//             'ip':address,
//             'text':text,
//         })
//     })
//     .then( response => response.json() )
//     .then(data => {
//         // console.log(data.reply);
//         // console.log(data.network);
//         // console.log(data.device);
//         // console.log(data.latest);
//     })
// }



function checkIP(text){
    
    fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
        // console.log("THE TEXT: ", text);
        sendIP(data.ip, text);
    })
    .catch(error => {
        console.log('Error:', error);
    });
}

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
        console.log("HELO");
        document.getElementById('loading').style.display = "none";
        document.getElementById('done').style.display = "block";
        // console.log(data.reply);
        // console.log(data.network);
        // console.log(data.device);
        // console.log(data.latest);
    })
}


// function getLocalIP(callback) {
//     var RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;
//     if (!RTCPeerConnection) {
//         return false;
//     }

//     var rtc = new RTCPeerConnection({iceServers: []});
//     rtc.createDataChannel('', {reliable: false});

//     rtc.onicecandidate = function (evt) {
//         if (evt.candidate) {
//             var ip = /([0-9]{1,3}(\.[0-9]{1,3}){3})/.exec(evt.candidate.candidate)[1];
//             callback(ip);
//             rtc.onicecandidate = null;
//         }
//     };

//     rtc.createOffer().then(function (offerDesc) {
//         rtc.setLocalDescription(offerDesc);
//     }).catch(function (e) {
//         console.warn("Offer failed: ", e);
//     });

//     return true;
// }