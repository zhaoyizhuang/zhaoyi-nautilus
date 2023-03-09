<template>
  <div>
    <TickerPanel/>
    <StockChartVue/>
  </div>
</template>

<script>
import TickerPanel from '@/components/TickerPanel.vue'
import StockChartVue from '../components/StockChart.vue'
import { ref, provide } from 'vue'

export default {
  name: 'ChartPage',
  components: {
    TickerPanel,
    StockChartVue
  },
  setup () {
    const stockData = ref([])
    provide('stockDataKey', stockData)

    const stockName = ref('')
    provide('stockNameKey', stockName)
  }
}
</script>

<style scoped>

</style>
