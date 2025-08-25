# End-to-End-AI-Chatbot-with-Langraph-FastAPI-and-Streamlit-UI

# AI Agent Experiments

This repository contains experiments and demos for building end-to-end AI chatbots using Langraph, FastAPI, and Streamlit.

## Project Structure

- `chatbot-langraph-fastapi/` — Main FastAPI backend and UI code
- `End-to-End-AI-Chatbot-with-Langraph-FastAPI-and-Streamlit-UI/` — Example projects and demos

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/agentic-digital-twins/ai-agent-experiments.git
cd ai-agent-experiments
```

### 2. Set Up a Local Python Environment

It is recommended to use a virtual environment to keep dependencies isolated.

#### a. Install the Latest Python

Download and install the latest Python from [python.org](https://www.python.org/downloads/) if you don't have it already.

#### b. Create a Virtual Environment

```bash
python -m venv venv
```

#### c. Activate the Virtual Environment

- On Windows (bash):
  ```bash
  source venv/Scripts/activate
  ```
- On macOS/Linux:
  ```bash
  source venv/bin/activate
  ```

#### d. Upgrade pip and Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Variables

Store your API keys and secrets in a `.env` file in the project root. Example:

```
API_KEY=your_api_key_here
ANOTHER_KEY=your_other_key_here
```

The application will load these automatically using `python-dotenv`.

### 4. Running the Application

Navigate to the `chatbot-langraph-fastapi` directory and run:

```bash
python app.py
```

Or, for the UI:

```bash
python ui.py
```

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)
