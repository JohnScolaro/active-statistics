## Active Statistics

Strava is a fantastic website, and shows a small number of highly polished visualisations. I often have ideas for plots I'd like to see that Strava doesn't show + I don't think should be too hard to produce. Luckily, Strava has an absolutely fabulous API to fetch user data from. I had an idea to create an open source website where anyone can contribute whatever visualisations they want, and hopefully we can accumulate a collection of cool visualisations.

## Webserver Setup

Do you want to run this site locally to help develop/fix bugs/make new charts? Here is how to do it:

* These steps may need modification for OSX/Linux, but I'm using WSL2 on Windows for development. You can't run on Windows alone because I use redis for data storage and task queues, and redis doesn't run on Windows (unless in WSL).

1. In WSL, update apt with `sudo apt-get update && sudo apt-get upgrade`
2. Install redis: `sudo apt-get install redis`
3. Start redis: `sudo service redis-server start`
4. Download this repository: `git clone [this-repos-url-here]`
5. Download Python + Pip. (Commands here may differ or not even be necessary on different systems).
    - `sudo apt-get install python3.10`
    - `sudo apt-get install python3.10-venv`
    - `sudo apt-get install python3-pip`
6. Set up the repo:
    - Make a virtual environment with: `python3 -m venv .venv`
    - Enter the virtual environment: `source .venv/bin/activate`
    - Install all website dependencies: `pip install -e.[dev]`
7. Copy the file `example.env` and create a new file called: `dev_local.env`. In this file, replace the `STRAVA_CLIENT_ID` and `STRAVA_CLIENT_SECRET` with your own Strava application ID and secret. To get your own Strava application ID/Secret read Strava's docs [here](https://developers.strava.com/docs/getting-started/).
8. Open repo in your editor of choice. I recommend VSCode because all the launch configurations are set up, but it doesn't matter.
    - If you use VSCode, make sure you're connected to WSL, and that the python extension is installed from the marketplace.
    - Run the "ActiveStatistics (Local)" launch config, and this will run everything correctly for you. If you're not using VSCode, you'll have to inspect the run config to find the exact commands to run the server and rq workers, and the environment file to pass them.

## Tests

Again, if you're using VSCode, these should be picked up automatically. Otherwise, run from the command line with: `pytest .` root of the repo. Warning: The tests also need environment variables passed into them which is automatically handled by vscode, so if you're not using VSCode you'll need to add them yourself.
