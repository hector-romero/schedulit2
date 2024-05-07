# Schedulit

## URLS:

- Frontend: https://schedulit.hecrom.com

- Django Backend admin: https://schedulit-be.hecrom.com/admin/

- Django Backend API: https://schedulit-be.hecrom.com/api/

- Rails Backend API: https://schedulit-ror.hecrom.com/api/

- Postman: https://www.postman.com/nods-realty/workspace/schedulit-api

## Dependencies and project setup:

    python 3.11

### Install direnv (*optional*)
    
    https://direnv.net/man/direnv-stdlib.1.html

### Install pipenv

```sh
    pip install pipenv
```

### Install requirements:

```sh    
    pipenv install -d
```

## Docker:

The docker setup is working on:
    
    Docker version 20.10.24, build 297e128
    Docker Compose version v2.17.2
    
**Note**: if you're going to use services referencing your `localhost`, you can not access those
directly from within the docker container with the name `localhost` or `127.0.0.1`. The docker way
to access those services is replacing `localhost` by `host.docker.internal`. 


### Execute server with docker:

```sh
    docker-compose up --build
```

## Linters / Inspections

Code analysis tools are setup to ensure better code quality.

```sh
    flake8
    pylint schedulit
```

Code typing anotations are checked using mypy

```sh
    mypy schedulit
```


Code testing with coverage:

```sh
    coverage run
```
