function get_ajax_obj() {
    if (window.XMLHttpRequest)
        var xmlhttp = new XMLHttpRequest();
    else // for IE6
        var xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    return xmlhttp;
}
function new_retweet(obj, id) {
    var xmlhttp = get_ajax_obj();
    if (obj.innerHTML == "NewRT") {
        obj.innerHTML = "Click to RT";
    }
    else if (obj.innerHTML == "Click to RT") {
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
                obj.innerHTML = xmlhttp.responseText;
        }
        xmlhttp.open("POST", ".", true);
        xmlhttp.send("action=newretweet&status_id=" + id);
        obj.innerHTML = '<img style="height:1em;" src="/media/images/ajax-loader-bar.gif">';
    }
}
function favo(obj, id) {
    var xmlhttp = get_ajax_obj();
    if (obj.innerHTML == "Favo") {
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
                obj.innerHTML = "Favo" + xmlhttp.responseText;
        }
        xmlhttp.open("POST", ".", true);
        xmlhttp.send("action=favo&status_id=" + id);
    }
    else {
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200)
                obj.innerHTML = xmlhttp.responseText;
        }
        xmlhttp.open("POST", ".", true);
        xmlhttp.send("action=unfavo&status_id=" + id);
    }
    obj.innerHTML = '<img style="height:1em;" src="/media/images/ajax-loader-bar.gif">';
}
function reply(name, id) {
    document.getElementById("in_reply_to_status_id").value = id;
    document.getElementById("tweet-text").value = "@" + name + " ";
    document.getElementById("tweet-text").focus();
}
function retweet(text) {
    document.getElementById("tweet-text").value = text;
    document.getElementById("tweet-text").focus();
}
function tweet() {
    var tweet_text = document.getElementById("tweet-text").value;
    if (tweet_text.length == 0) {
        return false;
    }

    var xmlhttp = get_ajax_obj();
    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            document.getElementById("new_tweets").innerHTML = xmlhttp.responseText + document.getElementById("new_tweets").innerHTML;
            document.getElementById("tweet-text").value = "";
            document.getElementById("char_count").innerHTML = "140";
        }
    }
    xmlhttp.open("POST", ".", true);
    var in_reply_to_status_id = document.getElementById("in_reply_to_status_id").value;
    xmlhttp.send("tweet_text=" + encodeURIComponent(tweet_text) + "&in_reply_to_status_id=" + in_reply_to_status_id);
    document.getElementById("char_count").innerHTML = '<img style="height:1em;" src="/media/images/ajax-loader-bar.gif">';
}
function check_char_count() {
    var tweet_text = document.getElementById("tweet-text").value;
    var tweet_length = tweet_text.length;
    if (tweet_length == 0 || tweet_text.indexOf("@") != 0) {
        document.getElementById("in_reply_to_status_id").value = "";
    }
    var len = 140 - tweet_length;
    if (len < 0)
        document.getElementById("char_count").innerHTML = '<font color="red">' + len + '</font>';
    else
        document.getElementById("char_count").innerHTML = len;
}
