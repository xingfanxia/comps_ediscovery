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
      <button class="btn-sm queryButtons" v-on:click="getDate">Put Date</button>
      <p class="separator">||</p>
      <button type="button" class="btn-sm queryButtons" v-for="option in options" @click="addField(option.value)" value="option.value">
        {{ option.text }}
      </button>
    </div>
    <div class="tooltip">
        Hover over me
      <span class="tooltiptext">Tooltip text</span>
    </div>
  </div>
</template>

<script>
import Datepicker from 'vue2-datepicker'
import VTooltip from 'v-tooltip'

export default {
  components: {
    'datepicker': Datepicker,
    'v-tooltip': VTooltip
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
        {text: 'From', value: '/From:\'\' '},
        {text: 'To', value: '/To:\'\' '},
        {text: 'Subject', value: '/Subject:\'\' '},
        {text: 'Message Contents', value: '/Message_Contents:\'\' '},
        {text: 'ID', value: '/ID:\'\' '}
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

/* Tooltip container */
.tooltip {
    position: relative;
    display: inline-block;
    border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
}

/* Tooltip text */
.tooltip .tooltiptext {
    visibility: hidden;
    width: 120px;
    background-color: #555;
    color: #fff;
    text-align: center;
    padding: 5px 0;
    border-radius: 6px;

    /* Position the tooltip text */
    position: absolute;
    z-index: 1;
    bottom: 125%;
    left: 50%;
    margin-left: -60px;

    /* Fade in tooltip */
    opacity: 0;
    transition: opacity 0.3s;
}

/* Tooltip arrow */
.tooltip .tooltiptext::after {
    content: "";
    position: absolute;
    top: 100%;
    left: 50%;
    margin-left: -5px;
    border-width: 5px;
    border-style: solid;
    border-color: #555 transparent transparent transparent;
}

/* Show the tooltip text when you mouse over the tooltip container */
.tooltip:hover .tooltiptext {
    visibility: visible;
    opacity: 1;
}

</style>
