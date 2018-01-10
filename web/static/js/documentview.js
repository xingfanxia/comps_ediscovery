// TODO: QUERY TOPICS AT THE BEGINNING AND STORE THEM AS
// OPPOSED TO QURYING THEM EVERY TIME
// var topicStore = {
//   debug: true
//   state: {
//     data : {}
//   },
//   setTopicAction(){
//
//   }
// }

//Vue Stuff

//Data store for document and metadata views
var email_store = {
  debug: true,
  state: {
    data: {'Message-Contents' : "Please Select an Email"}
  },
  setMessageAction (newValue) {
    if (this.debug) console.log('setMessageAction triggered with', newValue)
    shortID = newValue
    console.log('short:',shortID)
    axios.get("/data/" + shortID)
    .then(response => {
      this.state.data = response.data[0]
      metadataView.updateView()
      documentView.updateView()
    })
  },
  clearMessageAction () {
    if (this.debug) console.log('clearMessageAction triggered')
    this.state.item = {'Message-Contents' : "Please Select an Email"}
  },
  getMessageAction () {
    if (this.debug) console.log('getMessageAction triggered with', this.state.data['Message-Contents'])
    return this.state.data['Message-Contents']
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
      console.log("data:",data)
      data.forEach(datum => console.log(datum['Date']))
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
    },
    alert_user: function(item) {
      // `this` inside methods points to the Vue instance
      email_store.setMessageAction(item)
      // `event` is the native DOM event
      if (event) {
        //alert(event.target.tagName)
      }
    }
  }
})

//'main' method essentially, actually creates the views
window.onload = function () {
  documentView = new Vue({
    el: "#document",
    delimiters: ["[[", "]]"],
    data: {
      message: email_store.state.data['Message-Contents']
    },
    methods: {
      updateView: function () {
        console.log(this);
        span_message = email_store.getMessageAction()
        axios.get("/topics")
        .then(response => {
          for (var key in response.data) {
            // check if the property/key is defined in the object itself, not in parent
            if (response.data.hasOwnProperty(key)) {
                word_list = response.data[key]
                for (i in word_list){
                    var word = word_list[i]
                    var word_regex = new RegExp('\\b' + word + '\\b', 'gi')
                    var word_span = "<span class=topic_" + key + ">" + word +"</span>"
                    span_message = span_message.replace(word_regex, word_span)
                }
            }
          }
          documentView.message = span_message
        })
      }
    }
  })

  emailButtons = new Vue({
    el: '#email_buttons',
    delimiters: ['[[',']]'],
    methods: {
      feedback: function(relevant){
        axios.post('/feedback', {
          'ID': email_store.state.data.ID,
          'Relevant': relevant
        })
        .then(function (response) {
        })
        .catch(function (error) {
          console.log(error);
        });
      }
    }
  })

  emailList = new Vue({
    el: '#emailList',
    delimiters: ['[[',']]'],
    data: {
      searchQuery: '',
      gridColumns: ['From', 'To', 'Subject', 'Date'],
      items: []
    },
    mounted() {
      axios.get("/datakey")
      .then(response => {
        Object.keys(response.data).forEach(key => this.items.push(response.data[key]))
        console.log('items',this.items)
      })
    }
  })

  metadataView = new Vue({
    el: '#metadata',
    delimiters: ['[[',']]'],
    data: {
      metadata_to : '',
      metadata_from : '',
      metadata_date : '',
      metadata_subject : ''
    },
    methods: {
      updateView: function() {
        this.metadata_to = email_store.state.data['X-To']
        this.metadata_from = email_store.state.data['X-From']
        this.metadata_date = email_store.state.data['Date']
        this.metadata_subject = email_store.state.data['Subject']
      }
      }
    })
  }
