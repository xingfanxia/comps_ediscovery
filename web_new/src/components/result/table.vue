<template>
  <div class="col-lg-12">
    <vuetable ref="vuetable"
    :api-url="apiUrl"
    :fields="fields"
    :perPage="perPage"
    pagination-path=""
    detail-row-component="my-detail-row"
    track-by="ID"
    @vuetable:cell-clicked="onCellClicked"
    @vuetable:pagination-data="onPaginationData"
    ></vuetable>
    <div class="vuetable-pagination ui basic segment grid">
      <vuetable-pagination-info ref="paginationInfo"
      ></vuetable-pagination-info>
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

Vue.component('my-detail-row', DetailRow)

export default {

  data () {
    return {
      lastCell: ''
    }
  },

  components: {
    'vuetable': Vuetable,
    'vuetable-pagination': VuetablePagination,
    'vuetable-pagination-info': VuetablePaginationInfo
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
      this.$refs.vuetable.toggleDetailRow(data.ID)
      if (this.lastCell !== '') {
        this.$refs.vuetable.toggleDetailRow(this.lastCell)
      }
      this.lastCell = data.ID
    }
  }
}

</script>
