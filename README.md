## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Tests](#tests)
* [Postman](#postman)

## General info
This is a recruitment project for blabla.

	
## Technologies
Docker\
PostgreSQL\
Django\
Django Rest Framework
	
## Setup
To run this project, you need to have installed and configured Docker and Docker Compose:
https://docs.docker.com/engine/install/ubuntu/
https://docs.docker.com/compose/install/
It's very helpfull to configure Docker according to this doc:
https://docs.docker.com/engine/install/linux-postinstall/

After cloning the repository please:
1. Prepare the .env file. There is an .env.example file to help.
2. Perform these commands in the root directory:

docker-compose needs to be installed!
Check if You have it installed:

```bash
docker-compose version
```

```bash
docker-compose build
docker-compose run web ./manage.py migrate
```

3. To run the app please run:
```bash
docker-compose up
```

## Tests
Perform in the root directory.
```bash
docker-compose run web pytest
```

## Postman
There are two exported Postman Collections in the root directory.
It allows to test the local and Heroku Endpoints by "hand".
