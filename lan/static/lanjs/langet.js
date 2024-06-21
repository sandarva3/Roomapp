/* function getLocalIPs(callback) {
    const ips = [];
    const pc = new RTCPeerConnection({iceServers: []});
    pc.createDataChannel('');
    pc.createOffer().then(offer => pc.setLocalDescription(offer));
    pc.onicecandidate = (ice) => {
        if (!ice || !ice.candidate) return;
        const parts = ice.candidate.candidate.split(' ');
        const ip = parts[4];
        if (!ips.includes(ip) && ip.match(/^(192\.168|10\.|172\.(1[6-9]|2[0-9]|3[0-1]))/)) {
            ips.push(ip);
            callback(ip);
        }
    };
}

getLocalIPs((ip) => {
    console.log('Local IP Address:', ip);
});  */