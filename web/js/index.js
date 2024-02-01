// global variables
let chat = document.getElementById("chat").contentWindow
let display = document.getElementById("display").contentWindow

function getUrlParameter(name) {
    
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

document.addEventListener("DOMContentLoaded", function() {

    var code = getUrlParameter('code');

    if (code) {
        console.log('Code:', code);

        const params = {
            code: code
        };

        removeParameters(['code', 'scope']);
        let base = location.href.replace(/index\.html$/, "");

        const urlWithParams = new URL(base + "api/my/google/token");
        urlWithParams.search = new URLSearchParams(params).toString();
        fetch(urlWithParams)
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                console.log(data);
            })
            .catch((e) => {
                console.error(e);
                alert("ERROR: cannot load token");
            });

    }


    let base = location.href.replace(/index\.html$/, "")

    // retrieve index
    fetch(base + "api/my/mastrogpt/index")
        .then((x) => x.json())
        .then((data) => {
            console.log(data);
            let insert = document.getElementById("top-area");
            data.services.forEach(service => {
                const button = document.createElement("button");
                button.textContent = service.name;
                button.onclick = function() {
                    let url = base + "api/my/" + service.url;
                    chat.postMessage({ name: service.name, url: url });
                };
                let p = document.createElement("span");
                p.appendChild(button);
                insert.appendChild(p);
                console.log("enabled " + service.name);
            });
        })
        .catch((e) => {
            console.log(e);
            alert("ERROR: cannot load index");
        });
});

function removeParameters(parametersToRemove) {
    var newUrl = window.location.href;
    parametersToRemove.forEach(parameter => {
        newUrl = newUrl.replace(new RegExp('[?&]' + parameter + '=([^&#]*)'), '');
    });
    history.replaceState({}, document.title, newUrl);
}
