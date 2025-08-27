# Use the latest official Python image
FROM python:slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the ports for FastAPI (8000) and Streamlit (8501)
EXPOSE 8000 8501

# Start both the FastAPI and Streamlit apps
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & streamlit run ui.py --server.port 8501 --server.address 0.0.0.0"]

# docker build -t chatbot-langraph-fastapi .f
# docker run -d -p 8000:8000 -p 8501:8501 --name chatbot-langraph-fastapi-container chatbot-langraph-fastapi
# $ docker tag chatbot-langraph-fastapi buffaloo/chatbot-langraph-fastapi:latest
# docker push buffaloo/chatbot-langraph-fastapi:latest