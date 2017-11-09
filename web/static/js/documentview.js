// httpGetAsync('/fakedata', parseData)

function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    var response = ""
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous
    xmlHttp.send(null);
}


// function parseData(response){
//   response = JSON.parse(response)
//   console.log(response)
//   var emailList = document.getElementById('emailList')
//   var node = document.createElement("UL");
//   for (var i in response.data.emails){
//     console.log(i)
//     var listElement = document.createElement("LI")
//     listElement.onclick = function(){alert(this.textContent)}
//     var textnode = document.createTextNode(response.data.emails[i]);
//     listElement.appendChild(textnode);
//     node.appendChild(listElement);
//   }
//   emailList.appendChild(node);
// }

//https://vuejs.org/v2/guide/state-management.html#Simple-State-Management-from-Scratch
var store = {
  debug: true,
  state: {
    item: {Contents : "Please Select an Email"}
  },
  setMessageAction (newValue) {
    if (this.debug) console.log('setMessageAction triggered with', newValue)
    this.state.item = newValue
  },
  clearMessageAction () {
    if (this.debug) console.log('clearMessageAction triggered')
    this.state.item = {Contents : "Please Select an Email"}
  },
  getMessageAction () {
    if (this.debug) console.log('getMessageAction triggered with', this.state.item.Contents)
    return this.state.item.Contents
  }
}


window.onload = function () {
  documentView = new Vue({
    el: "#document",
    delimiters: ["[[", "]]"],
    data: {
      message: store.state.item.Contents
    },
    methods: {
      updateView: function () {
        console.log(this);
        documentView.message = store.getMessageAction()
      }
    }
  })

  emailList = new Vue({
    el: '#emailListVue',
    delimiters: ["[[", "]]"],
    methods: {
        alert_user: function(item) {
        // `this` inside methods points to the Vue instance
        store.setMessageAction(item)
        documentView.updateView()
        // `event` is the native DOM event
        if (event) {
          //alert(event.target.tagName)
        }
      }
    },
    data: {
      items: [
        { Sender: 'John Doe', Receiver : 'Jill Doe', Subject : 'Pizza Tonight?', Sent_Date : '1/1/17', Contents : "Yo", id : 0 },
        { Sender: 'Bob Doe', Receiver : 'John Doe', Subject : 'Pasta Tonight?', Sent_Date : '2/1/17', Contents : "hell0", id : 1 },
        { Sender: 'Elliot Doe', Receiver : 'Randy Doe', Subject : '\'za Tonight?', Sent_Date : '3/1/17', Contents : "whats up", id : 2 },
        { Sender: 'John Doe', Receiver : 'Jill Doe', Subject : 'Yolo', Sent_Date : '4/1/17', Contents : "butts", id : 3 }
      ]
    }
  })
}
