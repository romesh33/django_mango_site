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

//ReactDOM.render(
//  <p>Написано REact-ом</p>,
//  document.getElementById('content')
//);
//console.log("JS file loaded");
//var React = require('react');
//var ReactDOM = require('react-dom');
//window.ee = new EventEmitter();

var messages = [
    {from: 'admin', time: '12:13:14', text: 'Привет всем!', key: 0},
    {from: 'user', time: '12:14:15', text: 'Привет!', key: 1},
    {from: 'romko', time: '12:14:17', text: 'Пока!', key: 2}];

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
        var message = {from: "userX", time: "XX:XX", text: text};
        this.props.onButtonClick(message);
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
    handleMessageSend : function(message) {
        //alert("type of " + typeof message);
        //var old_messages = this.state.messages;
        //var new_messages = old_messages.push(message);
        this.setState({messages: messages.push(message)});
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