
/*!
    * Start Bootstrap - SB Admin v7.0.7 (https://startbootstrap.com/template/sb-admin)
    * Copyright 2013-2023 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-sb-admin/blob/master/LICENSE)
    */
    // 
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }
})


const hamburger = document.getElementById('hamburger');
const menu = document.getElementById('menu');
var lis = document.querySelectorAll('#menu li');
let isOn = false;



hamburger.addEventListener("click", () => {
    console.log('i love hamburgers')
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
        hamburger.classList.add('active');
        isOn = false;
    }
}) 