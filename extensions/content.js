const list = []

const myBody = document.body

const config = { attributes: true, childList: true, subtree: true }

console.log("Cyber Twin is working...")

const callback = (mutationList, observer) => {

    for (const mutation of  mutationList) {
        if (mutation.type === "childList") {
            for (let node of mutation.addedNodes) {
                if (node.nodeType === Node.ELEMENT_NODE) {
                    if (node.matches('[data-testid^="tweetTextarea"]')) {
                        list.push(node)
                        console.log("Found compose box directly:", node)
                }
                    else {
                        const targetInput = node.querySelector?.('[data-testid^="tweetTextarea"][role="textbox]');
                        if (targetInput) {
                        console.log("Found compose box indirectly:", targetInput)

                        }
                    }
            }
        }
    }
}}


const mutattionObserver = new MutationObserver(callback)
mutattionObserver.observe(myBody,config)

// {
//   type: "childList",               // "childList" | "attributes" | "characterData"
//   target: HTMLDivElement,          // The parent element where the change happened
//   addedNodes: NodeList [           // List of newly added DOM nodes
//     HTMLDivElement                 // Actual DOM Node object (e.g., <div data-testid="tweetTextarea_0">)
//   ],
//   removedNodes: NodeList [],       // List of removed DOM nodes (empty here)
//   previousSibling: HTMLDivElement, // Sibling immediately preceding the added node, or null
//   nextSibling: null,               // Sibling immediately following the added node, or null
//   attributeName: null,             // Name of modified attribute (only if type === "attributes")
//   attributeNamespace: null,        // Namespace of modified attribute, or null
//   oldValue: null                   // Previous attribute value (if returnOldValue was configured)
// }
