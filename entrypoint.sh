#!/bin/bash

# For testing
# set -a && source /active-statistics/backend/envs/[test.env] && set +a
source /active-statistics/backend/envs/prod.sh
source ~/.bashrc

service redis-server start
sleep 1

# Run python server
nohup gunicorn --bind localhost:5000 active_statistics.wsgi:app &

# Run python workers
nohup rq worker summary_queue --url redis://localhost/1 --config active_statistics.rq_settings &
nohup rq worker detailed_queue --url redis://localhost/1 --config active_statistics.rq_settings &

# Run node server
npm run --prefix /active-statistics/frontend start > out.log 2> err.log

wait
