<template>
  <div>
     <div class="row" id="homeSearchBar">
        <div class='col-lg-11'>
            <p class="control is-expanded">
              <!-- <input class="input" type="text" v-model="inputText" v-on:keyup="checkEnter"> -->
              <input type="text" class="input" id="searchBar" v-on:keyup.enter="checkEnter" v-model="inputText">
            </p>
        </div>
        <div class="col-lg-1">
          <p class="control">
            <a class="button is-info" id="searchButton" :href="formatSearchUrl(inputText)" target="_blank">Search</a>
          </p>
        </div>
    </div>
    <div id="the-buttons" class="row center">
      <datepicker id="dater" v-model='time1' lang="en" range format="yyyy-MM-dd" :shortcuts="shortcuts"></datepicker>
      <button id="tooltip" class="btn-sm queryButtons" v-on:click="getDate" data-text="Pass Date to Input">Put Date</button>
      <p class="separator">||</p>
      <button type="button" id="tooltip" class="btn-sm queryButtons" v-for="option in options" @click="addField(option.value)" value="option.value" :data-text="option.tooltip">
        {{ option.text }}
      </button>
    </div>
  </div>
</template>

<script>
import Datepicker from 'vue2-datepicker'

export default {
  components: {
    'datepicker': Datepicker
  },

  data () {
    return {
      inputText: '',
      selected: '',
      time1: '',
      msg: 'This is a button.',
      shortcuts: [
        {
          text: 'Today',
          start: new Date(),
          end: new Date()
        }
      ],
      options: [
        {text: 'From', value: '/From:\'\' ', tooltip: 'Filter by sender name or email'},
        {text: 'To', value: '/To:\'\' ', tooltip: 'Filter by recipient name or email'},
        {text: 'Subject', value: '/Subject:\'\' ', tooltip: 'Filter by keyword(s) in subject'},
        {text: 'Message Contents', value: '/Message_Contents:\'\' ', tooltip: 'Filter by keyword(s) in message contents'},
        {text: 'ID', value: '/ID:\'\' ', tooltip: 'Filter by ID'}
      ]
    }
  },

  methods: {
    formatSearchUrl: function (inputText) {
      if (inputText.length === 0) {
        return '/result?Message_Contents=' + inputText
      } else {
        var dict = {}
        var reFields = /(\/.*?:)/g
        var reValues = /'(.*?)'/g
        var filters = inputText.match(reFields)
        var values = inputText.match(reValues)
        for (var i = 0; i < filters.length; i++) {
          var filterTrimmed = filters[i].substr(1).slice(0, -1)
          var valueTrimmed = values[i].substr(1).slice(0, -1)
          dict[filterTrimmed] = valueTrimmed
        }
        console.log(dict)
        return '/result?' + $.param(dict)
      }
    },

    addField: function (newVal) {
      if (document.getElementById('searchBar').value !== 0 && document.getElementById('searchBar').value.indexOf(newVal) !== -1) {
        alert('This field has already added')
      } else {
        document.getElementById('searchBar').value += newVal
      }
    },

    checkEnter: function () {
      console.log('this works')
      $('#searchBar').keyup(function (event) {
        if (event.keyCode === 13) {
          $('#searchButton').click()
        }
      })
    },

    getDate: function () {
      var date1 = this.time1[0]
      var date2 = this.time1[1]
      console.log(date1)
      if (date1 !== undefined && date2 !== undefined) {
        document.getElementById('searchBar').value += 'Date:/\'' + this.time1[0] + '-' + this.time1[1] + '\' '
      }
    }
  }
}

</script>

<style scoped>

.dateStyle {
    width: 200px;
}

#homeSearchBar {
    margin: auto;
}

#dater {
    margin-top: 10px;
}

.queryButtons {
    border-color: #0B5091;
    display: inline;
    margin-left: 10px;
    margin-right: 10px;
    margin-top: 10px;
    transition-duration: 0.5s;
}
.queryButtons:hover {
    background-color: #0B5091;
    color: white;
}

#searchButton {
    color: #fff;
    background-color: #0B5091;
    border-color: #0B5091;
    border-radius: 4px;
}

#the-buttons {
    display: flex;
    justify-content: center;
}

#searchBar {
    border-color: #0B5091;
}

.separator {
    font-size:20px;
    margin-top: 10px;
    margin-bottom: 0px;
}

#tooltip:hover:before{
    border: solid;
    border-color: #333 transparent;
    border-width: 6px 6px 0 6px;
    bottom: 20px;
    content: "";
    left: 50%;
    position: absolute;
    z-index: 99;
}

#tooltip:hover:after{
    background: #333;
    background: rgba(0,0,0,.8);
    border-radius: 5px;
    bottom: 26px;
    color: #fff;
    content: attr(data-text);
    left: 20%;
    padding: 5px 15px;
    position: absolute;
    z-index: 98;
    width: 220px;
    white-space: pre;
}

#tooltip{
    display: inline;
    position: relative;
}
</style>
