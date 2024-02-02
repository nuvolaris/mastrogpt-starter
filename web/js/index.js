// global variables
let chat = document.getElementById("chat").contentWindow;
let display = document.getElementById("display").contentWindow;

//TODO dot env
const config = {
  clientId:
    "50639526067-dma0d7nqjeof22hboq3cv5j5e8kc0g75.apps.googleusercontent.com",
  redirectUri: "https://zany-dollop-59x95qxx4q7cqgj-8080.app.github.dev/",
};

document
  .getElementById("google-auth-button")
  .addEventListener("click", function () {
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

document.addEventListener("DOMContentLoaded", async function () {
  try {
    const code = getUrlParameter("code");
    removeParameters(["code", "scope"]);
    const base = location.href.replace(/index\.html$/, "");

    if (code) {
      console.log("Calling display to post message");
      await displayLoader();
      console.log("Display OK, starting Google Flow");
      startGoogleFlow(code);
    }
    const data = await fetchIndex(base + "api/my/mastrogpt/index");
    console.log(data);

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

function displayLoader() {
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

async function fetchIndex(url) {
  const response = await fetch(url);
  return response.json();
}

function createServiceButton(base, service) {
  const button = document.createElement("button");
  button.textContent = service.name;
  button.onclick = function () {
    const url = base + "api/my/" + service.url;
    chat.postMessage({ name: service.name, url: url });
  };
  const span = document.createElement("span");
  span.appendChild(button);
  return span;
}

function removeParameters(parametersToRemove) {
  var newUrl = window.location.href;
  parametersToRemove.forEach((parameter) => {
    newUrl = newUrl.replace(new RegExp("[?&]" + parameter + "=([^&#]*)"), "");
  });
  history.replaceState({}, document.title, newUrl);
}

function startGoogleFlow(code) {
  const params = {
    code: code,
  };

  let base = location.href.replace(/index\.html$/, "");

  const urlWithParams = new URL(base + "api/my/google/token");
  urlWithParams.search = new URLSearchParams(params).toString();

  fetch(urlWithParams)
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      getEvents(data.token)
        .then((events) => {
          askEventsDescription(events);
        })
        .catch((error) => {
          console.error("Error retrieving events:", error);
        });
    })
    .catch((e) => {
      console.error(e);
      alert("ERROR: cannot load token");
    });
}

function getEvents(token) {
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

  return fetch(url, { headers })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((responseData) => {
      const items = responseData.items.map((item) => ({
        start: item.start.dateTime,
        end: item.end.dateTime,
        organizer: item.organizer.email,
        summary: item.summary,
      }));
      return items;
    })
    .catch((error) => {
      console.error("Error during the events call:", error);
      throw error;
    });
}

function askEventsDescription(events) {
  let base = location.href.replace(/index\.html$/, "");

  const url = base + "api/my/google/description";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      input: events,
    }),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      if (data.output) {
        display.postMessage({ type: "message", message: data.output }, "*");
      }
    })
    .catch((error) => {
      display.postMessage(
        {
          type: "message",
          message: '<div id="error">Error loading description</div>',
        },
        "*"
      );
      console.error(error);
      alert("ERROR: cannot load description");
    });
}
