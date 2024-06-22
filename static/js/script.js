let menu = document.querySelector('#menu-btn');
let navbar = document.querySelector('.navbar');

menu.onclick = () =>{
    menu.classList.toggle('fa-times');
    navbar.classList.toggle('active');
}

window.onscroll = () =>{
    menu.classList.remove('fa-times');
    navbar.classList.remove('active');
}

const contactButton = document.querySelector('.btn[href="#contact_us"]');
contactButton.addEventListener('click',()=>{
    const heading = document.getElementById('bottom_footer');
     heading.scrollIntoView({behavior:'smooth'})
    
})

