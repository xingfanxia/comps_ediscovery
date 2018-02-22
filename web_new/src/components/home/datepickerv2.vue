<script>
import DatePicker from 'vue2-datepicker'

export default {
  components: { DatePicker },
  data () {
    return {
      lang: 'en',
      time1: '',
      shortcuts: [
        {
          text: 'Today',
          start: new Date(),
          end: new Date()
        }
      ]
    }
  },

  methods: {
      getDate: function () {
          this.$emit("dateRange", this.time1)
      }
  }
}
</script>

<template>
  <div>
        <date-picker v-on:selected="getDate" v-model="time1" :lang="lang" range :shortcuts="shortcuts"></date-picker>
        <button v-on:click="getDate">Date</button>
  </div>
</template>
