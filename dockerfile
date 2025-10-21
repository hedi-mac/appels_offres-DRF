FROM python:3.9
# Copy your project files into the container
COPY . /ao_website
# Set the working directory
WORKDIR /ao_website
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /ao_website


COPY requirements.txt /ao_website/
COPY .env /ao_website/
# Install Python packages from requirements.txt
RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
RUN pre-commit install-hooks

# Install Node.js
#RUN apt-get update && apt-get install -y curl
#RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
#RUN apt-get install -y nodejs
#RUN pip install gunicorn

COPY entrypoint.sh /entrypoint.sh
COPY .pre-commit-config.yaml /.pre-commit-config.yaml
# Make the entrypoint script executable
RUN chmod +x /entrypoint.sh


# Expose the port the app runs on
EXPOSE 8000
