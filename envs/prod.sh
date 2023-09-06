# A shell script to get secret environment variables from AWS Parameter Store and export to environment variables.

export DOMAIN=$(aws ssm get-parameter --name /active_statistics/app/domain --query Parameter.Value --output text)
export PORT=$(aws ssm get-parameter --name /active_statistics/app/port --query Parameter.Value --output text)
export ENVIRONMENT=$(aws ssm get-parameter --name /active_statistics/app/environment --query Parameter.Value --output text)
export DATA_STORAGE=$(aws ssm get-parameter --name /active_statistics/app/data_storage --query Parameter.Value --output text)
export SENTRY_SERVER_DSN=$(aws ssm get-parameter --name /active_statistics/sentry/server_dsn --query Parameter.Value --output text)
export SENTRY_WORKER_DSN=$(aws ssm get-parameter --name /active_statistics/sentry/worker_dsn --query Parameter.Value --output text)
export STRAVA_CLIENT_ID=$(aws ssm get-parameter --name /active_statistics/strava/client_id --query Parameter.Value --output text)
export STRAVA_CLIENT_SECRET=$(aws ssm get-parameter --name /active_statistics/strava/client_secret --query Parameter.Value --output text)
export FLASK_SECRET_KEY=$(aws ssm get-parameter --name /active_statistics/flask/secret_key --query Parameter.Value --output text)