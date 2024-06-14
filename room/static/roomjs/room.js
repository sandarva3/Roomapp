document.addEventListener('DOMContentLoaded', (event)=>{
    var copyBtn = document.getElementById('copytext');
    copyBtn.addEventListener('click', () =>{
        var text = document.getElementById('text').textContent;
        navigator.clipboard.writeText(text).then(() => {
            copyBtn.textContent = "Copied !";
            setTimeout(() => {
                copyBtn.textContent = "Copy text";
            }, 3000);
        }).catch(err => {
            console.error("Failed to copy text to clipboard.", err);
        });
    });
});