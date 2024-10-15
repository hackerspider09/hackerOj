# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory in the container

# Copy the current directory contents into the container at /app
COPY . /home/app/

WORKDIR /home/app/server


# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Flask app runs on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=production


# Initialize the database and apply migrations
# Note: Use a script to check if migrations folder exists before running `flask db init`
# Copy entrypoint script to the working directory
COPY server/entrypoint.sh /home/app/server/entrypoint.sh

# Set executable permissions on the entrypoint script
RUN chmod +x /home/app/server/entrypoint.sh

# Run the Flask app
ENTRYPOINT ["/home/app/server/entrypoint.sh"]