
// receive messages and forward to the display method
window.addEventListener('message', async function(ev) {
    let data = ev.data
    console.log(data);
    fetch("/api/my/mastrogpt/display", {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(r => r.text())
    .then(t => {
        //console.log(t)
        if(t !=  "") {
            let content =  document.getElementById("_display_container_");
            content.innerHTML = t;
            let scripts = content.getElementsByTagName("script")
            for(let script of scripts)
                eval(script.text)
        }
    })
    .catch(e => {
        content.innerHTML="<h1>Error!</h1><p>Check logs for details.</p>"
        console.log(e)
    })
})
