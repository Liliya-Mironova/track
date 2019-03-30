#! /bin/sh

TRUNK=/home/katze
BACKEND_DIR=$TRUNK/back
FRONTEND_DIR=$TRUNK/2018-FS-11-Frontend-Mironova
CENTRIFUGE_DIR=$TRUNK/Downloads/centrifuge
DATAGRIP_DIR=$TRUNK/Downloads/DataGrip-2018.2.4/bin
REDIS_CONF=/etc/redis/redis.conf
run_in_new_tab=$TRUNK/back/run-in-new-tab.sh

$run_in_new_tab sudo service memcached restart
$run_in_new_tab $BACKEND_DIR/run.py runserver
$run_in_new_tab $CENTRIFUGE_DIR/centrifugo --admin --config=$CENTRIFUGE_DIR/config.json
$run_in_new_tab "cd $FRONTEND_DIR; npm start"
$run_in_new_tab sh $DATAGRIP_DIR/datagrip.sh
$run_in_new_tab redis-server $REDIS_CONF
$run_in_new_tab "cd $BACKEND_DIR; celery -A app.celery worker --loglevel INFO"
$run_in_new_tab "cd $BACKEND_DIR; flower -A app.celery --port=5555"
