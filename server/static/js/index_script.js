document.addEventListener("DOMContentLoaded", (event) => {
    difficulties = document.querySelectorAll(".difficulty input").forEach((e) => e.addEventListener("change", show_selected_board));
    show_selected_board();
});

function show_selected_board() {
    difficulties = document.querySelectorAll(".difficulty input");
    leaderboards = document.querySelectorAll(".leaderboard-container");

    leaderboards.forEach((e) => e.classList.add("hidden"));
    difficulties.forEach((e, i) => {
        if (e.checked) {
            leaderboards[i].classList.remove("hidden");
            own_place = document.querySelector(".leaderboard-element-player");
            console.log(e.value);
            console.log(own_place.getAttribute("data-name"));
            if (e.value == own_place.getAttribute("data-name")) {
                own_place.classList.remove("hidden");
            }
            else {
                own_place.classList.add("hidden");
            }
        }
    });
}

function getPreferredTheme() {
    if(localStorage.getItem("theme")){
        console.log("from storage")
        return localStorage.getItem("theme")
    }
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        localStorage.setItem("theme", "dark")
        console.log("from system")
        return 'dark';
    } else {
        localStorage.setItem("theme", "light")
        return 'light';
    }
}

localTheme = getPreferredTheme()
console.log(localTheme)
document.documentElement.setAttribute('data-theme', localTheme);
document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelector(".mode-img").src = "static/images/" + localTheme + "-mode.png"
});



function toggleTheme(){
    
    currentTheme = localStorage.getItem("theme")

    if(currentTheme == "dark"){
        localStorage.setItem("theme", "light")
        document.querySelector(".mode-img").src = "static/images/light-mode.png"
        document.documentElement.setAttribute('data-theme', 'light');
    } else {
        localStorage.setItem("theme", "dark")
        document.querySelector(".mode-img").src = "static/images/dark-mode.png"
        document.documentElement.setAttribute('data-theme', 'dark');
    }

}