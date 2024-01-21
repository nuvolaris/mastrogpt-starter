let chat = document.getElementById("chat").contentWindow
let display = document.getElementById("display").contentWindow

chat.addEventListener("load", function() { 
    chat.postMessage({name: "No Chat", url: null})
    console.log("posted No Chat")
})

document.addEventListener("DOMContentLoaded", function() {

    // retrieve index
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
                let url = base + "api/my/"+service.url
                chat.postMessage({name: service.name, url: url})
            };
            let = p = document.createElement("span")
            p.appendChild(button);
            insert.appendChild(p);
            console.log("posted "+service.name)
        });
    })
    .catch( (e) => { console.log(e); alert("ERROR: cannot load index") } )
})
