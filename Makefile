# Makefile
# xavier, 2013-07-30 07:56
#
# vim:ft=make

LOGS?=/tmp/intuition.logs

all: rest

rest:
		apt-get install -y redis-server
		cd rest && python setup.py install

.PHONY: rest
