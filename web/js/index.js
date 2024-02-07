// global variables
let chat = document.getElementById("chat").contentWindow
let display = document.getElementById("display").contentWindow
let base = location.href.replace(/index\.html$/, "")


// inizialize the chat buttons
document.addEventListener("DOMContentLoaded", function() {
    // retrieve index
    fetch(base+"api/my/mastrogpt/index")
    .then( (x)  => x.json())
    .then( (data) => {
        // console.log(data)
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
            console.log("enabled "+service.name)
        });
    })
    .catch( (e) => { console.log(e); alert("ERROR: cannot load index") } )
})


window.addEventListener('message', async function(ev) {
    let data = ev.data
    console.log("index.js: ricevuto un messaggio!")
    console.log(data)
    var chatframe = document.getElementById("chat")

    if (data == "Show Nodes") {
        // var chatframeDocument = chatframe.contentDocument || chatframe.contentWindow.document;

        // var inputField = chatframeDocument.getElementById("msger-input-id");
        // var form = chatframeDocument.getElementById("msger-inputarea-id")

        // inputField.value = "Show Nodes";
        
        chatframe.contentWindow.postMessage("COMMAND: Show Nodes", "*")
    } else if (data == "Show Pods") {

        chatframe.contentWindow.postMessage("COMMAND: Show Pods", "*")

    }

  })