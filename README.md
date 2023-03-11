# zhaoyi-nautilus

The project is deployed at https://zhaoyi-nautilus.netlify.app/

This project used Django for backend, Vue.js for frontend.

### Django Part

The Django server provides a restful api - '/stock/{pk}/?interval={interval}' where pk is the company name or ticker symbol, interval is the desired time interval. For more information, please check out the comment in the ./nautilus/v1/views.py StockViewSet.retrieve.

The endpoint uses yfinance library to retrieve stock data, and it is tested in ./nautilus/tests/tests_views.py

django-cors-headers is introduced to deal with the CORS problem. All libraries/packages needed for the Django server is listed in the nautilus/requirements.txt

### Vue.js part

The Vue.js part provides a single-page web to display an interactive chart of the stock. Users can enter the ticker symbols or company names to look up different stocks. Users can also draw an area of interest in the chart. 

The Vue.js part enables eslint to ensure that code is in a good format and to keep its consistent over the codebase. 

axios is introduced to deal with the http request, echarts and vue-echarts are introduced to create the interactive chart.

This part uses process.env to make the development and deployment more convinient. 