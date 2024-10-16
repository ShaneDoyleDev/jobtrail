
const hamburger = document.getElementById('hamburger');
const menu = document.getElementById('menu');
var lis = document.querySelectorAll('#menu li');
let isOn = false;



hamburger.addEventListener("click", () => {
    if (!isOn) {
        console.log('Turning on')
        menu.classList.add("nav-right-mobile-active");
        for (var i = 0; i < lis.length; i++) {
            lis[i].classList.add('active')
            lis[i].classList.remove('hidden')
        }
        isOn = true;
    }
    else {
        menu.classList.remove("nav-right-mobile-active");
        for (var i = 0; i < lis.length; i++) {
            lis[i].classList.add('hidden')
            lis[i].classList.remove('active')
        }
        isOn = false;
    }
}) 
