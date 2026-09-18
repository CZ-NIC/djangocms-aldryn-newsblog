const addArticlesintoForm = (data) => {
    const arricles = document.querySelector(".field-related .sortedm2m-items")
    data.articles.forEach((item, i) => {
        const li = document.createElement("li")
        arricles.appendChild(li)
        li.classList.add("sortedm2m-item")
        const label = document.createElement("label")
        li.appendChild(label)
        label.for = `id_related_${i}`
        const input = document.createElement("input")
        label.appendChild(input)
        input.type = "checkbox"
        input.value = item[0]
        input.id = `id_related_${i}`
        input.classList.add("sortedm2m")
        label.appendChild(document.createTextNode(" "))
        label.appendChild(document.createTextNode(item[1]))
    })
    const hidden = document.querySelector(".field-related input[type=hidden]")
    if (hidden) {
        hidden.name = "related"
    }
}


const fetchRelatedArticles = () => {
    const related_arricles = document.querySelector(".field-related .sortedm2m-items")
    const node = document.getElementById("fetch-related-articles")
    if (!(node && related_arricles)) {
        return
    }
    const buttons = document.querySelectorAll("#article_form input[type=submit]")
    buttons.forEach((btn, i) => {btn.disabled = true})
    fetch(node.dataset.endpoint, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`)
                }
                return response.json()
            })
            .then(addArticlesintoForm)
            .catch(error => {
                console.error('Fetch error:', error)
            })
            .finally(() => {
                buttons.forEach((btn, i) => {btn.disabled = false})
            })
}

document.addEventListener("DOMContentLoaded", fetchRelatedArticles)
