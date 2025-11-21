const ids = [
    "7990e121-9aeb-4d80-8318-0eea4fa07cd5",
    "61fade10-a3b7-4b57-bd1f-4ba96c255ce9",
    "26b0eb0e-e14e-4ba6-a333-ab822dccce4e",
    "33f89376-2f1e-4975-846e-add002508888",
    "dbdb5234-bdb4-4ec6-849c-e726e15473f4"

]

function generateStatTiles(ids){
    let container = document.querySelector(".stat-container")

    for(let i = 0; i<ids.length; i++){
        container.insertAdjacentHTML("beforeend",
            `<iframe 
                class="stat-frame"
                src="https://charts.mongodb.com/charts-project-0-btywdyw/embed/charts?id=${ids[i]}&maxDataAge=14400&theme=dark&attribution=false">
            </iframe>`
        )
        console.log("Appended: " + ids[i])
    }
}

document.addEventListener("DOMContentLoaded", (event) => {
    generateStatTiles(ids);
});
