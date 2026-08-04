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
                console.log("Assessment from Ccyber Twin:", response?.assessment)
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
