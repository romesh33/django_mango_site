window.ee = new EventEmitter();
// читаем в локальную переменную messages объекты, полученные из джанго в виде json и преобразованные в js объекты
// в глобальном js скрипте (в теле event.html):
// messages is a list of messages without ID:
var messages = messages_obj;
// messages_dict is a dictionary with keys = message ids and values = dictionaries {from, text, time}:
var messages_dict = messages_dict_obj;
var users = users_obj;
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var path = ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname;
console.log("Opened web socket with path: " + path);
console.log("Users: " + users);
// создаем сокет:
var chatsock = new ReconnectingWebSocket(path);

// регистрируем функцию по обработке события "получение сообщения" в веб-сокете:
chatsock.onmessage = function(message)
{
    console.log("Message received by web socket");
    // так как данные в объекте message сериализованы в json, парсим его для получения объекта js:
    var data = JSON.parse(message.data);
    if (data.message_text != null)
    {
        var message_id = data.id;
        //console.log("new_nessage_id = " + message_id);
        var sender = data.sender;
        //console.log("sender=" + sender);
        var text = data.message_text;
        //console.log("text of receivd message=" + text);
        var time = data.time;
        //console.log("time=" + time);
        var received_message = {"id": message_id, "from": sender, "text": text, "time": time};
        //console.log("received_message = " + received_message);
        //messages.push(received_message);
        window.ee.emit('Message.add', received_message);
        //console.log("Messages length: " + messages.length);
    }
    else
    {
        console.log("Were are here!");
        if (data.user_connected != null)
        {
            var username = data.user_connected;
            console.log("User " + username + " is connected");
            window.ee.emit('User.add', username);
        }
        else if (data.user_disconnected != null)
        {
            var username = data.user_disconnected;
            console.log("User " + username + " is disconnected");
            window.ee.emit('User.remove', username);
        }
        // сюда мы должны попасть, если посылаем сообщение из функции consumers, которая посылает сообщение в ответ на
        // подключение вебсокета:
        //console.log("message length is zero... it can be because user is connected, in this case no messsage data exists...");
        //TODO: need to add handler when message is deleted 
    }
};

var SendMessageBar = React.createClass({
    handleButtonClick: function()
    {
        var text = this.refs.messageTextInput.value;
        if (text.length > 0)
        {
            //alert(text);
        }
        else
        {
            //alert("Message text is empty");
        }
        this.props.onButtonClick(text);
    },
    render: function()
    {
        return (
            <div className="bordered">
                <input placeholder='введите сообщение' ref='messageTextInput'/>
            <button onClick={this.handleButtonClick}>Отправить</button>
            </div>
        )
    }
});

var DeleteMessageButton = React.createClass({
    handleDeleteButtonClick: function() {
        var text = this.props.text;
        var time = this.props.time;
        var user = this.props.user;
        this.props.onButtonClick(time, user, text);
    },
    render: function()
    {
        return (
            <button onClick={this.handleDeleteButtonClick}>x</button>
        )
    }
});

var Message = React.createClass({
    render: function()
    {
        return (
            <div className="bordered">
                <span>{this.props.time}: {this.props.user}: {this.props.text}</span>
                <DeleteMessageButton onButtonClick={this.props.onMessageDelete} text={this.props.text}
                user={this.props.user} time={this.props.time}/>
            </div>
        )
    }
});
      
var MessageTable = React.createClass({
    render: function() {
        var messages = [];
        var messDelFunction = this.props.onMessageDelete;
        console.log("messDelFunction = " + messDelFunction);
        this.props.messages.forEach(function(message, index) {
            messages.push(<Message text={message.text} time={message.time} user={message.from}
            key={index} onMessageDelete={messDelFunction}/>);
        });
        return (
            <div>
                {messages}
            </div>
        )
    }
});
        
var Chat = React.createClass({
    getInitialState: function() {
        return {
            //messages: messages,
            messages: messages_dict
        };
    },
    componentDidMount: function() {
        var self = this;
        window.ee.addListener('Message.add', function(received_message) {
            //messages.push(received_message);
            var id = received_message['id'];
            var from = received_message['from'];
            var text = received_message['text'];
            var time = received_message['time'];
            messages[id] = {from: from, text: text, time: time};
            self.setState({messages: messages});
        });
    },
    componentWillUnmount: function() {
        window.ee.removeListener('Message.add');
    },
    handleMessageSend : function(text) {
        console.log("Message was sent to web socket with text: " + text);
        chatsock.send(JSON.stringify(text));
    },
    handleMessageDelete : function(time, user, text) {
        console.log("Chat: Message with time: " + time + ", user: " + user + ", text: " + text + " will be deleted");
        //TODO: need to delete specific message from messages;
        var message_to_delete = {"from": user, "text": text, "time": time};
        var indexInArray = messages.indexOf(message_to_delete);
        console.log("Index of mess to del = " + indexInArray);
        if (indexInArray == -1)
        {
            console.log("As I didn't find element, I'll delete latest in the list :)");
            messages.pop();
            //что-то мне кажется, что не совсем правильно сет стейт в самом компоненте делать:
            var self = this;
            self.setState({messages: messages});
        }
        // And also send message about message deletion to the web socket - for all clients to understand that it was deleted
        //messages.delete()
        //chatsock.send(JSON.stringify(text));
        //this.setState({messages: messages});
    },
    render: function() {
        return (
            <div>
                <div className="chat_app" id="chat">
                    <h1>This is chat!</h1>
                    <MessageTable messages={this.props.messages} onMessageDelete={this.handleMessageDelete}/>
                    {/* This is comment */}
                </div>
                <SendMessageBar onButtonClick={this.handleMessageSend}/>
            </div>
        )
    }
});

var SingleUser = React.createClass({
    render: function() {
        return (
            <span>{this.props.name} and </span>
        )
    }
});

var UsersList = React.createClass({
    getInitialState: function() {
        return {
            users: users,
        };
    },
    componentDidMount: function() {
        var self = this;
        window.ee.addListener('User.add', function(username) {
            users.push(username);
            self.setState({users: users});
        });
        window.ee.addListener('User.remove', function(username) {
            var index = users.indexOf(username);
            if (index != 0)
            {
                users.splice(index, 1);
            }
            console.log("Listener noticed that user " + username + " was disconnected");
            //users.push(username);
            self.setState({users: users});
        });
    },
    componentWillUnmount: function() {
        window.ee.removeListener('User.add');
        window.ee.removeListener('User.remove');
    },
    render: function() {
        var users = [];
        this.props.users.forEach(function(user, index) {
            users.push(<SingleUser name={user} key={index} />);
        });
        return (
            <div>
                {users}
            </div>
        )
    }
});

ReactDOM.render(<Chat messages={messages}/>, document.getElementById('new_chat'));
ReactDOM.render(<UsersList users={users}/>, document.getElementById('user_list'));

// this function does autoscrolling to the bottom of the chat. I'm not sure how it works - just copied example from SO :)
// http://stackoverflow.com/questions/25505778/automatically-scroll-down-chat-div
// TODO: to understand how it works
setInterval(function () {
    $("#chat").animate({
        scrollTop: $("#chat")[0].scrollHeight}, -500);
}, 1000);