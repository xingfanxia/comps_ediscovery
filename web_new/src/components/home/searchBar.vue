<template>
  <div>
     <div class="row" id="homeSearchBar">
        <datepicker id="dater"></datepicker>
        <div class='col-lg-7'>
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
      <button type="button" class="btn-sm queryButtons" v-for="option in options" @click="addField(option.value)" value="option.value">
        {{ option.text }}
      </button>

    </div>
  </div>
</template>

<script>
import Datepicker from './datepickerv2.vue'

export default {
  components: {
    'datepicker': Datepicker
  },
  data () {
    return {
      inputText: '',
      selected: '',
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
    checkEnter: function() {
      console.log('this works')
      $('#searchBar').keyup(function (event) {
        if (event.keyCode === 13) {
          $('#searchButton').click()
    }
    })
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

</style>
