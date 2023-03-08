from django.test import TestCase, Client
from v1.views import StockViewSet
from pandas.testing import assert_series_equal

import pandas as pd
import numpy as np

client = Client()

class StockViewSetTestCase(TestCase):
    def test_empty_ticker_data(self):
        response = client.get('/stock/^GSPC3', follow=True)

        assert response.status_code == 200
        assert response.data == {'data': []}

    def test_successfully_retrieve_data(self):
        response = client.get('/stock/^GSPC', follow=True)

        assert response.status_code == 200

    def test_simple_moving_average(self):
        view_set = StockViewSet()
        data = [10,20,30,40,50,70]
        df = pd.DataFrame(data, columns=['Close'])
        view_set._simple_moving_average(df, 3)
        
        expected_df = pd.DataFrame({'3D-SMA': [np.nan, np.nan, 20, 30, 40, 53.33]})
        assert_series_equal(df['3D-SMA'], expected_df['3D-SMA'])

