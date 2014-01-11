Intuition as a REST Service
===========================

> This plugin provides a RESTFul interface to intuition


Installation
------------

```console
$ git clone https://github.com/hackliff/intuition-plugins
$ cd intuition-plugins/rest
$ [sudo] pip install -r requirements.txt
```

Currently the plugin searchs for portfolios data in [Rethinkdb](rethinkdb.com).
Check out their installation page and [how to use it in
intuition](https://github.com/hackliff/insights/blob/master/insights/plugins/database.py)


Usage and API
-------------

* In a first console

```console
$ # Rethinkdb informations
$ export DB_HOST=localhost
$ export DB_PORT=28015
$ export DB_NAME=portfolios

$ ./api.py --help
$ ./apy.py --bind 0.0.0.0 --debug
```

* In another terminal

```console
$ curl -X GET http://localhost:5000/api/v1/portfolios?id=chuck&key=portfolio.cash
$ GET /api/v1/portfolios?id=chuck&key=cmr.algo_volatility
$ # the key is the data path (check below), the id the database table (i.e. the argument you gave to --id)

$ # You can retrieve many keys at the same time
$ GET /api/v1/portfolios?id=chuck&key=cmr.algo_volatility&key=portfolio.cash

$ # Or for many portfolios
$ GET /api/v1/portfolios?id=chuck&id=gekko&key=cmr.algo_volatility

$ # You can request time series given epoch times.
$ # If the "to" parameter is missing, it will be set to now
$ GET /api/v1/portfolios?id=chuck&key=portfolio.portfolio_value&from=1389183632
```

Notes
-----

* The [Dashboard plugin](https://github.com/hackliff/intuition-plugins/blob/master/dashboard/readme.md)
uses this API

* At a specific date, intuition stores this type of data

```json
{
    "date": Thu Jan 09 2014 18:58:04 GMT+00:00,
    "id":  "08bc3177-034b-4317-9e8e-d9a160adcafc",
    "positions_value": 49921.24627,
    "returns": -0.023526527502224052,
    "start_date": Thu Jan 09 2014 17:01:04 GMT+00:00,
    "starting_cash": 50000,
    "cmr": {
        "algo_volatility": 0,
        "algorithm_period_return": 0,
        "alpha": -0.0794,
        "benchmark_period_return": 1001,
        "benchmark_volatility": 0,
        "beta": 0,
        "excess_return": -0.0794,
        "information": null,
        "max_drawdown": 0,
        "period_label":  "2014-01",
        "sharpe": null,
        "sortino": 0,
        "trading_days": 1,
        "treasury_period_return": 0.0794
    },
    "portfolio": {
        "capital_used": -51097.572645111206,
        "cash": -1097.572645111206,
        "pnl": -1176.3263751112027,
        "portfolio_value": 48823.6736248888,
        "positions": {
            "USD/JPY": {
            "amount": 47,
            "cost_basis": 104.7801341943,
            "last_sale_price": 104.787,
            "sid":  "USD/JPY"
        }
    }
}
```
