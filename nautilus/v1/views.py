from rest_framework import viewsets
from rest_framework.response import Response

import yfinance as yf
import json
import pandas as pd
import datetime

class StockViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        """
        request: incoming request
        pk: Ticker of the stock

        Given Ticker, retrive stock data for the last 2 years 

        return: 
            Response with status = 400 and error msg if data is empty for the Ticker
            Response with status = 200 and stock data if data retrieved successfully

            The return data looks like following:
            {
                data: {
                    50DSMA: [4366.11, 4288.28, 4293.62],
                    200DSMA: ['', 4357.94, 4374.35],
                    columns: ['Open', 'Close', 'Low', 'High'],
                    data: [
                        [3891.99, 3898.81, 3885.73, 3917.35],
                        [3915.54, 3900.34, 3815.54, 3960.27],
                        [3924.52, 3943.34, 3915.21, 3944.99]
                    ],
                    index: ['2021-03-10', '2021-03-11', '2021-03-12'],
                    volume: [
                        [0, 5847380000, -1],
                        [1, 5312880000, 1],
                        [2, 4476280000, -1]
                    ]
                }
            }
            
            Where 50DSMA and 200DSMA represents 50/200 days simple moving average,
            data represents daily OCLH for the stock, 
            volume represents [index, volume, 1 if (today's open > today's close) else -1]

        """
        stock = yf.Ticker(pk)
        hist = stock.history(period='2y')

        if hist.empty:
            return Response(data={'data': []})
        
        self._simple_moving_average(hist, 50)
        self._simple_moving_average(hist, 200)

        hist['Volume'] = hist.apply(
            lambda x: [x['Volume'], 1] if x['Open'] > x['Close'] else [x['Volume'], -1],
            axis=1
            )

        data = hist[['Open', 'Close', 'Low', 'High']].round(2).copy()
        json_format_data = data.to_json(orient='split', date_format='epoch')
        result = json.loads(json_format_data)
        result['index'] = [
            datetime.datetime.fromtimestamp(x/1000.0).strftime('%Y-%m-%d') 
            for x in result['index']
            ]
        result['50DSMA'] = pd.Series(hist['50D-SMA']).fillna('').tolist()
        result['200DSMA'] = pd.Series(hist['200D-SMA']).fillna('').tolist()
        result['volume'] = [
            [idx, item[0], item[1]] for idx, item in enumerate(pd.Series(hist['Volume']).tolist())
            ]

        return Response(data=result)
    
    def _simple_moving_average(self, data, time_period):
        '''
        data: pandas.dataframe, represents the history data of a stock.
              data must contains a column 'Close'
        time_period: int, represents the time periods for moving average.

        Calculate the moving average for a stock, 
        and add a new column `${time_period}D-SMA` to the data frame.

        return: no return value, the data is mutated.
        '''
        data[str(time_period) + 'D-SMA'] = data['Close'].rolling(window=time_period).mean().round(2)