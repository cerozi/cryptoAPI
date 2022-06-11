# Crypto API

A crypto API made using Django Rest Framework 3.13.1. This API provides you a dashboard that displays crypto prices and other details (that are updated every 15 min), a conversion endpoint, and
an endpoint that compares prices of a specific crypto from two input dates that are passed as a url parameter. To make this API, i used other two crypto API's: coinAPI
and CoinMarketCapAPI.

# API Endpoints

| METHOD	          |  ROUTE              | FUNCTIONALITY       |
| ------------------- | ------------------- | ------------------- |
|  GET                |  /overall/          | Displays a dashboard with all the crypto's info   |
|  GET               |  /overall?from=YYYY-mm-dd&to=YYY-mm-dd     | 	Displays crypto info from the received parameters dates and compares each other       |
|  POST               |  /overall/          | 	Adds a new crypto to the dashboard        |
|  POST               |  /convert/     | 	Converts one crypto to another    |

# To run you need to..
* 1. Install Docker on your system.
* 2. Once you have Docker installed, clone this repo.
```
git clone https://github.com/cerozi/cryptoAPI.git
```
* 3. On the project root directory, opens the terminal and build the containers.
```
docker-compose up --build
```
* 4. Now, you can access the API endpoints at http://0.0.0.0:8000/docs
