// ----------------------------
// mitnk.com main.js
// updated: Sep 02, 2011
// whgking @ gmail.com
// ----------------------------

function enter_search_box() {
    var search_box = document.getElementById("cse-input");
    if (search_box == null) 
        return;
    if (search_box.value == "Search") {
        search_box.value = "";
    }
}

function leave_search_box() {
    var search_box = document.getElementById("cse-input");
    if (search_box == null)
        return;
    if (search_box.value == "") {
        search_box.value = "Search";
    }
}
