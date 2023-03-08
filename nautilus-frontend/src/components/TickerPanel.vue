<template>
  <div>
    <div>
      Enter the stock ticker
    </div>
    <textarea v-model.trim="ticker"/>
    <button @click="retrieveStockData" :disabled="ticker == ''">
        Submit
    </button>
    <div v-if="emptyData">
      No data found
    </div>
    <li v-for="i in stockData" :key="i.Date">
      {{ i }}
    </li>
  </div>
</template>

<script>
import stockService from '../services/stockService'

export default {
  name: 'TickerPanel',
  data () {
    return {
      ticker: '^GSPC',
      stockData: [],
      emptyData: false
    }
  },
  methods: {
    retrieveStockData () {
      stockService.getStock(this.ticker).then(
        data => {
          if (data.data?.length === 0) {
            this.emptyData = true
          } else {
            this.emptyData = false
            this.stockData = data.data
          }
        }
      )
    }
  }
}
</script>

<style scoped>

</style>
