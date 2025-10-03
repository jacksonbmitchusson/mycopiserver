let temp = document.getElementById("temp");
let humid = document.getElementById("humid");
let image = document.getElementById("image");
let textbox = document.getElementById("textbox");

window.onload = function() {
    fetch('/api/env')
        .then(resp => resp.text())
        .then(text => {env.textContent = text})    
}

function get_image() {
    image.src = '/api/image/' + textbox.value;
}
