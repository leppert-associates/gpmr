# Groundwater Protection Monitoring Report

A tool used in analyzing and visualizing monitoring well data for permit reports.

## Setup

Run the command `pipenv install` to install the necessary packages.

## Development Server

To start a development server, first enter the project environment with `pipenv shell`, then start the application by calling the script `py app.py`.

```sh
pipenv shell
py index.py
```

The development will start on localhost port 8050, `http://127.0.0.1:8050/` by default.

## Production

To update `requirements.txt` run `pipreqs --force`. Be sure to add `gunicorn`.
