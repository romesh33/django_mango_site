$(function() {
    // When we're using HTTPS, use WSS too.
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var path = ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname;
    var chatsock = new ReconnectingWebSocket(path);

    chatsock.onmessage = function(message)
    {
        var data = JSON.parse(message.data);
        var chat = $("#chat");
        if (data.message_text != null)
        {
            // сюда мы попадаем, когда посылаем сообщение из consumers:
            if ($("#empty_chat_message").length) $("#empty_chat_message").hide();
            chat.append($("<p></p>").text(data.creation_time + ": " + data.sender + ": " + data.message_text));
        }
        else
        {
            // сюда мы должны попасть, если посылаем сообщение из функции consumers, которая посылает сообщение в ответ на
            // подключение вебсокета:
            var users_connected = $("#connected_users").text();
            users_connected = users_connected + "," + data.user_connected;
            $("#connected_users").text(users_connected);
        }
//        else if (data.user_connected != null)
//        {
//            var l = 1;
//            $("#connected_users").append($("<span></span>").text(data.user_connected);
//        }
//        if (data.user_connected)
//        {
//            //alert("1");
//            $("#connected_users").append($("<span></span>").text(data.user_connected);
//        }
//        else
//        {
//            //alert("2");
//            var chat = $("#chat");
//            $("#empty_chat_message").hide();
//            chat.append($("<p></p>").text(data.creation_time + ": " + data.sender + ": " + data.message_text));
//        }
    };

    $("#chatform").on("submit", function(event)
    {
        var message = {
            message: $('#id_text').val(),
        }
        chatsock.send(JSON.stringify(message));
        return false;
    });
});