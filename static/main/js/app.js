let navbar_nav = document.getElementsByClassName('navbar-nav');
let nav_search = document.getElementsByClassName('nav-search');
let bar_button = document.getElementsByClassName('fa-bars');
let close_button = document.getElementsByClassName('fa-close');
let search_button = document.getElementsByClassName('fa-search');
let nav_search_close = document.getElementsByClassName('nav-search-close');
let sort_button = document.getElementsByClassName('sort-button');
let filter_wrapper = document.getElementsByClassName('filter-wrapper');
let filter_close_button = document.getElementsByClassName('filter-close-button');
let availability_wrapper = document.getElementsByClassName('availability-wrapper');
let availability_button = document.getElementsByClassName('availability-button');
let availability_close_button = document.getElementsByClassName('availability-close-button');
let price_wrapper = document.getElementsByClassName('price-wrapper');
let price_button = document.getElementsByClassName('price-button');
let price_close_button = document.getElementsByClassName('price-close-button');
let product_wrapper = document.getElementsByClassName('product-wrapper');
let counter_num = document.getElementsByClassName('counter-num');
let counter_sub = document.getElementsByClassName('counter-sub');
let counter_sum = document.getElementsByClassName('counter-sum');

function navigateToProduct (){
    let url = window.location.href.split('/');
    let currentPage = url[url.length-1];
    if(currentPage == 'index.html'){
        window.location.href = 'pages/product.html';
    }else{
        window.location.href = 'product.html';
    }
}

function sumar (pos) {
    let currentValue = parseInt(counter_num[pos].innerHTML);
    counter_num[pos].innerHTML = (currentValue + 1);
};

function restar (pos) {
    let currentValue = parseInt(counter_num[pos].innerHTML);
    if(currentValue > 1){
        counter_num[pos].innerHTML = (currentValue - 1);
    }
};

if (window.screen.width > 576) {
    navbar_nav[0].className += ' nav-open';
};

bar_button[0].addEventListener('click', () => {
    navbar_nav[0].className += ' nav-open';
    bar_button[0].className += ' d-none';
    close_button[0].classList.remove('d-none');
});

close_button[0].addEventListener('click', ()=> {
    close_button[0].className += ' d-none';
    bar_button[0].classList.remove('d-none');
    navbar_nav[0].classList.remove('nav-open');
});

search_button[0].addEventListener('click', ()=>{
    nav_search[0].classList.remove('search-close');
});

nav_search_close[0].addEventListener('click', ()=>{
    nav_search[0].className += ' search-close';
});

sort_button[0].addEventListener('click', ()=>{
    filter_wrapper[0].classList.remove('filter-close');
});

filter_close_button[0].addEventListener('click', ()=>{
    filter_wrapper[0].className += ' filter-close';
});

availability_button[0].addEventListener('click', ()=>{
    availability_wrapper[0].classList.remove('availability-close');
});

availability_close_button[0].addEventListener('click', ()=>{
    availability_wrapper[0].className += ' availability-close';
});

availability_close_button[1].addEventListener('click', ()=>{
    availability_wrapper[0].className += ' availability-close';
});

price_button[0].addEventListener('click', ()=>{
    price_wrapper[0].classList.remove('price-close');
});

price_close_button[0].addEventListener('click', ()=>{
    price_wrapper[0].className += ' price-close';
});

price_close_button[1].addEventListener('click', ()=>{
    price_wrapper[0].className += ' price-close';
});



