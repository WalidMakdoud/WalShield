async function loadArpData() {
    

    const response = await fetch("http://127.0.0.1:8000/arp");
    const devices = await response.json();
    const table = document.getElementById("arptable");
    table.innerHTML = "";

    devices.array.forEach(device => {
        
        const row = `
            <tr>
                <td>${device.ip}</td>
                <td>${device.mac}</td>
            
            </tr>
        
        `;

        table.innerHTML += row;
    });

}

loadArpData();