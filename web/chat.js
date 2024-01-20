// Globals
let invoker = undefined

// Constants
const BOT_IMG = "robot-mini.png";
const PERSON_IMG = "human-mini.png";
const BOT_NAME = "BOT";
const PERSON_NAME = "YOU";

const msgerForm  =  document.querySelector(".msger-inputarea");
const msgerInput = document.querySelector(".msger-input");
const msgerChat = document.querySelector(".msger-chat");
const titleChat = document.getElementById("chat-title");
const areaChat = document.getElementById("chat-area");

// Classes
class Invoker {

  constructor(name, url) {
      this.name = name
      this.url = url
      this.state = null
  }

  async invoke(msg) {
      // welcome message no input
      if(msg == null) {
          return "Welcome, you have selected "+this.name;
      }
      // no url 
      if(this.url == null) 
          return "Welcome, please select the chat application you want to use by clicking a  button on top.";
      // prepare a request
      let json = {
        input: msg
      }
      if(this.state != null) {
        json['state'] = this.state
      }
      // send the request
      let self = this;
      return fetch(this.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json'},
        body: JSON.stringify(json)
      })
      .then(r => r.json())
      .then(r => {
        console.log(r)
        this.state = r.state 
        return r.output
      })
      .catch(e => {
          console.log(e)
          return `ERROR interacting with ${this.url}`
      })
  }
}

function formatDate(date) {
    const h = "0" + date.getHours();
    const m = "0" + date.getMinutes();
    return `${h.slice(-2)}:${m.slice(-2)}`;
}
  

function appendMessage(name, img, side, text) {
  //   Simple solution for small apps
  const msgHTML = `
    <div class="msg ${side}-msg">
      <div class="msg-img" style="background-image: url(${img})"></div>

      <div class="msg-bubble">
        <div class="msg-info">
          <div class="msg-info-name">${name}</div>
          <div class="msg-info-time">${formatDate(new Date())}</div>
        </div>

        <div class="msg-text">${text}</div>
      </div>
    </div>
  `;

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
}

function bot(msg) {
  appendMessage(BOT_NAME, BOT_IMG, "left", msg);
}

function human(msg) {
  appendMessage(PERSON_NAME, PERSON_IMG, "right", msg);
  msgerInput.value = "";
}


msgerForm.addEventListener("submit", event => {
  event.preventDefault();

  const input = msgerInput.value;
  if (!input) return;

  human(input);

  if(invoker) {
    invoker.invoke(input).then(reply => bot(reply))
  } else {
    bot("Did you select a chat?")
  }
});


window.addEventListener('message', async function(ev) {
  console.log(ev);
  invoker = new Invoker(ev.data.name, ev.data.url)
  titleChat.textContent = ev.data.name
  areaChat.innerHTML = ""
  bot(await invoker.invoke(null))
})
