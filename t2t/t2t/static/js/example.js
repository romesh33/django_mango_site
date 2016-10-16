/**
 * This file provided by Facebook is for non-commercial testing and evaluation
 * purposes only. Facebook reserves all rights not expressly granted.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * FACEBOOK BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 * WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

var messages = messages_obj;
//console.log(messages);
var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
var path = ws_scheme + '://' + window.location.host + "/chat" + window.location.pathname;
console.log("Opened web socket with path: " + path);
var chatsock = new ReconnectingWebSocket(path);

chatsock.onmessage = function(message)
{
    console.log("Message received by web socket");
    //TODO: for some reason web socket doesn't receive messages when we send them by Send button
    var data = JSON.parse(message.data);
    if (data.message_text != null)
    {
        var sender = data.sender;
        console.log("sender=" + sender);
        var text = data.message_text;
        console.log("text=" + text);
        var time = data.time;
        console.log("time=" + time);
        var received_message = {"from": sender, "text": text, "time": time};
        console.log("received_message = " + received_message);
        messages.push(received_message);
        console.log("Messages length: " + messages.length);
    }
    else
    {
        // сюда мы должны попасть, если посылаем сообщение из функции consumers, которая посылает сообщение в ответ на
        // подключение вебсокета:
        console.log("message length is zero... it can be because user is connected, in this case no messsage data exists...");
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
      
var Message = React.createClass({
    render: function()
    {
        return (
            <div className="bordered">
                <p>{this.props.time}: {this.props.user}: {this.props.text}</p>
            </div>
        )
    }
});
      
var MessageTable = React.createClass({
    render: function() {
        var messages = [];
        this.props.messages.forEach(function(message, index) {
            messages.push(<Message text={message.text} time={message.time} user={message.from} key={index} />);
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
            messages: messages,
        };
    },
    handleMessageSend : function(text) {
        //alert("type of " + typeof message);
        //var old_messages = this.state.messages;
        //var new_messages = old_messages.push(message);
        //this.setState({messages: messages.push(message)});
        console.log("Message was sent to web socket with text: " + text);
        chatsock.send(JSON.stringify(text));
        //alert("Number of messages in state is: " + this.state.messages.length);
    },
    render: function() {
        return (
            <div>
                <h1>This is chat!</h1>
                <MessageTable messages={this.props.messages}/>
                {/* This is comment */}
                <SendMessageBar onButtonClick={this.handleMessageSend}/>
            </div>
        )
    }  
});
      
ReactDOM.render(<Chat messages={messages}/>, document.getElementById('new_chat'));