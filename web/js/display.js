// receive messages and forward to the display method
window.addEventListener('message', async function(ev) {
    let data = ev.data
    //console.log(data);
    fetch("/api/my/mastrogpt/display", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(r => r.text())
    .then(t => {
        if(t !=  "") {
            let content =  document.getElementById("_display_container_");
            content.innerHTML = t;

            // Trova tutti gli elementi script nell'HTML appena inserito
            const scriptElements = content.getElementsByTagName('script');

            // Esegui ciascuno script
            for (let i = 0; i < scriptElements.length; i++) {
                console.log("Running script", i)
                const script = scriptElements[i].innerText || scriptElements[i].textContent;
                new Function(script)();
            }

            
        }
    })
    .catch(e => {
        let content =  document.getElementById("_display_container_");

        content.innerHTML="<h1>Error!</h1><p>Check logs for details.</p>"
        console.log(e)
    })
})
