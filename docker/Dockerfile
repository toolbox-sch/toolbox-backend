# Use an official Python runtime as a parent image
FROM python:3.11.9-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        gcc \
        default-libmysqlclient-dev \
        git \
        openssh-client \
    && curl -sSL https://install.python-poetry.org | python -

# Set working directory
WORKDIR /app

# SSH Private Key for git clone, make sure to use the correct key for your repo
ARG SSH_PRIVATE_KEY

RUN mkdir -p /root/.ssh/ \
    && echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa \
    && chmod 600 /root/.ssh/id_rsa \
    && touch /root/.ssh/known_hosts \
    && ssh-keyscan github.com >> /root/.ssh/known_hosts

# Clone the main repository
RUN git clone git@github.com:clxxrlove/toolbox-backend.git .

# Initialize and update submodules
RUN git submodule update --init --recursive

# Copy only requirements to cache them in docker layer
COPY ./pyproject.toml ./poetry.lock /app/

# Install python dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy all files
COPY . /app/

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]