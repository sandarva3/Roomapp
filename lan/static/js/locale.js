document.getElementById('copyBtn').addEventListener('click', function() {
    var textArea = document.getElementById('textArea');
    textArea.select();
    document.execCommand('copy');
    alert('Text copied to clipboard');
});

document.getElementById('shareBtn').addEventListener('click', function() {
    var textArea = document.getElementById('textArea');
    if (navigator.share) {
        navigator.share({
            text: textArea.value
        }).then(() => {
            console.log('Text shared successfully');
        }).catch((error) => {
            console.error('Error sharing text', error);
        });
    } else {
        alert('Share API not supported in this browser');
    }
});
