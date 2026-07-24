url = "http://127.0.0.1:8000/analyze-post"

const usr_input = document.getElementById("UsrInput")
const button = document.getElementById("ScanButton")
const output = document.getElementById("Output")


button.addEventListener("click", async() => { 
    const request = new Request(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body : JSON.stringify({
            "text": usr_input.value,
            "platform" : "Web"})
    })

    const response = await fetch(request)
    const data = await response.json()
    output.innerText = data.assessment
})
