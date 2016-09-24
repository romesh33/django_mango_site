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
window.ee = new EventEmitter();

var messages = [
{from: 'admin', time: '12:13:14', text: 'Привет всем!'},
{from: 'user', time: '12:14:15', text: 'Привет!'},
{from: 'romko', time: '12:14:17', text: 'Пока!'}];

var Messages = React.createClass({
    render: function() {
        var data = this.props.data;
        var newsTemplate = data.map(function(message, index) {
            return (
                <p key={index}>{message.time}: {message.from}: {message.text}</p>
            )
        })
        console.log(newsTemplate);
        console.log(data);
        return (
            <div>
                {newsTemplate}
            </div>
        )
    }
});

var TestInput = React.createClass({
    getInitialState: function() {
        return {
            myValue: ''
        };
    },
    onChangeHandler: function(e) {
        this.setState({myValue: e.target.value})
    },
    onBtnClickHandler: function(e) {
        e.preventDefault();
//        var author = ReactDOM.findDOMNode(this.refs.author).value;
//        var text = ReactDOM.findDOMNode(this.refs.text).value;
//        var item = [{
//            author: author,
//            text: text,
//            bigText: '...'
//        }];
        window.ee.emit('News.add', item);
    }
    render: function() {
        return (
            <div>
                <input
                    value={this.state.myValue}
                    onChange={this.onChangeHandler}
                    placeholder='введите значение'
                />
                <button onClick={this.onBtnClickHandler}>Отправить сообщение</button>
            </div>
        );
    }
});

var ChatApp = React.createClass({
    getInitialState: function() {
        return {
            messages: {messages}
        }
    },
    render: function() {
        return (
            <div className="app">
                Всем привет, я компонент ChatApp!. Я умею показывать сообщения в чате.
                <Messages data={this.state.messages} /> {/*добавили свойство data */}
                <TestInput />
            </div>
        );
    }
});

ReactDOM.render(<ChatApp />, document.getElementById('new_chat'));