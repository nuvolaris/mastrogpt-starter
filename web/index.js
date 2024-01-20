let chat = document.getElementById("chat").contentWindow

chat.addEventListener("load", function() { 
    chat.postMessage({name: "No Chat", url: null})
    console.log("posted No Chat")
})

document.addEventListener("DOMContentLoaded", function() {

    // retrieve 
    let base = location.href.replace(/index\.html$/, "")
    fetch(base+"api/my/mastrogpt/index")
    .then( (x)  => x.json())
    .then( (data) => {
        console.log(data)
        let insert = document.getElementById("top-area")
        data.services.forEach(service => {
            const button = document.createElement("button");
            button.textContent = service.name;
            button.onclick = function() {
                chat.postMessage({name: service.name, url: service.url})
            };
            let = p = document.createElement("p")
            p.appendChild(button);
            insert.appendChild(p);
            console.log("posted "+service.name)
        });
    })
    .catch( (e) => { console.log(e); alert("ERROR: cannot load index") } )
})
