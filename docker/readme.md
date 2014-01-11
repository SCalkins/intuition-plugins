Docker
======

This directory empowers [Intuition](https://github.com/hackliff/intuition) with
[Docker](docker.io). All the necessary stable images are already stored on the
docker repository but you can still use these dockerfiles to improve and build
them by yourself.

All you need is a [docker friendly](http://www.docker.io/gettingstarted/) machine.

Here is a deployment topology example (willingly complex, and complete)

```console
# With the mongodb context, you can store your configurations as mongo docs
$ docker run -d -name mongodb -p 27017:27017 -p 28017:28017 waitingkuo/mongodb

# A database to store metrics
$ docker run -d -name rethinkdb crosbymichael/rethinkdb --bind all

# A dashboard to monitor what's going on
# With its database
$ docker run -d -name mysql brice/mysql
$ docker run -d -name dashboard\
    -e DB_HOST=${MYSQL_IP} \
    -e DB_PORT=3306 \
    -e DB_USERNAME=root \
    hackliff/team-dashboard

# Finally Intuition itself
$ docker run hivetech/intuition \
    --id chuck \
    --context mongodb::${MONGO_IP}:${MONGO_PORT}/${MONGO_DOC_ID}
```

Notea that there is probably a smarter way using [containers
link](http://docs.docker.io/en/latest/use/working_with_links_names/).  But for
now I don't really need it and I'm not completely satisfied with the
environment variables semantic.
