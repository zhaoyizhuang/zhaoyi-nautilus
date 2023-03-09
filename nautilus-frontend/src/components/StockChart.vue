<template>
  <div>
    <div>
      {{ stockName }}
    </div>
    <li v-for="i in stockData" :key="i.Date">
      {{ i }}
    </li>
  </div>
</template>

<script>
import { inject } from 'vue'

export default {
  name: 'StockChart',
  setup () {
    const stockData = inject('stockDataKey')
    const stockName = inject('stockNameKey')
    return {
      stockData,
      stockName
    }
  }
}
</script>

<style scoped>

</style>
