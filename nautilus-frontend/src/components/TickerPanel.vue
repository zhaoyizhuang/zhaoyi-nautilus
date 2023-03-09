<template>
  <div>
    <div>
      node env: {{ nodeEnv }}
    </div>
    <div>
      back end: {{ backendURL }}
    </div>
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
import Config from '../services/config'

export default {
  name: 'TickerPanel',
  data () {
    return {
      ticker: '^GSPC',
      stockData: [],
      emptyData: false,
      nodeEnv: Config.NODE_ENV,
      backendURL: Config.BACKEND_URL
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
