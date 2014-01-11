#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (c) 2014 xavier <xavier@laptop-300E5A>

'''Dashboard

Usage:
  dashboard -h | --help
  dashboard --version
  dashboard new --team-dashboard=<loc> --portfolios=<pf> [--templates=<loc>]

Options:
  -h --help               Show this screen.
  --version               Show version.
  --team-dashboard=<loc>  team dashboard repository path.
  --portfolios=<pf>       comma separated list of portfolio ids
  --templates=<loc>       templates directory path [default: ./templates].
'''


import jinja2
import logbook
from docopt import docopt


log = logbook.Logger('intuition.plugins.dashboard')


class Dashboard(object):
    completion = {'panel': []}
    properties = {}

    def __init__(self, templates, dashboard):
        self.templates_path = templates
        self.dashboard_path = dashboard

    def build(self):
        tpl_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.templates_path))
        template = tpl_env.get_template('dashboard_block.tpl')
        log.info('Rendering templates')
        document = template.render(self.completion)
        fd = open(
            '{}/lib/tasks/populate.rake'.format(self.dashboard_path), 'w')
        fd.write(document)
        fd.close()

    def add_description(self, portfolio, remote_ip='127.0.0.1', title=None):
        title = title or portfolio
        log.info('registering {} dashboard'.format(title))
        self.completion['panel'].append(
            {
                'i': len(self.completion['panel']) + 1,
                'title': title,
                'proxy_ip': remote_ip,
                'proxy_port': 5000,
                'portfolio': portfolio
            }
        )
        return self.completion


if __name__ == '__main__':
    args = docopt(__doc__, version='dashboard 0.0.1')

    if args['new']:
        dash = Dashboard(
            args['--templates'], args['--team-dashboard'])

        portfolios = args['--portfolios'].split(',')
        for pf in portfolios:
            dash.add_description(pf)

        dash.build()

        'rake cleanup'
        'rake custom_populate'
        'rails server -p 3333 -b 0.0.0.0 '
