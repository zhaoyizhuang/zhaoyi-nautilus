from rest_framework import viewsets
from rest_framework.response import Response

import yfinance as yf
import json

class StockViewSet(viewsets.ViewSet):

    def retrieve(self, request, pk=None):
        """
        request: incoming request
        pk: Ticker of the stock

        Given Ticker, retrive stock data for the last 2 years 

        return: 
            Response with status = 400 and error msg if data is empty for the Ticker
            Response with status = 200 and stock data if data retrieved successfully
        """
        stock = yf.Ticker(pk)
        hist = stock.history(period="2y")

        if hist.empty:
            return Response(data={'data': []})
        
        self._simple_moving_average(hist, 50)
        self._simple_moving_average(hist, 200)
        json_format_data = hist.to_json(orient="table", date_format='iso')
        result = json.loads(json_format_data)

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