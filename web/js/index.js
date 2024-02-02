// global variables
let chat = document.getElementById("chat").contentWindow;
let display = document.getElementById("display").contentWindow;

//TODO dot env
const config = {
    clientId: "insert-here",
    redirectUri: "insert-here"
};

document.getElementById('google-auth-button').addEventListener('click', function() {
    window.location.href = `https://accounts.google.com/o/oauth2/auth?client_id=${config.clientId}&redirect_uri=${config.redirectUri}&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar&response_type=code`;
});

function getUrlParameter(name) {
  name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
  var regex = new RegExp("[\\?&]" + name + "=([^&#]*)");
  var results = regex.exec(location.search);
  return results === null
    ? ""
    : decodeURIComponent(results[1].replace(/\+/g, " "));
}

document.addEventListener("DOMContentLoaded", function () {
  var code = getUrlParameter("code");

  if (code) {
    console.log("Code:", code);

    if (code) {
        startGoogleFlow(code);
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
  parametersToRemove.forEach((parameter) => {
    newUrl = newUrl.replace(new RegExp("[?&]" + parameter + "=([^&#]*)"), "");
  });
  history.replaceState({}, document.title, newUrl);
}

function startGoogleFlow(code) {
    const params = {
        code: code
    };

    removeParameters(['code', 'scope']);
    let base = location.href.replace(/index\.html$/, "");

    const urlWithParams = new URL(base + "api/my/google/token");
    urlWithParams.search = new URLSearchParams(params).toString();
    
    fetch(urlWithParams)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.token);
            
            getEvents(data.token)
                .then(events => {
                    console.log('events', events);
                    askEventsDescription(events);
                
                })
                .catch(error => {
                    console.error('Error retrieving events:', error);
                });
        })
        .catch(e => {
            console.error(e);
            alert("ERROR: cannot load token");
        });
}

function getEvents(token) {
    console.log('get events');
    
    const apiUrl = 'https://www.googleapis.com/calendar/v3/calendars/primary/events';
    
    const currentDate = new Date();
    currentDate.setHours(0, 0, 0);
    const formattedStartDate = currentDate.toISOString().split('.')[0] + 'Z';
    
    currentDate.setHours(23, 59, 59);
    const formattedEndDate = currentDate.toISOString().split('.')[0] + 'Z';
    
    const headers = {
        'Authorization': 'Bearer ' + token
    };
    
    const params = new URLSearchParams({
        'timeMin': formattedStartDate,
        'timeMax': formattedEndDate
    });
    
    const url = `${apiUrl}?${params.toString()}`;
    
    return fetch(url, { headers })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(responseData => {
            const items = responseData.items.map(item => ({
                start: item.start.dateTime,
                end: item.end.dateTime,
                organizer: item.organizer.email,
                summary: item.summary
            }));
            return items;
        })
        .catch(error => {
            console.error('Error during the events call:', error);
            throw error;
        });
}


function askEventsDescription(events) {
    let base = location.href.replace(/index\.html$/, "");

    const url = base + "api/my/google/description";
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            input: events
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.output) {
            display.postMessage({ type: 'message', message: data.output }, '*');        
        } 
    })
    .catch(error => {
        console.error(error);
        alert("ERROR: cannot load description");
    });
}
