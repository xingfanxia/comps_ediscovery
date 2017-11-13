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

// register the grid component
Vue.component('demo-grid', {
  template: '#grid-template',
  delimiters: ['[[',']]'],
  props: {
    data: Array,
    columns: Array,
    filterKey: String
  },
  data: function () {
    var sortOrders = {}
    this.columns.forEach(function (key) {
      sortOrders[key] = 1
    })
    return {
      sortKey: '',
      sortOrders: sortOrders
    }
  },
  computed: {
    filteredData: function () {
      var sortKey = this.sortKey
      var filterKey = this.filterKey && this.filterKey.toLowerCase()
      var order = this.sortOrders[sortKey] || 1
      var data = this.data
      if (filterKey) {
        data = data.filter(function (row) {
          return Object.keys(row).some(function (key) {
            return String(row[key]).toLowerCase().indexOf(filterKey) > -1
          })
        })
      }
      if (sortKey) {
        data = data.slice().sort(function (a, b) {
          a = a[sortKey]
          b = b[sortKey]
          return (a === b ? 0 : a > b ? 1 : -1) * order
        })
      }
      return data
    }
  },
  filters: {
    capitalize: function (str) {
      return str.charAt(0).toUpperCase() + str.slice(1)
    }
  },
  methods: {
    sortBy: function (key) {
      this.sortKey = key
      this.sortOrders[key] = this.sortOrders[key] * -1
    }
  }
})

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

  var emailList = new Vue({
    el: '#emailList',
    delimiters: ['[[',']]'],
    data: {
      searchQuery: '',
      gridColumns: ['Sender', 'Receiver', 'Subject', 'Sent_Date'],
      gridData: [
          { Sender: 'John Doe', Receiver : 'Jill Doe', Subject : 'Pizza Tonight?', Sent_Date : '1/1/17', Contents : "Yo", id : 0 },
          { Sender: 'Bob Doe', Receiver : 'John Doe', Subject : 'Pasta Tonight?', Sent_Date : '2/1/17', Contents : "hell0", id : 1 },
          { Sender: 'Elliot Doe', Receiver : 'Randy Doe', Subject : '\'za Tonight?', Sent_Date : '3/1/17', Contents : "whats up", id : 2 },
          { Sender: 'John Doe', Receiver : 'Jill Doe', Subject : 'Yolo', Sent_Date : '4/1/17', Contents : "butts", id : 3 }
        ]
    }
  })

  // emailList = new Vue({
  //   el: '#emailList',
  //   delimiters: ["[[", "]]"],
  //   data: function(){
  //     var sortOrders = {}
  //     var keys = ['Sender', 'Receiver', 'Subject', 'Sent_Date']
  //     keys.forEach(function (key) {
  //       sortOrders[key] = 1
  //     })
  //     var toReturn = {
  //       items: [
  //         { Sender: 'John Doe', Receiver : 'Jill Doe', Subject : 'Pizza Tonight?', Sent_Date : '1/1/17', Contents : "Yo", id : 0 },
  //         { Sender: 'Bob Doe', Receiver : 'John Doe', Subject : 'Pasta Tonight?', Sent_Date : '2/1/17', Contents : "hell0", id : 1 },
  //         { Sender: 'Elliot Doe', Receiver : 'Randy Doe', Subject : '\'za Tonight?', Sent_Date : '3/1/17', Contents : "whats up", id : 2 },
  //         { Sender: 'John Doe', Receiver : 'Jill Doe', Subject : 'Yolo', Sent_Date : '4/1/17', Contents : "butts", id : 3 }
  //       ],
  //       keys: keys,
  //       sortKey: '',
  //       sortOrders: sortOrders,
  //       searchQuery: ''
  //     }
  //     return toReturn 
  //   },
  //   methods: {
  //       alert_user: function(item) {
  //         // `this` inside methods points to the Vue instance
  //         store.setMessageAction(item)
  //         documentView.updateView()
  //         // `event` is the native DOM event
  //         if (event) {
  //           //alert(event.target.tagName)
  //         }
  //       },
  //       sortBy: function (key) {
  //         console.log('sorting by', key);
  //         this.sortKey = key
  //         this.sortOrders[key] = this.sortOrders[key] * -1
  //       }
  //   },
  //   computed: {
  //     filteredData: function () {
  //       var sortKey = this.sortKey
  //       var filterKey = this.filterKey && this.filterKey.toLowerCase()
  //       var order = this.sortOrders[sortKey] || 1
  //       var data = this.items
  //       if (filterKey) {
  //         console.log('filterKey')
  //         data = data.filter(function (row) {
  //           return Object.keys(row).some(function (key) {
  //             return String(row[key]).toLowerCase().indexOf(filterKey) > -1
  //           })
  //         })
  //       }
  //       if (sortKey) {
  //         console.log('sortKey')
  //         data = data.slice().sort(function (a, b) {
  //           a = a[sortKey]
  //           b = b[sortKey]
  //           return (a === b ? 0 : a > b ? 1 : -1) * order
  //         })
  //       }
  //       return data
  //     }
  //   },
  //   filters: {
  //     capitalize: function (str) {
  //       return str.charAt(0).toUpperCase() + str.slice(1)
  //     }
  //   }
  // })
}
