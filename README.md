# Groundwater Protection Monitoring Report

A data visualization dashboard for monitoring well data.

## Setup

Run the command `pip install -r requirements.txt` to install the required packages.

## Development Server

To run a development server, start the application with `py app.py`. The server defaults to localhost port 8050, `http://127.0.0.1:8050/`.

## Production

Install `gunicorn` and `heroku-cli` to deploy application.
Enable `postgres` and `redis` addons.
