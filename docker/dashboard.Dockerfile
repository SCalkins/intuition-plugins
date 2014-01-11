# Team dashboard image
# VERSION 0.0.1

FROM binaryphile/ruby:2.0.0-p247
MAINTAINER Xavier Bruhiere <xavier.bruhiere@gmail.com>

RUN apt-get install -y git-core libxml2-dev libz-dev libmysqlclient-dev libxslt-dev && \
  gem install bundler && \
  gem install debugger -v '1.6.4' && \
  gem install uglifier -v '2.3.0' && \
  gem install libxml-ruby -v '2.7.0' && \
  gem install rack-test -v '0.6.2'
RUN git clone https://github.com/fdietz/team_dashboard.git /app
RUN cd /app && bundle install --verbose

ADD ./start.sh /app/

ENTRYPOINT ["bash", "/app/start.sh"]

EXPOSE 3000
