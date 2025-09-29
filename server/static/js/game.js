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
var correctAudio = new Audio('/static/sounds/mixkit-correct-answer-tone-2870.wav');
var wrongAudio = new Audio('/static/sounds/mixkit-wrong-answer-fail-notification-946.wav');

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
        product2.childNodes[3].childNodes[3].href = response.productLast_link
        product2.childNodes[3].childNodes[3].title = 'Gehe zum Produkt'
        //console.log(response)
        if (response.correct) {
            overrideCheckmark = false
            let pos1X = getOffset(product1).x
            let pos2X = getOffset(product2).x
            let offsetX = pos1X - pos2X
            let pos1Y = getOffset(product1).y
            let pos2Y = getOffset(product2).y
            let offsetY = pos1Y - pos2Y
            displayCorrect();
            animateNewProduct(offsetX, offsetY, response);
            correctAudio.play();
            
        }
        else {
            displayWrong();
            wrongAudio.play();
            game_over(response);
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
                        <a target="_blank" rel="noopener noreferrer">${response.productNext_name}</a>
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

    // Klick auf die Produktboxen
    product1.addEventListener('click', send_guess);
    product2.addEventListener('click', send_guess);

    // Verhindere, dass Klicks auf Links send_guess auslösen
    const product1Link = product1.querySelector('.text-box a');
    if (product1Link) {
        product1Link.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }

    const product2Link = product2.querySelector('.text-box a');
    if (product2Link) {
        product2Link.addEventListener('click', function(event) {
            event.stopPropagation();
        });
    }
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

function game_over(response) {
    product1.removeEventListener('mouseenter', enter_rotate);
    product1.removeEventListener('mouseleave', leave_rotate);
    product1.removeEventListener('click', send_guess);

    product2.removeEventListener('mouseenter', enter_rotate);
    product2.removeEventListener('mouseleave', leave_rotate);
    product2.removeEventListener('click', send_guess);
}

function displayCorrect(){
    arrow.style.display= "none"
    correct.style.display = "block"
    logobig.style.display = "none"

    //remove listeners to avoid clicks during animation
    product1.removeEventListener('mouseenter', enter_rotate);
    product1.removeEventListener('mouseleave', leave_rotate);
    product1.removeEventListener('click', send_guess);

    product2.removeEventListener('mouseenter', enter_rotate);
    product2.removeEventListener('mouseleave', leave_rotate);
    product2.removeEventListener('click', send_guess);
}

function animateNewProduct(offsetX, offsetY, response){
    setTimeout(() => {
            product1.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
            product2.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
                setTimeout(() => {
                load_next_product(response);
                product2.style.transform = `translate(${-offsetX}px, ${-offsetY}px)`;
                product1.style.transform = `translate(0px, 0px)`;
                setTimeout(() => {
                    product2.style.transform = `translate(0px, 0px)`;
                    overrideCheckmark = true
                    correct.style.display = "none"
                    arrow.style.display = "block"


                    //add back listeners
                    product1.addEventListener('mouseenter', enter_rotate);
                    product1.addEventListener('mouseleave', leave_rotate);
                    product1.addEventListener('click', send_guess);

                    product2.addEventListener('mouseenter', enter_rotate);
                    product2.addEventListener('mouseleave', leave_rotate);
                    product2.addEventListener('click', send_guess);

                },10);
                },500);
            }, 1000);
}

function displayWrong(){
    arrow.style.display= "none";
    wrong.style.display = "block";
    score_display.style.zoom = window.innerWidth > 600 ? 1.4 : 1;
    return_button.style.display = 'block'
    game_over_display.style.display= 'flex'

}

function getOffset(el) {
  const rect = el.getBoundingClientRect();
  return {
    x: rect.left + window.scrollX,
    y: rect.top + window.scrollY
  };
}