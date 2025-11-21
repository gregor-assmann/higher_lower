function getPreferredTheme() {
    if(localStorage.getItem("theme")){
        return localStorage.getItem("theme")
    }
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        localStorage.setItem("theme", "dark")
        return 'dark';
    } else {
        localStorage.setItem("theme", "light")
        return 'light';
    }
}

localTheme = getPreferredTheme()
document.documentElement.setAttribute('data-theme', localTheme);
document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelector(".mode-img").src = "static/images/" + localTheme + "-mode.png"
    document.querySelectorAll(".stat-frame").forEach(e => {
        e.src = e.src.replace("dark", localTheme)
    })
});



function toggleTheme(){
    
    currentTheme = localStorage.getItem("theme")

    if(currentTheme == "dark"){
        localStorage.setItem("theme", "light")
        document.querySelector(".mode-img").src = "static/images/light-mode.png"
        document.documentElement.setAttribute('data-theme', 'light');
        document.querySelectorAll(".stat-frame").forEach(e => {
        e.src = e.src.replace("dark", "light")
    })
    } else {
        localStorage.setItem("theme", "dark")
        document.querySelector(".mode-img").src = "static/images/dark-mode.png"
        document.documentElement.setAttribute('data-theme', 'dark');
        document.querySelectorAll(".stat-frame").forEach(e => {
        e.src = e.src.replace("light", "dark")
    })
    }
}