# Pick and choose any language/version you want to run interactively

docker run -it python:3.13.7-trixie

docker run -it node

--- Build and Push ----

docker build -f Dockerfile -t pyapp .

docker run -it pyapp
exit()

docker build -f Dockerfile -t buffaloo/ai-py-app-test:latest .

docker push buffaloo/ai-py-app-test:latest

Starting a new container with an interactive Bash shell:
Code

    docker run -it <image_name_or_id> bash

This command starts a new container from the specified image and immediately provides you with an interactive Bash shell within that container. The -it flags are crucial: -i for interactive mode (keeping STDIN open) and -t for allocating a pseudo-TTY.
Accessing the Bash shell of a running container:
Code

    docker exec -it <container_name_or_id> bash

docker run -it buffaloo/ai-py-app-test:latest bash
exit

------ python built in web server -----
now use Dockerfile

docker build -f Dockerfile -t pyapp .
docker run -it -p 3000:8000 pyapp

----- docker compose help remember what arguments you want on your docker run command ----
----- docker compose lets you specify multiple programs/services --------
docker compose up --remove-orphans
docker compose up --build

WORKDIR /app

# COPY local_folder container_folder

RUN mkdir -p /static_folder
COPY ./static_folder /static_folder

docker compose run backend bash

volumes don't honor dockerignore
develop:
watch:
-action: sync does honor dockerignore
path:

#Databases persist, volumes won't stop
docker compose down
#Databases will be deleted
docker compose down -v
docker compose ps

--- Other

pypi
fastapi
git remote -v
