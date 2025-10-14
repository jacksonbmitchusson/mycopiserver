let temp = document.getElementById("temp");
let humid = document.getElementById("humid");
let image0 = document.getElementById("image0");
let image1 = document.getElementById("image1");
let textbox = document.getElementById("textbox");
let button = document.getElementById("button");

window.onload = function() {
    fetch('/api/env')
        .then(resp => resp.text())
        .then(text => {env.textContent = text})    
}

function get_image() {
    textbox.hidden = true;
    button.hidden = true;
    image0.src = '/api/image/' + textbox.value + '/0';
    image0.hidden = false;
    image1.src = '/api/image/' + textbox.value + '/1';
    image1.hidden = false;
}
