Dashboard
=========

![Dashboard](https://raw.github.com/hivetech/hivetech.github.io/master/images/QuantDashboard.png)

**Work in progress at a very early stage**, for early adopters and fearless geeks only

This plugin fires up a dashboard to monitor live trading metrics or backtest
results. It uses [Team Dashboard](https://github.com/fdietz/team_dashboard)
which performs http requests that the REST plugin of this repo can use to
return data from [Rethinkdb](rethinkdb.com).


Installation
------------

* Install first [Team Dashboard](https://github.com/fdietz/team_dashboard)

If you have docker installed, you can be on track right away:

```console
# Team dashboard needs a mysql database
# You can use a container as well
$ docker run -d -name mysql brice/mysql

$ docker run -d \
  -e DB_HOST=`docker inspect -format '{{ .NetworkSettings.IPAddress }}' mysql` \
  -e DB_PORT=3306 \
  -e DB_USERNAME=root \
  hivetech/team-dashboard
```

* Then install the [REST Server plugin](https://github.com/hackliff/intuition-plugins/blob/master/rest/readme.md)


Usage
-----

Currently the dashboard supports only Rethinkdb data, so you must to enable
[storage](https://github.com/hackliff/insights/blob/master/insights/plugins/database.py)
in your algorithms.

Then run the REST plugin and finally team_dashboard (with docker or from the
official project instructions)

From the web interface, create new widgets with the http_proxy source. You can
check the [REST plugin specifications](https://github.com/hackliff/intuition-plugins/blob/master/rest/readme.md)
and [team_dashboard proxy documentation](https://github.com/fdietz/team_dashboard/blob/master/HTTP_PROXY.markdown)
to have a full understanding, but here is an example :

```
proxy_url: = http://localhost:5000/api/v1/portfolios?id=gekko&key=portfolio.portfolio_value
value_path = gekko.portfolio_value  # i.e. ${id}.${key - without the first field}
# Other fields are optionals
```
