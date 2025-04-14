
# google-adk-automation

A Python project demonstrating single and multi-agent systems using the **Google Agent Development Kit (ADK)**. This repository includes:

- **weather_agent**: A single agent that provides mock weather data for a given city.
- **multi_agent**: A system with a coordinator, conversation, and researcher agent to handle queries with delegated tasks.

This project is ideal for learning how to build and deploy AI agents with Google ADK.

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


