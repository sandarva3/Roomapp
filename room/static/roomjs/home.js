document.addEventListener('DOMContentLoaded', (event) => {

    let copyCode = document.getElementById('copyCode');
    copyCode.addEventListener('click', () => {
        const text = document.getElementById('roomcode').textContent;
        navigator.clipboard.writeText(text).then(() => {
            copyCode.textContent = "Copied !";
            setTimeout(() => {
                copyCode.textContent = "Copy code";
            }, 3000);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
        });
    });

    let copyUrl = document.getElementById('copyUrl');
    copyUrl.addEventListener("click", () => {
        const link = document.getElementById('roomlink').textContent;
        navigator.clipboard.writeText(link).then(() => {
            copyUrl.textContent = "link copied!";
            setTimeout(() =>{
                copyUrl.textContent = "Copy link";
            }, 3000);
        }).catch(err => {
            console.error('Failed to copy link: ', err);
        });
    });
});
// var currentUrl = window.location.href;
// if(currentUrl === "")

// function submitBtnclick(boxs){
//     box = document.getElementById(boxs);
//     box.style.display = "block";
//     console.log("The function has been triggered.");
// }

let fileinput = document.getElementById('fileinput');
fileinput.addEventListener('change', function(event){
    console.log("TRIGGERED");
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
} )