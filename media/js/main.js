function clear_cse_bkimg() {
    var input = document.getElementById('cse-input');
    input.setAttribute('class', 'cse-bgnoimg');
}

function set_cse_bkimg() {
    var input = document.getElementById('cse-input');
    if (input.value.length == 0) {
        input.setAttribute('class', 'cse-bgimg');
    }
}
