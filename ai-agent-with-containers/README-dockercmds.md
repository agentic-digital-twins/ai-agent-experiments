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
docker compose down -v --remove-orphans
docker compose up --remove-orphans
docker compose up --build --watch

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

$ curl -X POST -d '{"message": "Hello, World!"}' -H "Content-Type: application/json" http://localhost:3002/api/chats/

$ curl -X POST -d '{"message": "Hello, World!"}' -H "Content-Type: application/json" https://ai-agent-experiments-production.up.railway.app/api/chats/
{"created_at":"2025-09-01T18:06:24.791262Z","message":"Hello, World!","id":1}(venv)

## Docker Model Runner

docker model pull ai/smollm2:135M-Q2_K

_From host terminal_

```bash
curl http://localhost:12434/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

_From within a container_

```bash
curl http://model-runner.docker.internal/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

---

interactively test:

$ docker compose run backend bash
[+] Creating 1/1
✔ Container ai-agent-with-containers-db_service-1 Running 0.0s
root@54299f8768f6:/app# pwd
/app
root@0dcf8fe1f2de:/app# echo $OPENAI_MODEL_NAME # echo environment
ai/smollm2
root@54299f8768f6:/app# ls
**pycache** api main.py
root@54299f8768f6:/app# cd api
root@54299f8768f6:/app/api# ls
**init**.py **pycache** chat db.py
root@54299f8768f6:/app/api# cd chat
root@54299f8768f6:/app/api/chat# ls
**init**.py **pycache** ai_services.py models.py routing.py
root@54299f8768f6:/app/api/chat# python ai_services.py # Don't want to see any errors
root@54299f8768f6:/app/api/chat# python -i ai_services.py

> > > OPENAI_BASE_URL
> > > 'http://model-runner.docker.internal/engines/v1'

---

interactive debug:

$ docker compose run backend bash
time="2025-09-02T09:09:48-05:00" level=warning msg="Found orphan containers ([ai-agent-with-containers-backend-run-adcefb30263c]) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up."
[+] Creating 1/1
✔ Container ai-agent-with-containers-db_service-1 Running 0.0s
root@0dcf8fe1f2de:/app# echo $OPENAI_BASE_MODEL

root@0dcf8fe1f2de:/app# echo $OPENAI_MODEL_NAME
ai/smollm2
root@0dcf8fe1f2de:/app#
root@0dcf8fe1f2de:/app# pwd
/app
root@0dcf8fe1f2de:/app# ls
**pycache** api main.py
root@0dcf8fe1f2de:/app# cd api
root@0dcf8fe1f2de:/app/api# ls
**init**.py **pycache** chat db.py
root@0dcf8fe1f2de:/app/api# cd chat
root@0dcf8fe1f2de:/app/api/chat# ls
**init**.py **pycache** ai_services.py models.py routing.py
root@0dcf8fe1f2de:/app/api/chat# python -i ai_services.py

> > > llm_base.invoke("what is your name?")
> > > AIMessage(content='I am a bot named SmolLM, and I was trained by Hugging Face to provide helpful and concise responses to user queries. I have been trained on a large dataset of text, which enables me to understand context and respond accordingly.', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 49, 'prompt_tokens': 35, 'total_tokens': 84, 'completion_tokens_details': None, 'prompt_tokens_details': None}, 'model_name': 'ai/smollm2', 'system_fingerprint': 'b1-f44f793', 'id': 'chatcmpl-F2oSokAJ8YlcKFg9BBCt8En1XIEAl2jV', 'service_tier': None, 'finish_reason': 'stop', 'logprobs': None}, id='run--bfac0e69-bbf6-40d6-a51a-f1039c5e4253-0', usage_metadata={'input_tokens': 35, 'output_tokens': 49, 'total_tokens': 84, 'input_token_details': {}, 'output_token_details': {}})
