// global variables
let chat = document.getElementById("chat").contentWindow;
let display = document.getElementById("display").contentWindow;
let base = location.href.replace(/index\.html$/, "")


function getUrlParameter(name) {
    
  name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
  var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
  var results = regex.exec(location.search);
  return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}
document.addEventListener("DOMContentLoaded", async function () {
  try {
    const base = location.href.replace(/index\.html$/, "");
    const data = await fetchIndex(base + "api/my/mastrogpt/index");

    const insert = document.getElementById("top-area");
    data.services.forEach((service) => {
      const button = createServiceButton(base, service);
      insert.appendChild(button);
      console.log(`Enabled ${service.name}`);
    });
  } catch (error) {
    console.error(error);
    alert("ERROR: Cannot load index");
  }
});


async function fetchIndex(url) {
  const response = await fetch(url);
  return response.json();
}

function createServiceButton(base, service) {

    const button = document.createElement("button");
    button.textContent = service.name;    
    button.onclick = function() {
      console.log("click on ", button.textContent)

      if (button.textContent === "Calendar") {
        createServiceButtonGoogle(base);
      } 
      else {
        let url = base + "api/my/" + service.url
        chat.postMessage({name: service.name, url: url})
      }
    };
    
  const span = document.createElement("span");
  span.appendChild(button);
  return span;
}
