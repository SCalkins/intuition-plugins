#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2014 xavier <xavier@laptop-300E5A>


'''Intuition api

Usage:
  api -h | --help
  api --version
  api [--bind=<ip>] [--port=<port>] [-d | --debug]

Options:
  -h --help       Show this screen.
  --version       Show version.
  --debug         Activates Flask debug
  --bind=<ip>     Listens on the given ip [default: 127.0.0.1]
  --port=<port>   Listens on the given port [default: 5000]
'''


from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse
import rethinkdb as rdb
import os
from docopt import docopt

app = Flask(__name__)
api = restful.Api(app)


# http://www.rethinkdb.com/api/python/
RDB_CONFIG = {
    'host': os.environ.get('DB_HOST', '172.17.0.3'),
    'port': os.environ.get('DB_PORT', 28015),
    'db': os.environ.get('DB_NAME', 'portfolios')}


def _format_datapoints(pf, field):
    path = field.split('.')
    return [pf[path[0]][path[1]], int(pf['date']['epoch_time'])]


class RethinkdbPortfolios():
    session = rdb.connect(host=RDB_CONFIG['host'],
                          port=RDB_CONFIG['port'],
                          db=RDB_CONFIG['db'])

    def _build_datapoints(self, ids, keys, dt_from, dt_to=None):
        dt_from = rdb.epoch_time(dt_from)
        dt_to = rdb.epoch_time(dt_to) if dt_to else rdb.now()

        data = []
        for portfolio_id in ids:
            for key in keys:
                pfs = rdb.table(portfolio_id).filter(
                    lambda pf: pf['date'].during(
                        dt_from, dt_to)).run(self.session)

                path = key.split('.')
                data.append(
                    {
                        'target': '{}.{}'.format(portfolio_id, path[1]),
                        'datapoints': sorted(
                            [_format_datapoints(pf, key) for pf in pfs],
                            key=lambda point: point[1])
                    })
        return data

    def _build_values(self, ids, keys):
        data = {}
        for portfolio_id in ids:
            data[portfolio_id] = {}
            for key in keys:
                path = key.split('.')
                portfolio = (rdb.table(portfolio_id)
                             .order_by(index=rdb.desc('date'))
                             .limit(1)
                             .pluck(path[0])
                             .run(self.session))
                data[portfolio_id][path[1]] = portfolio[0][path[0]][path[1]]

        return data


class Portfolios(restful.Resource):
    db = RethinkdbPortfolios()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', type=str, action='append', required=True)
        parser.add_argument('key', type=str, action='append', required=True)
        parser.add_argument('from', type=int)
        parser.add_argument('to', type=int)
        #TODO parser.add_argument('date', type=str)
        #TODO parser.add_argument('less', type=float)
        #TODO parser.add_argument('more', type=float)
        args = parser.parse_args()

        if args['from']:
            data = self.db._build_datapoints(
                args['id'], args['key'], args['from'], args['to'])
        else:
            data = self.db._build_values(args['id'], args['key'])

        return data


api.add_resource(Portfolios, '/api/v1/portfolios')

if __name__ == '__main__':
    args = docopt(__doc__, version='Intuition api 0.0.1')

    app.run(host=args['--bind'],
            port=int(args['--port']),
            debug=args['--debug'])
