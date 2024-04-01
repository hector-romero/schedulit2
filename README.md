# Schedulit

## Dependencies and project setup:

    python 3.11

### Install direnv (*optional*)
    
    https://direnv.net/man/direnv-stdlib.1.html

### Install pipenv

    pip install pipenv


### Install requirements:
    
    pipenv install -d


## Docker:

The docker setup is working on:
    
    Docker version 20.10.24, build 297e128
    Docker Compose version v2.17.2
    
**Note**: if you're going to use services referencing your `localhost`, you can not access those
directly from within the docker container with the name `localhost` or `127.0.0.1`. The docker way
to access those services is replacing `localhost` by `host.docker.internal`. 


### Execute server with docker:

    docker-compose up --build
