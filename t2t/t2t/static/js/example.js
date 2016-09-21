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

var NewSuperComponent = React.createClass({
    render: function() {
        return <div>I'm the new div returned by react!</div>;
    }
});

ReactDOM.render(<NewSuperComponent name="Roman"/>,
  document.getElementById('chat_new_messages'));