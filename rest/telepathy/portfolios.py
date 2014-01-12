# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Xavier Bruhiere


import rethinkdb as rdb
import os


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
