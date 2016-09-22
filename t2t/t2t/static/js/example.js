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

var ChatApp = React.createClass({
    render: function() {
        return (
            <div className="app">
                Всем привет, я компонент ChatApp!. Я умею показывать сообщения в чате.
                <Messages data={messages} /> {/*добавили свойство data */}
                <button type="submit" className="btn btn-default">Отправить</button>
            </div>
        );
    }
});

ReactDOM.render(<ChatApp />, document.getElementById('new_chat'));