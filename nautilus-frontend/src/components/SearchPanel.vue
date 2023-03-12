<template>
  <div class="panel">
    <div class="search-panel">
      <div class="search-bar">
        <input
          class="text-area"
          v-model.trim="searchValue"
          placeholder="Search for ticker symbols or companies"
          @keypress.enter="retrieveStockData"
        />
        <button
          class="search-btn"
          @click="retrieveStockData"
          :disabled="searchValue == ''"
        >
            Search
        </button>
      </div>
      <div v-if="emptyData" class='search-msg'>
        No data found
      </div>
    </div>
    <div class="interval" v-for="(interval, idx) in intervals" :key="interval">
      <IntervalSelector
        :interval="interval"
        :selected="selectedIdx === idx"
        @clicked="clicked(idx)"/>
    </div>
  </div>
</template>

<script>
import stockService from '../services/stockService'
import IntervalSelector from './IntervalSelector.vue'
import { inject } from 'vue'

export default {
  name: 'SearchPanel',
  components: {
    IntervalSelector
  },
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
      searchValue: 'S&P 500',
      currentValue: 'S&P 500',
      emptyData: false,
      selectedIdx: 4,
      intervals: ['5D', '60D', 'YTD', '1Y', '2Y']
    }
  },
  methods: {
    retrieveStockData () {
      const id = this.searchValue ? this.searchValue : this.currentValue
      stockService.getStock(
        id,
        this.intervals[this.selectedIdx]
      ).then(
        data => {
          if (data.data?.length === 0) {
            this.emptyData = true
          } else {
            this.emptyData = false
            this.stockData = data
            this.stockName = data.name
            this.currentValue = id
          }
          this.searchValue = ''
        }
      )
    },
    clicked (idx) {
      this.selectedIdx = idx
      this.retrieveStockData()
    }
  },
  mounted () {
    this.retrieveStockData()
  }
}
</script>

<style scoped>
.search-panel {
  margin: auto;
  width: 80%;
  padding: 15px;
  background-color: rgba(245, 242, 242, 0.514);
}
.search-msg {
  padding-top: 3px;
  padding-left: 30%;
  padding-bottom: 5px;
  color: rgb(247, 96, 96);
}
.text-area {
  margin-left: 7%;
  width: 50%;
  height: 20px;
  font-family: "Times New Roman", Times, serif;
  font-size: 16px;
  background-color: rgba(255, 255, 255, 0.719);
}
.search-btn {
  background-color: rgb(0, 183, 255);
  border: rgb(0, 183, 255);
  color: white;
  display:inline-block;
  vertical-align: top;
  height: 26px;
  border-radius: 5%;
}
.search-btn:disabled {
  background-color: rgb(185, 221, 236);
}
.search-btn:hover {
  cursor: pointer;
}
.search-bar {
  padding-left: 25%;
}
.interval {
  display: inline-block;
  position: relative;
  left: 42%;
  margin: 5px;
}
</style>
