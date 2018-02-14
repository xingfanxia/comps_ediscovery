<template>
  <div id="home-datepicker">
    <datepicker></datepicker>
    <datepicker></datepicker>
  </div>
</template>

<script>
// import Datepicker from 'vuejs-datepicker'

const state = {
  date1: new Date()
}

export default {
  data () {
    return {
      format: 'd MMMM yyyy',
      disabled: {},
      highlighted: {},
      eventMsg: null,
      state: state,
      language: 'en',
      vModelExample: null
    }
  },
  methods: {
    highlightTo (val) {
      if (typeof this.highlighted.to === 'undefined') {
        this.highlighted = {
          to: null,
          daysOfMonth: this.highlighted.daysOfMonth,
          from: this.highlighted.from
        }
      }
      this.highlighted.to = val
    },
    highlightFrom (val) {
      if (typeof this.highlighted.from === 'undefined') {
        this.highlighted = {
          to: this.highlighted.to,
          daysOfMonth: this.highlighted.daysOfMonth,
          from: null
        }
      }
      this.highlighted.from = val
    },
    setHighlightedDays (elem) {
      if (elem.target.value === 'undefined') {
        return
      }
      let highlightedDays = elem.target.value.split(',').map(day => parseInt(day))
      this.highlighted = {
        from: this.highlighted.from,
        to: this.highlighted.to,
        daysOfMonth: highlightedDays
      }
    },
    setDisabledDays (elem) {
      if (elem.target.value === 'undefined') {
        return
      }
      let disabledDays = elem.target.value.split(',').map(day => parseInt(day))
      this.disabled = {
        from: this.disabled.from,
        to: this.disabled.to,
        daysOfMonth: disabledDays
      }
    },
    disableTo (val) {
      if (typeof this.disabled.to === 'undefined') {
        this.disabled = {
          to: null,
          daysOfMonth: this.disabled.daysOfMonth,
          from: this.disabled.from
        }
      }
      this.disabled.to = val
    },
    disableFrom (val) {
      if (typeof this.disabled.from === 'undefined') {
        this.disabled = {
          to: this.disabled.to,
          daysOfMonth: this.disabled.daysOfMonth,
          from: null
        }
      }
      this.disabled.from = val
    },
    openPicker () {
      this.$refs.programaticOpen.showCalendar()
    }
  }
}
</script>

<style scoped>

</style>
