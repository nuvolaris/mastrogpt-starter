// global variables
let token;
let calendarEvents;
let htmlEvents;

//TODO dot env
const config = {
  clientId:
    "50639526067-dma0d7nqjeof22hboq3cv5j5e8kc0g75.apps.googleusercontent.com",
  redirectUri: "https://zany-dollop-59x95qxx4q7cqgj-8080.app.github.dev/",
};


document.addEventListener("DOMContentLoaded", async function () {
  try {
    const code = getUrlParameter("code");
    removeParameters(["code", "scope"]);

    if (code) {
      await displayLoader();
      await startGoogleFlow(code);
    }

  } catch (error) {
    console.error(error);
    alert("ERROR: Cannot load index");
  }
});

function getUrlParameter(name) {
    
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

async function displayLoader() {
  return new Promise((resolve) => {
    setTimeout(() => {
      display.postMessage(
        { type: "html", html: '<h1 id="loader">Loading...</h1>' },
        "*"
      );
      resolve();
    }, 100);
  });
}

function createServiceButtonGoogle(base) {
    
    if (token)
        getEvents(token)
          .then((events) => {
            calendarEvents = events;
            //let base = location.href.replace(/index\.html$/, "");
            // const url = base + "api/my/google/human_events";
            askEventsDescription(events);
          })
          .catch((error) => {
            console.error(
              "Si è verificato un errore durante il recupero degli eventi:",
              error
            );
          });
      else {
        const url = `https://accounts.google.com/o/oauth2/auth?client_id=${config.clientId}&redirect_uri=${config.redirectUri}&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcalendar&response_type=code`;
        window.location.href = url;
      }

      const url = base + "api/my/openai/chat";

      chat.postMessage({ name: 'calendar', url: url });
  
};



function removeParameters(parametersToRemove) {
  var newUrl = window.location.href;
  parametersToRemove.forEach((parameter) => {
    newUrl = newUrl.replace(new RegExp("[?&]" + parameter + "=([^&#]*)"), "");
  });
  history.replaceState({}, document.title, newUrl);
}
async function startGoogleFlow(code) {
  const params = {
    code: code,
  };

  let base = location.href.replace(/index\.html$/, "");

  const urlWithParams = new URL(base + "api/my/google/token");
  urlWithParams.search = new URLSearchParams(params).toString();

  try {
    const response = await fetch(urlWithParams);

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const data = await response.json();
    token = data.token;
    const events = await getEvents(data.token);
    askEventsDescription(events);
  } catch (e) {
    console.error(e);
    alert("ERROR: cannot load token");
  }
}

async function getEvents(token) {
  const apiUrl =
    "https://www.googleapis.com/calendar/v3/calendars/primary/events";

  const currentDate = new Date();
  currentDate.setHours(0, 0, 0);
  const formattedStartDate = currentDate.toISOString().split(".")[0] + "Z";

  currentDate.setHours(23, 59, 59);
  const formattedEndDate = currentDate.toISOString().split(".")[0] + "Z";

  const headers = {
    Authorization: "Bearer " + token,
  };

  const params = new URLSearchParams({
    timeMin: formattedStartDate,
    timeMax: formattedEndDate,
  });

  const url = `${apiUrl}?${params.toString()}`;

  try {
    const response = await fetch(url, { headers });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const responseData = await response.json();

    const items = responseData.items.map((item) => ({
      start: item.start.dateTime,
      end: item.end.dateTime,
      organizer: item.organizer.email,
      summary: item.summary,
    }));

    calendarEvents = items;
    window.calendarEvents = calendarEvents;

    return Promise.resolve(items);
  } catch (error) {
    console.error("Error during the events call:", error);
    return Promise.reject(error);
  }
}
function askEventsDescription(events) {
  let base = location.href.replace(/index\.html$/, "");

  const url = base + "api/my/google/html_events";
  
  fetch(url, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          events
      })
  })
  .then(response => {
      if (!response.ok) {
          throw new Error('Network response was not ok');
      }
      return response.json();
  })
  .then(data => {
      try {
          let base = location.href.replace(/index\.html$/, "");

          const url = base + "api/my/google/human_events";
          const description = "describe these events in human terms";
          const combinedMessage = JSON.stringify({
              description: description,
              events: events
          });
          chat.postMessage({ name: 'Calendar', url: url, calendarEvent: combinedMessage });       
      } catch (error) {
          console.log("error on post message calendar", error);
      }

      return data;
  })
  .then(data => {
      if (data.output) {
          htmlEvents = data.output;
          display.postMessage({ type: 'html', html: data.output }, '*');
      } 
      return data;
  })
  .catch(error => {
      display.postMessage({ type: 'html', html: '<div id="error">Error loading description</div>' }, '*');
      console.error(error);
      alert("ERROR: cannot load description");
  });
}

window.createServiceButtonGoogle = createServiceButtonGoogle;
