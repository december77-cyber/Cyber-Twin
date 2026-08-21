const usr_input = document.getElementById("UsrInput")
const button = document.getElementById("ScanButton")
const output = document.getElementById("Output")


document.addEventListener('DOMContentLoaded', async() => {
    const result = await chrome.storage.local.get(['latestAssessment'])
    console.log(result)

    // const response = await fetch(request)
    const data = await result
    output.innerHTML = data.latestAssessment



})