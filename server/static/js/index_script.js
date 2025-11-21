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
