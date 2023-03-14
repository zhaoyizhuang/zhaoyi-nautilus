<template>
  <div class="panel">
    <div class="search-panel">
      <div class="search-bar">
        <input
          class="text-area"
          v-model.trim="searchValue"
          placeholder="Search for ticker symbols or companies"
          @keypress.enter="enterToAdd"
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
    <div class="tool-bar">
      <button class="tools comparison-tool" @click="showComparisonModal = true">
        Comparison
      </button>
      <div class="tools" v-for="(interval, idx) in intervals" :key="interval">
        <IntervalSelector
          :interval="interval"
          :selected="selectedIdx === idx"
          @clicked="clicked(idx)"/>
      </div>
    </div>
    <ComparisonModal
     :show="showComparisonModal"
    >
      <template v-slot:body>
        <input
         class="comparison-input"
         v-model.trim="comparisonValue"
         placeholder="Add a comparison stock"
        />
      </template>
      <template v-slot:footer>
        <button
          class="search-btn"
          @click="closeModal"
        >
          Close
        </button>
        <button
          class="search-btn comparison-btn"
          @click="addComparison"
          :disabled="comparisonValue == ''"
        >
          Add
        </button>
      </template>
    </ComparisonModal>
  </div>
</template>

<script>
import stockService from '../services/stockService'
import IntervalSelector from './IntervalSelector.vue'
import ComparisonModal from './ComparisonModal.vue'
import { inject } from 'vue'

export default {
  name: 'SearchPanel',
  components: {
    IntervalSelector,
    ComparisonModal
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
      comparisonValue: '',
      emptyData: false,
      selectedIdx: 4,
      intervals: ['5D', '60D', 'YTD', '1Y', '2Y'],
      showComparisonModal: false
    }
  },
  methods: {
    enterToAdd () {
      if (this.searchValue !== '') {
        this.retrieveStockData()
      }
    },
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
    },
    addComparison () {
      this.closeModal()
    },
    closeModal () {
      this.showComparisonModal = false
      this.comparisonValue = ''
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

.tools {
  display: inline-block;
  position: relative;
  left: 37%;
  margin: 5px;
}

.comparison-input {
  width: 100%;
  height: 20px;
  outline: 0;
  border-width: 0 0 2px;
  border-color: rgb(185, 221, 236);
}
.comparison-input:focus {
  border-color: rgb(0, 183, 255);
}

.comparison-btn {
  float: right;
}

.comparison-tool {
  border-width: 0;
  background-color: white;
}
.comparison-tool:hover {
  color: rgb(0, 183, 255);
  cursor: pointer;
}
</style>
