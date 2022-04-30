# crypto API

A crypto API made using Django Rest Framework 3.13.1. This API provides you a dashboard that displays crypto prices and other details (that are updated every 15 min), a conversion endpoint, and
an endpoint that compares prices of a specific crypto from two input dates that are passed as a url parameter. To make this API, i used other two crypto API's: coinAPI
and CoinMarketCapAPI.

# API Endpoints

/overall/ => (GET, POST)
When requested through GET HTTP method, displays a dashboard with the current cryptos that you have on your database. The maximum cryptos that you can have on
the dashboard is 5. Accepts a POST HTTP that contains the name of the crypto that you want to add to your dashboard.

/overall/<slug>?from={date}&to={date} => (GET)
Can only receive GET HTTP requests. Returns the detail of a specific crypto (wich needs to be on your database). Accepts two parameters: from and to; both receive a date in the format of a YYYY-mm-dd and
returns the price of the current crypto in those specified dates and a percent change of the price from one date to another.
    
/convert/ (POST)
The body of the HTTP POST method must have these informations: fromCoin (the crypto that you wanna convert), toCoin (the crypto that you wanna receive), amount (the
amount to be converted). P.S.: you can only convert cryptos that you have on your database.
