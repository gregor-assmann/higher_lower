var arrow = document.getElementById('arrow');
var correct = document.getElementsByClassName('check')[0]
var wrong = document.getElementsByClassName('check')[1] //muss so gemacht werden da man sonst kurz den haken sieht bei falschem guess
var logobig = document.getElementById('logobig');
var center_container = document.getElementsByClassName('center-container')[0]
var product1 = document.getElementsByClassName('product-box')[0];
var product2 = document.getElementsByClassName('product-box')[1];
var score = document.getElementsByClassName('score')[0];
var score_display = document.getElementsByClassName('score-container')[0]
var return_button = document.getElementsByClassName('return-button')[0]
var game_over_display = document.getElementsByClassName('game-over')[0]

var overrideCheckmark = true





document.addEventListener("DOMContentLoaded", (event) => {
    setup();
});

async function send_guess() {
    //console.log(this.getAttribute('user_guess'))
    await fetch("/guess", {
        method: 'POST',
        redirect: 'follow',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ guess: this.getAttribute('user_guess') })
    }).then(response => {
        console.log(response.status)
        if (response.redirected) {
            window.location.href = response.url;
        }
        return response.json();
    }).then(response => {
        document.querySelectorAll('.price')[1].textContent = `Preis: ${response.productLast_price} €`
        //console.log(response)
        if (response.correct) {
            overrideCheckmark = false
            let pos1 = getOffset(product1)
            let pos2 = getOffset(product2)
            let offset = pos1 - pos2
            displayCorrect(offset);
            animateNewProduct(offset, response);
            
        }
        else {
            displayWrong();
            game_over();
        }
    });
}

function load_next_product(response) {
    product1.remove();
    moveDown(center_container);
    product2.removeEventListener('mouseenter', enter_rotate);
    product2.removeEventListener('mouseleave', leave_rotate);
    product2.removeEventListener('click', send_guess);
    score.innerHTML = response.score + 1

    document.querySelector('.product-container').insertAdjacentHTML('beforeend', `<div class="product-box">
                    <img class="product-image" src=${response.productNext_high_q_img} alt="Produkt">
                    <div class="text-box">
                        <h2>${response.productNext_brand}</h2>
                        <a>${response.productNext_name}</a>
                        <p class="price">Preis: ${response.productNext_price} €</p>
                        <p>lieferbar - in ${response.productNext_parcel_time} Werktagen bei dir</p>
                        <img alt="Logo" class="UpLogo" src="/static/images/otto-up-logo.png">
                    </div>
                </div>`);
    setup();
}

function moveDown(element) {
  if(element.nextElementSibling)
    element.parentNode.insertBefore(element.nextElementSibling, element);
}

function insertAfter(referenceNode, newNode) {
    referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function setup() {
    arrow = document.getElementById('arrow');
    logobig = document.getElementById('logobig');
    center_container = document.getElementsByClassName('center-container')[0]
    product1 = document.getElementsByClassName('product-box')[0];
    product2 = document.getElementsByClassName('product-box')[1];
    score = document.getElementsByClassName('score')[0];
    correct = document.getElementsByClassName('check')[0]
    wrong = document.getElementsByClassName('check')[1]
    score_display = document.getElementsByClassName('score-text')[0]
    return_button = document.getElementsByClassName('return-button')[0]
    game_over_display = document.getElementsByClassName('game-over')[0]
    
    product1.setAttribute('rotation', '-180');
    product2.setAttribute('rotation', '0');

    product1.setAttribute('user_guess', 'lower');
    product2.setAttribute('user_guess', 'higher');

    // Initialzustand
    arrow.style.display = 'none';
    if (overrideCheckmark) logobig.style.display = 'block';
    wrong.style.display = 'none'
    if (overrideCheckmark) correct.style.display = "none"

    // Maus berührt ein Feld
    product1.addEventListener('mouseenter', enter_rotate);
    product2.addEventListener('mouseenter', enter_rotate);

    // Maus verlässt ein Feld
    product1.addEventListener('mouseleave', leave_rotate);
    product2.addEventListener('mouseleave', leave_rotate);

    product1.addEventListener('click', send_guess);
    product2.addEventListener('click', send_guess);
}

function enter_rotate() {
    rotation = this.getAttribute('rotation')
    arrow.style.transform = `rotate(${rotation}deg)`;
    arrow.style.display = 'block';
    logobig.style.display = 'none';
    if (overrideCheckmark) correct.style.display = "none"
}

function leave_rotate() {
    arrow.style.transform = 'rotate(-90deg)';
    arrow.style.display = 'block';
    logobig.style.display = 'none';
}

function game_over() {
    product1.removeEventListener('mouseenter', enter_rotate);
    product1.removeEventListener('mouseleave', leave_rotate);
    product1.removeEventListener('click', send_guess);

    product2.removeEventListener('mouseenter', enter_rotate);
    product2.removeEventListener('mouseleave', leave_rotate);
    product2.removeEventListener('click', send_guess);
}

function displayCorrect(offset){
    arrow.style.display= "none"
    correct.style.display = "block"
    logobig.style.display = "none"
}

function animateNewProduct(offset, response){
    setTimeout(() => {
            product1.style.transform = `translateX(${offset}px)`;
            product2.style.transform = `translateX(${offset}px)`;
                setTimeout(() => {
                load_next_product(response);
                product2.style.transform = `translateX(${-offset}px)`;
                product1.style.transform = `translateX(0px)`;
                setTimeout(() => {
                    product2.style.transform = `translateX(0px)`;
                    overrideCheckmark = true
                    correct.style.display = "none"
                    arrow.style.display = "block"
                },10);
                },500);
            }, 1000);
}

function displayWrong(){
    arrow.style.display= "none";
    wrong.style.display = "block";
    score_display.style.zoom = 1.4;
    return_button.style.display = 'block'
    game_over_display.style.display= 'flex'

}

function getOffset(el) {
  const rect = el.getBoundingClientRect();
  return rect.left + window.scrollX

}