console.log("Cyber Twin is working...")

const list = []
const myBody = document.body
const config = { attributes: true, childList: true, subtree: true }
const url = "http://127.0.0.1:8000/analyze-post"


let timer

const input_return = (event) => {
    clearTimeout(timer)
    timer = setTimeout(async () => { 
        const users_input = event.target.innerText
        list.push(users_input)

        chrome.runtime.sendMessage({action: "ANALYZE_TEXT", payload: users_input},
            (response) => {
                if (!(document.getElementById('cyber-twin-response'))) {
                const twinResponse = document.createElement('div');
                twinResponse.style.cssText = "position: fixed; top: 24px; right: 24px; z-index: 999999; opacity: 0.88; background-color: #121212; color: #00ffcc; border: 1px solid #00ffcc; padding: 16px; border-radius: 16px; max-width: 400px; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5); white-space: pre-wrap; font-family: monospace; font-size: 18px;"
                twinResponse.className = 'cyber-twin-assessment';
                twinResponse.id = 'cyber-twin-response'
                twinResponse.innerText = response?.assessment
                document.body.appendChild(twinResponse)

                console.log("Assessment from Cyber Twin:", response?.assessment)

                }
            }
        )
        },500)

    }

const callback = (mutationList, observer) => {


    for (const mutation of  mutationList) {
        if (mutation.type === "childList") {
            for (let node of mutation.addedNodes) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    if (node.matches('[data-testid^="tweetTextarea"][role="textbox"]')) {
                        node.addEventListener('input',input_return)
                        list.push(node)
                }
                    else {
                        const targetInput = node.querySelector?.('[data-testid^="tweetTextarea"][role="textbox"]');
                        if (targetInput) {
                        targetInput.addEventListener('input', input_return)
                        list.push(targetInput)

                        }
                    }
            }
        }
    }
}}


const mutattionObserver = new MutationObserver(callback)
mutattionObserver.observe(myBody,config)
