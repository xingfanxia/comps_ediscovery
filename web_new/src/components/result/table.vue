<template>
  <div class="col-lg-12">
    <scale-loader :loading="loading" :color="color" :size="size"></scale-loader>
    <vuetable ref="vuetable"
    :api-url="apiUrl"
    :fields="fields"
    :perPage="perPage"
    pagination-path=""
    detail-row-component="my-detail-row"
    track-by="ID"
    @vuetable:cell-clicked="onCellClicked"
    @vuetable:pagination-data="onPaginationData"
    @vuetable:loaded="onLoaded"
    ></vuetable>
    <div class="vuetable-pagination ui basic segment grid">
      <vuetable-pagination-info ref="paginationInfo"
      ></vuetable-pagination-info>
      <feedback></feedback>
      <vuetable-pagination ref="pagination"
      @vuetable-pagination:change-page="onChangePage"
      ></vuetable-pagination>
    </div>
  </div>
</template>

<script>

import Vue from 'vue'
import Vuetable from 'vuetable-2/src/components/Vuetable'
import VuetablePagination from 'vuetable-2/src/components/VuetablePagination'
import VuetablePaginationInfo from 'vuetable-2/src/components/VuetablePaginationInfo'
import DetailRow from './DetailRow.vue'
import CustomActions from './CustomActions'
import Feedback from './Feedback.vue'
import ScaleLoader from 'vue-spinner/src/ScaleLoader.vue'

Vue.component('custom-actions', CustomActions)
Vue.component('my-detail-row', DetailRow)

export default {

  data () {
    return {
      lastCell : null,
      loading: true,
      color: '#0B5091',
      size: '20px'
    }
  },

  components: {
    'vuetable': Vuetable,
    'vuetable-pagination': VuetablePagination,
    'vuetable-pagination-info': VuetablePaginationInfo,
    'feedback': Feedback,
    ScaleLoader
  },

  props: {
    'apiUrl': String,
    'fields': Array,
    'perPage': Number
  },

  methods: {
    onPaginationData (paginationData) {
      this.$refs.pagination.setPaginationData(paginationData)
      this.$refs.paginationInfo.setPaginationData(paginationData)
    },

    onChangePage (page) {
      this.$refs.vuetable.changePage(page)
    },

    onCellClicked (data, field, event) {
      console.log('cellClicked: ', field.name)
      if (this.lastCell !== data.ID){
        this.$refs.vuetable.hideDetailRow(this.lastCell)
      }
      this.$refs.vuetable.toggleDetailRow(data.ID)
      this.lastCell = data.ID
    },

    onLoaded: function () {     
        this.loading = false;
    }
  }
}

</script>

<style>

.animate-enter-active,
.animate-leave-active {
  -moz-transition: -moz-transform .8s;
  -o-transition: -o-transform .8s;
  -webkit-transition: -webkit-transform .8s;
   -moz-transform-origin: top;
  -ms-transform-origin: top;
  -o-transform-origin: top;
  -webkit-transform-origin: top;
  transform-origin: top;
  transition: transform .8s;
}

.animate-enter ,
.animate-leave-active {
  -moz-transform: scaleY(0);
  -ms-transform: scaleY(0);
  -o-transform: scaleY(0);
  -webkit-transform: scaleY(0);
  transform: scaleY(0);
}

</style>
