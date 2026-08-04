const url = "http://127.0.0.1:8000/analyze-post"

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action == "ANALYZE_TEXT") {
        const usr_input = message.payload

        const api_fetch = async() => {
            const request = new Request(url, {
                method: "POST",
                headers: {"Content-Type": "application/json", "Cyber-Twin-Key": "skibidi"},
                body : JSON.stringify({
                    "text": usr_input,
                    "platform" : "Web"})
    })

        const response = await fetch(request)
        const data = await response.json()
        const output = data.assessment

        console.log(sender)
        chrome.storage.local.set({
            "latestAssessment": output,
            "lastUpdated": Date()
        })
        sendResponse({success: true, assessment: output})
    }

    api_fetch()

}

    return true;

})


