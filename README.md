

# Google ADK Automation: Multi-Agent , Multi-Model Usage  With  RAG System

An advanced Python framework for building single and multi-agent systems powered by the **Google Agent Development Kit (ADK)**, featuring Retrieval-Augmented Generation (RAG) with ChromaDB and multi-model orchestration. This repository demonstrates:

- **weather_agent**: A single agent that provides mock weather data for a given city.
- **multi_agent**: A robust multi-agent system with a coordinator, conversation, and researcher agent, capable of selecting the right model for each task and leveraging RAG for dynamic context retrieval.

This project is ideal for learning, prototyping, and deploying intelligent AI agents that can dynamically choose models and retrieve relevant knowledge for complex workflows using Google ADK and ChromaDB.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Project Structure](#project-structure)
- [Running the Agents](#running-the-agents)
  - [Single Agent: weather_agent](#single-agent-weather_agent)
  - [Multi-Agent System: multi_agent](#multi-agent-system-multi_agent)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before starting, ensure you have:

- **Python 3.11+** installed ([download](https://www.python.org/downloads/)).
- A **Google AI Studio API key** from [Google AI Studio](https://aistudio.google.com/).
- The **Generative Language API** enabled in your Google Cloud project:
  - Go to [Google Cloud Console](https://console.developers.google.com/apis/api/generativelanguage.googleapis.com/overview).
  - Select your project (check AI Studio for the project ID).
  - Click **Enable** and wait 2–5 minutes for propagation.
  - Note: A billing account may be required, even for free-tier usage.
- A command-line interface (e.g., PowerShell, Terminal).
- Optional: Git for cloning the repository.

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kondwani0099/google-adk-automation.git
   cd google-adk-automation
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv env
   .\env\Scripts\activate  # Windows
   # or source env/bin/activate  # macOS/Linux
   ```

3. **Install Dependencies**:
   ```bash
   pip install google-adk
   ```

4. **Configure the API Key**:
   - Create a `.env` file in the project root:
     ```env
     GOOGLE_GENAI_USE_VERTEXAI="False"
     GOOGLE_API_KEY="your-api-key-here"
     ```
   - Replace `"your-api-key-here"` with your Google AI Studio API key.

5. **Verify API Activation**:
   - Ensure the Generative Language API is enabled (see [Prerequisites](#prerequisites)).
   - If you encounter a `403 PERMISSION_DENIED` error later, revisit the Google Cloud Console to confirm.


## Project Structure

```
google-adk-automation/
├── .env
├── weather_agent/
│   ├── __init__.py
│   ├── agent.py
├── multi_agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── conversation.py
│   ├── researcher.py
├── README.md
```

- **weather_agent/**: Single agent for mock weather queries.
- **multi_agent/**: Multi-agent system with a coordinator, conversation, and researcher agent.
- **.env**: Stores API key and configuration.

## RAG System with ChromaDB for Multi-Model Agents

This project integrates a Retrieval-Augmented Generation (RAG) system using [ChromaDB](https://www.trychroma.com/) for efficient embedding and retrieval. The RAG system enables agents to access relevant context and knowledge dynamically, improving their responses and decision-making.

### Multi-Model Use Case

Agents in this system are designed to select the most suitable model for their specific needs and complexity. Each agent can:

- **Embed and retrieve context** using ChromaDB, ensuring fast and accurate access to relevant information.
- **Choose the right model** (e.g., LLM, specialized task model, or domain-specific model) based on the complexity and requirements of the task.
- **Optimize performance** by leveraging multiple models, ensuring that simple tasks use lightweight models while complex tasks utilize more powerful or specialized models.

#### Example Workflow

1. **Agent receives a task** and determines the required context.
2. **Embeddings are generated** and stored/retrieved from ChromaDB.
3. **Agent selects the appropriate model** (from a pool of available models) based on the task's complexity and domain.
4. **Response is generated** using the selected model, with context retrieved via RAG.

This architecture allows for scalable, flexible, and intelligent agent behavior, supporting a wide range of use cases and domains.

## Running the Agents

### Single Agent: weather_agent

The `weather_agent` responds to weather queries (e.g., “What’s the weather in New York?”) with mock data.

1. **Run via CLI**:
   ```bash
   adk run weather_agent
   ```
   - Type a query like “What’s the weather in New York?”.
   - Type `exit` to quit.

2. **Run via Web Interface**:
   ```bash
   adk web
   ```
   - Open `http://localhost:8000`.
   - Select `weather_agent` and enter a query.

**Expected Output**:
```
Sunny, 20°C in New York at [current time]
```

### Multi-Agent System: multi_agent

The `multi_agent` system routes queries through a coordinator to a conversation agent, which delegates research tasks to a researcher agent.

1. **Run via CLI**:
   ```bash
   adk run multi_agent
   ```
   - Try “What’s new in AI?”.
   - Type `exit` to quit.

2. **Run via Web Interface**:
   ```bash
   adk web
   ```
   - Open `http://localhost:8000`.
   - Select `multi_agent` and enter a query.

**Expected Output**:
```
Search results for 'What’s new in AI?': Sample data.
```

## Troubleshooting

- **Error: `module 'X' has no attribute 'agent'`**:
  - Ensure `weather_agent/agent.py` or `multi_agent/agent.py` exists and defines `root_agent`.
  - Verify `__init__.py` imports `root_agent` (e.g., `from .agent import root_agent`).

- **Error: `Agent already has a parent`**:
  - Check `multi_agent/agent.py` to ensure `sub_agents` only includes `conversation_agent`, not `researcher_agent`.
  - Confirm hierarchy: `coordinator` → `conversation` → `researcher`.

- **Error: `403 PERMISSION_DENIED`**:
  - Enable the Generative Language API in [Google Cloud Console](https://console.developers.google.com/apis/api/generativelanguage.googleapis.com/overview).
  - Wait 2–5 minutes and retry.
  - Verify `.env` has the correct API key.

- **Changes Not Taking Effect**:
  - Clear Python cache:
    ```bash
    del weather_agent\__pycache__ /S /Q
    del multi_agent\__pycache__ /S /Q
    ```

- **General Issues**:
  - Update ADK:
    ```bash
    pip install --upgrade google-adk
    ```
  - Check logs: `C:\Users\<YourUsername>\AppData\Local\Temp\agents_log\agent.latest.log`.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

Please include tests and update documentation as needed.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.


