FROM python:latest


WORKDIR /app
COPY ./src .

#python -m http.server 8000
#python -m streamlit run ui.py --server.port 8501 --server.address
CMD [ "python", "-m", "http.server", "8000" ]