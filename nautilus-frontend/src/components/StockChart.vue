<template>
  <div class="stock-chart">
    <ECharts v-if="stockData.length !== 0" class="chart" :option="option"/>
  </div>
</template>

<script>
import { inject } from 'vue'
import ECharts from 'vue-echarts'
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { CandlestickChart, LineChart, BarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  ToolboxComponent,
  BrushComponent,
  VisualMapComponent,
} from "echarts/components";

use([
  CanvasRenderer,
  CandlestickChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  ToolboxComponent,
  BrushComponent,
  VisualMapComponent,
  LineChart,
  BarChart
]);

export default {
  name: 'StockChart',
  components: {
    ECharts
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
      upColor: '#00da3c',
      downColor: '#ec0000',
    }
  },
  computed: {
    option() {
      return {
        animation: false,
        legend: {
          data: [this.stockName, 'MA50', 'MA200']
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            animation: false,
            type: 'cross',
            lineStyle: {
              color: '#376df4',
              width: 2,
              opacity: 1
            }
          }
        },
        xAxis: [{
          type: 'category',
          data: this.stockData.index,
          axisLine: { lineStyle: { color: '#8392A5' } },
        },
        {
          type: 'category',
          gridIndex: 1,
          data: this.stockData.index,
          boundaryGap: true,
          axisLine: { onZero: false },
          axisTick: { show: false },
          splitLine: { show: false },
          axisLabel: { show: false },
        }],
        yAxis: [{
          scale: true,
          axisLine: { lineStyle: { color: '#8392A5' } },
          splitArea: { show: true }
        }, 
        {
          scale: true,
          type: 'value',
          gridIndex: 1,
          splitNumber: 2,
          axisLabel: { show: false },
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false }
        }],
        grid: [{
          left: '10%',
          right: '8%',
          height: '50%'
        },
        {
          left: '10%',
          right: '8%',
          top: '72%',
          height: '16%'
        }],
        toolbox: {
          feature: {
            brush: {
              type: ['lineX', 'clear']
            }
          }
        },
        brush: {
          xAxisIndex: 'all',
          brushLink: 'all',
          outOfBrush: {
            colorAlpha: 0.1
          }
        },
        axisPointer: {
          link: [
            {
              xAxisIndex: 'all'
            }
          ]
        },
        visualMap: {
          show: false,
          seriesIndex: 3,
          dimension: 2,
          pieces: [
            {
              value: 1,
              color: this.downColor
            },
            {
              value: -1,
              color: this.upColor
            }
          ]
        },
        dataZoom: [
          {
            type: 'inside',
            textStyle: {
              color: '#8392A5'
            },
            dataBackground: {
              areaStyle: {
                color: '#8392A5'
              },
              lineStyle: {
                opacity: 0.8,
                color: '#8392A5'
              }
            },
            brushSelect: true,
            start: 80
          },
          {
            show: true,
            xAxisIndex: [0, 1],
            type: 'slider',
            top: '90%',
            start: 80
          }
        ],
        series: [
          {
            type: 'candlestick',
            name: this.stockName,
            data: this.stockData.data,
            itemStyle: {
              color: this.upColor,
              color0: this.downColor,
              borderColor: this.upColor,
              borderColor0: this.downColor
            }
          },
          {
            name: 'MA50',
            type: 'line',
            data: this.stockData['50DSMA'],
            smooth: true,
            showSymbol: false,
            lineStyle: {
              width: 1
            }
          },
          {
            name: 'MA200',
            type: 'line',
            data: this.stockData['200DSMA'],
            smooth: true,
            showSymbol: false,
            lineStyle: {
              width: 1
            }
          },
          {
            name: 'Volume',
            type: 'bar',
            xAxisIndex: 1,
            yAxisIndex: 1,
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            },
            data: this.stockData.volume
          }
        ]
      }
    }
  }
}
</script>

<style scoped>
.chart {
  height: 500px;
}
.stock-chart {
  padding: 10px;
}
</style>
