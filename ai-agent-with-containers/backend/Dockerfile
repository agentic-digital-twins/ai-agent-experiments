FROM python:latest

# RUN apt-get update && apt-get install -y curl
# host.docker.internal

# Create python virtual environment
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH 


WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && pip install -r /tmp/requirements.txt

COPY ./src .


# CMD [ "python", "-m", "http.server", "3000" ]
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000" ]
