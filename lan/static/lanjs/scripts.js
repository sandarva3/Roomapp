document.addEventListener("DOMContentLoaded", () => {
    // console.log("LOCAL STORAGE: ", localStorage);
    // const lightSwitches = document.querySelectorAll('.light-switch');


    //Focus textBox on loading of Page
    window.onload = () => {
        document.getElementById('textBox').focus();
    }

    const lightSwitches = document.querySelectorAll('.toggle-checkbox');
            if (localStorage.getItem('dark-mode') === 'true') {
                lightSwitches.forEach(lightSwitch => lightSwitch.checked = true);
                document.documentElement.classList.add('dark');
                document.getElementById('darkSwitch').classList.add('translate-x-full', 'bg-green-500');
            } else {
                document.documentElement.classList.remove('dark');
            }

            lightSwitches.forEach(lightSwitch => {
                lightSwitch.addEventListener('change', () => {
                    if (lightSwitch.checked) {
                        document.documentElement.classList.add('dark');
                        localStorage.setItem('dark-mode', 'true');
                        document.getElementById('darkSwitch').classList.add('translate-x-full', 'bg-green-500');
                    } else {
                        document.documentElement.classList.remove('dark');
                        localStorage.setItem('dark-mode', 'false');
                        document.getElementById('darkSwitch').classList.remove('translate-x-full', 'bg-green-500');
                    }
                });
            });


    // //DarkMode Logic
    // if (localStorage.getItem('dark-mode') === 'true') {
    //     lightSwitches.forEach(lightSwitch => lightSwitch.checked = true);
    //     document.documentElement.classList.add('dark');
    // } else {
    //     document.documentElement.classList.remove('dark');
    // }

    // lightSwitches.forEach(lightSwitch => {
    //     if(lightSwitch.checked){
    //         document.getElementById('darkSwitch').textContent = "LIGHT";
    //     }
    //     else{
    //         document.getElementById('darkSwitch').textContent = "DARK";
    //     }
    //     lightSwitch.addEventListener('change', () => {
    //         if (lightSwitch.checked) {
    //             document.documentElement.classList.add('dark');
    //             localStorage.setItem('dark-mode', 'true');
    //             document.getElementById('darkSwitch').textContent = "LIGHT";
    //         } else {
    //             document.documentElement.classList.remove('dark');
    //             localStorage.setItem('dark-mode', 'false');
    //             document.getElementById('darkSwitch').textContent = "DARK";
    //         }
    //     });
    // });

    
    
    
//TypeWriting Logic
function typeWriter(text, callback) {
let i = 0;
const textBox = document.getElementById('textBox');
textBox.placeholder = ''; // Clear placeholder before typing

function type() {
        if (i < text.length) {
            textBox.placeholder += text.charAt(i);
            i++;
            setTimeout(type, 120);
        }
        else {
            if (callback) callback();
        }
    };
    type();
};

function goBack(callback) {
    const textBox = document.getElementById('textBox');
    let i = textBox.placeholder.length;
    
    function back() {
        if (i > 0) {
            textBox.placeholder = textBox.placeholder.slice(0, i - 1);
            i--;
            setTimeout(back, 120);
        }
        else {
            if (callback) callback();
        }
    }
    back();
}

const texts = [
    'Type here...',
    'Hello World..',
    'Scroll down for Files..',
];

function processTexts(index) {
    if (index < texts.length) {
        typeWriter(texts[index], function() {
            goBack(function() {
                processTexts(index + 1); // Increment index correctly
            });
        });
    }
    else{
        index = 0;
        processTexts(index);
    }
};
processTexts(0);


//Reload Page on click of Reload Button
document.getElementById('reloadBtn').onclick = ()=>{
    window.location.reload();
};

const RoomappUrl = "http://roomapp.pythonanywhere.com/";

document.getElementById('linkedinBtn').onclick = () =>{
    const linkedinUrl = `https://www.linkedin.com/shareArticle?mini=true&url=${RoomappUrl}`;
    window.open(linkedinUrl, '_blank');
}

document.getElementById('tweetBtn').onclick = () =>{
    const twitterUrl = `https://twitter.com/intent/tweet?url=${RoomappUrl}`;
    window.open(twitterUrl, '_blank');
}

// script.js
document.getElementById('friendBtn').addEventListener('click', function() {
    document.getElementById('overlay').style.display = 'flex';
});

document.getElementById('closeBtn').addEventListener('click', function() {
    document.getElementById('overlay').style.display = 'none';
});



const supportButton = document.getElementById('support-button');
            const supportDropdown = document.getElementById('support-dropdown');

            supportButton.addEventListener('click', () => {
                supportDropdown.classList.toggle('hidden');
            });

            // Close dropdown if clicked outside
            document.addEventListener('click', (event) => {
                if (!supportButton.contains(event.target) && !supportDropdown.contains(event.target)) {
                    supportDropdown.classList.add('hidden');
                }
            });

});