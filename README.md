# Active Statistics

This is Active Statistics! An open source repo webapp for showing off your Strava data in cool ways. It's a little project I made to learn a more about frontend web dev, and visualise Strava data. It's been re-written a few times in different frameworks until I settled on something cheap and maintainable.

## Local Development

When debugging and testing the application locally, you need to run a next.js app, and a python FastAPI application at the same time. Set these up like so:

### Backend Setup

1. Enter the backend folder and make a virtual environment with `cd backend && /path/to/your/python3.13 -m venv .venv`
2. Activate your virtual environment. `source .venv/bin/activate`. (On windows the command is slightly different).
3. Install all development dependencies with `pip install -e ".[dev]"`
4. Create a `.env` file. Use the `.example.env` and just copy it. Replace the Strava API keys with your own. It will run fine locally if the SENTRY_DSN is just a random string, because Sentry isn't ran in development mode.
5. The backend will hit your production AWS DynamoDB tables and S3 buckets, so you'll also have to have authenticated with AWS CLI. Make sure you have the AWS CLI installed and run `aws sso login` or one of the other methods. (I just have the access key and secret locally).
6. Run the application in debug mode with the VSCode launch config, or by running `fastapi run backend/main.py` to run it without the debugger attached.
7. Your backend should now be running on localhost:8000.

### Frontend Setup

1. I guess make sure you have node installed. I'm currently using v23.5.0.
2. Enter the frontend folder with `cd frontend`.
3. Install dependencies with `npm install`.
4. Run with `npm run dev`.
5. (Optional) If running with dev is slow, you can run `npm run builddev` and then serve the built static frontend with `npx serve@latest out`. Since this won't reload frontend changes, this is best for working on the backend.
6. At this point, the frontend should be available on http://localhost:3000, and if the backend is also running, you should have the full application running on your computer.

## Deployment Infra

Since SSHing into EC2 boxes is annoying and error-prone, and since EC2 boxes are expensive (I have a budget of $0 to run this infrequently used webapp), this webapp is deployed entirely serverlessly. When branches are merged to master, the frontend is built (the next.js app is and must remain entirely static), and uploaded to S3. The FastAPI backend is wrapped with Mangum and uploaded as a lambda behind an AWS APIGateway using the AWS SAM framework. Cloudfront sits on top of everything, caching the static files, and a CloudFront function directs incoming static requests to the correct files in S3. Most of the infra is defined in `template.yaml`, and it's deployed with GitHub actions.

The ENTIRE infrastructure stack isn't defined in the `template.yaml` though, simply because I'm a bit lazy. The dynamoDB tables and S3 activity data buckets need to be set up manually. The certificates for the domain name need to be set up manually, and probably a few other things too.

Since traffic for this website is ~3 people / week, this sets the website permanently in the free tier, and allows me to host it.

If you're setting up this pipeline by hand from nothing, the main catches are:

1. You'll need to manually create the S3 frontend bucket in AWS with the name specified in deploy.yaml.
2. You'll need to manually create the ECR repo in AWS with the name specified in deploy.yaml.
3. You'll need to set up Github OIDC with AWS and give the role that GitHub actions assumes enough permissions to run `sam deploy`. It will need permissions to deploy everything in the template.yaml, which is quite a lot.
4. You'll need a bunch of secrets to put into GitHub secrets. Go to deploy.yaml, and ctrl+f "secrets" and you'll see what you need.
5. Comb through template.yaml and replace anything hardcoded. The AcmCertificateArn for cloudfront will obviously need to be replaced with your own domain, because active-statistics.com is mine.

## Testing

This repo has a bunch of backend tests using pytest. If you're using VSCode the `settings.json` file should direct the IDE to the correct location. Otherwise you can run manually with `pytest backend/tests`.