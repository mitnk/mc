var new_results_count = 0;
var tweet_flag = 'li id="tweet-item-';
var LIMIT_AUTO_UPDATE = 200;
var pid_auto_update = 0;

// "" if root path else not ends up with a '/', should be "/path_like_this"
var TWITCN_ROOT_PATH = "/t";

String.prototype.count = function(char){
    return this.split(char).length-1;
}

function confirm_msg(msg)
{
    if(confirm(msg))
    {
        return true;
    }
    return false;
}

function setTweetText(text) {
    $("#status_update_box").show();
    $("#status-textarea").val(text).focus();
    checkCharCount();
}

function retweet(status_id) {
    if (confirm_msg('Retweet to your followers?'))
        $.post(TWITCN_ROOT_PATH + "/retweet/", 
                {"status_id":status_id}, 
                after_re_tweet);
}

function after_re_tweet(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            alert('Retweet Succeed!');
        }
    }
}

function after_destroy_tweet(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            id = data.substr(data.indexOf('|')+1);
            $("li#tweet-item-" + id).remove();
        }
    }
}

function destroy_dm(status_id) {
    if (confirm_msg('delete this message?'))
        $.post(TWITCN_ROOT_PATH + "/destroy_dm/", 
                {"status_id":status_id}, 
                after_destroy_tweet);
}

function destroy_tweet(status_id) {
    if (confirm_msg('delete this tweet?'))
        $.post(TWITCN_ROOT_PATH + "/destroy_tweet/", 
                {"status_id":status_id}, 
                after_destroy_tweet);
}

function after_create_favorite(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            id = data.substr(data.indexOf('|')+1);
            $("#favo-action-" + id).addClass("this-is-favo");
        }
    }
}

function create_favorite(status_id) {
    $.post(TWITCN_ROOT_PATH + "/create_favorite/", 
            {"status_id":status_id}, 
            after_create_favorite);
}

function after_destroy_favorite(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            id = data.substr(data.indexOf('|')+1);
            $("#favo-action-" + id).removeClass("this-is-favo");
        }
    }
}

function destroy_favorite(status_id) {
    $.post(TWITCN_ROOT_PATH + "/destroy_favorite/", 
            {"status_id":status_id}, 
            after_destroy_favorite);
}

function after_unblock_user(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            user_name = data.substr(data.indexOf('|')+1);
            $("#block-user-" + user_name).html("block");
        }
    }
}

function unblock_user(user_name) {
    $.post(TWITCN_ROOT_PATH + "/unblock/", 
            {"user_name":user_name}, 
            after_unblock_user);
}

function after_block_user(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            user_name = data.substr(data.indexOf('|')+1);
            $("#block-user-" + user_name).html("unblock");
            $("#spam-user-" + user_name).html("");
        }
    }
}

function block_user(user_name) {
    $.post(TWITCN_ROOT_PATH + "/block/", 
            {"user_name":user_name}, 
            after_block_user);
}

function after_report_spam(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            user_name = data.substr(data.indexOf('|')+1);
            $("#spam-user-" + user_name).html("report Done!");
            $("#block-user-" + user_name).html("unblock");
        }
    }
}

function report_spam(user_id) {
    $.post(TWITCN_ROOT_PATH + "/report_spam/", 
            {"user_id":user_id}, 
            after_report_spam);
}

function after_follow_user(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            user_name = data.substr(data.indexOf('|')+1);
            $("#follow-user-" + user_name).html("unfollow");
            $("#follow-state-" + user_name).html('<span class="is-following"><i></i><strong>Following</strong></span>');
        }
    }
}

function follow_user(user_name) {
    $.post(TWITCN_ROOT_PATH + "/follow/", 
            {"user_name":user_name}, 
            after_follow_user);
}

function after_unfollow_user(data, textStatus) {
    if (textStatus == "success") {
        if (data.indexOf('ok|') != -1) {
            user_name = data.substr(data.indexOf('|')+1);
            var txt = '<button onclick="javascript:follow_user(\'' + user_name + '\');return false;" title="" class="btn"><i></i>Follow</button>';
            $("#follow-state-" + user_name).html(txt);
            $("#follow-user-" + user_name).html("follow");
        }
    }
}

function unfollow_user(user_name) {
    $.post(TWITCN_ROOT_PATH + "/unfollow/", 
            {"user_name":user_name}, 
            after_unfollow_user);
}

function after_tweet(data, status){
    if (status == "success") {
        if (data.indexOf("TWITCNERROR: ") == -1) {
            $('#timeline').prepend(data);
        }
        $("#status-textarea").val("");
        $("#status-field-char-counter").html("140");
        $("#status-field-char-counter").removeClass("loading").addClass("char-counter").css("color","#CCCCCC");
    }
}

function afterAutoUpdate(data, textStatus) {
    if (textStatus == 'success') {
        // check data.length, make sure data contains tweets
        if (data.length > 30) {
            new_results_count += data.count(tweet_flag);
            if (new_results_count > LIMIT_AUTO_UPDATE) {
                clearInterval(pid_auto_update);
            }
            $("#results_update").html(new_results_count + ' new tweets.');
            $('#timeline').prepend(data);
            $("#new_results_notification").show();
            document.title = '(' + new_results_count + ') Twitcn';
            make_hover_action();
        }
    }
}

function showNewRetweets() {
    if (new_results_count > LIMIT_AUTO_UPDATE) {
        pid_auto_update = setInterval(autoUpdate, 300000);
    }
    new_results_count = 0;
    $('.buffered').removeClass('buffered');
    $("#new_results_notification").hide();
    document.title = 'Twitcn';
}

function tweet()
{
    try {
        if ($("#status-textarea").val().length <= 0)
            return false;
        else {
            $.post(TWITCN_ROOT_PATH + "/tweet/", 
                   {"tweet-text":$("#status-textarea").val()}, 
                   after_tweet);

            $("#status-field-char-counter").removeClass("char-counter").addClass("loading").css("color","transparent");
            $("#update-submit").addClass("disabled");
        }
    }
    catch(e) {}
    return false;
}

function checkCharCount(){
    var len = 140 - $("#status-textarea").val().length;
    
    if (len == 140) {
        $("#update-submit").addClass("disabled");
    }
    else {
        $("#update-submit").removeClass("disabled");
    }
    
    if (len < 0)
        $("#status-field-char-counter").html('<font color="red">' + len + '</font>');
    else
        $("#status-field-char-counter").html(len);
}

function make_hover_action() {
    $(".hentry").hover(
        function () {
           $(this).find(".actions-hover").show();
           $(this).find(".fav-action").css("display", "block");
        }, 
        function () {
            $(this).find(".actions-hover").hide();
            $(this).find(".fav-action").hide();
        }
    );
} 

function afterLoadMore(data, textStatus) {
    if (textStatus == "success") {
        if (new_results_count > LIMIT_AUTO_UPDATE) {
            pid_auto_update = setInterval(autoUpdate, 300000);
            new_results_count = 0;
        }

        $('#timeline').find("li#first-time-helper").remove();
        $("#pagination").remove();
        $('#timeline').append(data);
        make_hover_action();
    }
}

function resetCursor(cursor_name) {
    $("#side_base").find("li.active").removeClass("active");
    $("#" + cursor_name).addClass("active");
}

function loadMoreStatus(data) {
    if (data['first_time']) {
        resetCursor(data['cursor_name']);
        var loadingHTML = '<li id="first-time-helper"><div style="width:100px; height:100px; margin:0 auto; padding-top:1em;"><a href="#"><img src="/twitcn_media/images/loading.gif" width=100 height=100></a></div></li>';
        $('#timeline').html(loadingHTML); 
        $("#heading").html(data['page_name']);
    }
    else {
        $("#more").addClass("loading").html("");
    }

    $.post(TWITCN_ROOT_PATH + "/more/", 
            data, 
            afterLoadMore);
}

function afterLoadUsers(data, textStatus) {
    if (textStatus == "success") {
        $('#timeline').find("li#first-time-helper").remove();
        $("#pagination").remove();
        $('#users_table').append(data);
    }
}

function loadUsers(data) {
    if (data['first_time']) {
        resetCursor(data['cursor_name']);
        var loadingHTML = '<li><div id="follow_grid"><table id="users_table"></table></div></li><li id="first-time-helper"><div style="width:100px; height:100px; margin:0 auto; padding-top:1em;"><a href="/"><img src="/twitcn_media/images/loading.gif" width=100 height=100></a></div></li>';
        $('#timeline').html(loadingHTML);
        $("#heading").html(data['page_name']);
    }
    else {
        $("#more").addClass("loading").html("");
    }

    $.post(TWITCN_ROOT_PATH + "/more/", 
            data, 
            afterLoadUsers);
}

function afterLoadTrends(data, textStatus) {
    if (textStatus == "success") {
        $('#ul-trends-list').html(data);
    }
}

function loadTrends(data) {
    $.post(TWITCN_ROOT_PATH + "/get_trends/", 
            data, 
            afterLoadTrends);

    $('#ul-trends-list').html('<li><a>Loading...</a></li>');
    return false;
}
