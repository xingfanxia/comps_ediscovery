

var store = {
  debug: true,
  state: {
    item: {Contents : "Please Select an Email"}
  },
  setMessageAction (newValue) {
    if (this.debug) console.log('setMessageAction triggered with', newValue)
    axios.get("/data/" + newValue)
    .then(response => {this.state.item.Contents = response.data['Message-Contents']})
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
      items: {}
    },
      mounted() {
        console.log('yolo')
        axios.get("/datakey")
        .then(response => {this.items = response.data})
      }
  })
}
