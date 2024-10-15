#!/bin/sh

# Initialize the database if migrations folder does not exist
if [ ! -d "migrations" ]; then
    flask db init
    # flask db migrate -m "Initial migration"
    # flask db upgrade
fi
flask db migrate
flask db upgrade

# Run the Flask app
exec gunicorn -w 3 -b 0.0.0.0:5000 run:app
