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
$ streamlit run ui.py
```

      Welcome to Streamlit!

      If you'd like to receive helpful onboarding emails, news, offers, promotions,
      and the occasional swag, please enter your email address below. Otherwise,
      leave this field blank.

      Email:

You can find our privacy policy at https://streamlit.io/privacy-policy

Summary:

- This open source library collects usage statistics.
- We cannot see and do not store information contained inside Streamlit apps,
  such as text, charts, images, etc.
- Telemetry data is stored in servers in the United States.
- If you'd like to opt out, add the following to %userprofile%/.streamlit/config.toml,
  creating that file if necessary:

  [browser]
  gatherUsageStats = false

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.1.8:8501

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](LICENSE)

The class `TavilySearchResults` was deprecated in LangChain 0.3.25 and will be removed in 1.0. An updated version of the class exists in the :class:`~langchain-tavily package and should be used instead. To use it run `pip install -U
:class:`~langchain-tavily` and import as `from :class:`~langchain_tavily import TavilySearch``.

You can see the OpenAPI Swagger doc here:
http://localhost:8000/docs#/
