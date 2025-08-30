FROM python:latest

# Create python virtual environment
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH 


WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && pip install -r /tmp/requirements.txt

COPY ./src .


CMD [ "python", "-m", "http.server", "8000" ]