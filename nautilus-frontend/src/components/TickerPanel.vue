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
  </div>
</template>

<script>
import stockService from '../services/stockService'
import { inject } from 'vue'

export default {
  name: 'TickerPanel',
  setup () {
    const stockData = inject('stockDataKey')
    const stockName = inject('stockNameKey')
    return {
      stockData,
      stockName
    }
  },
  data () {
    return {
      ticker: '^GSPC',
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
            this.stockName = this.ticker
          }
        }
      )
    }
  }
}
</script>

<style scoped>

</style>
