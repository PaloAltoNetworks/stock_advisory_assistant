# Stock Advisory Assistant

This assistant is powered by [CrewAI](https://crewai.com). 

## Installation

CrewAI currently supports [Python versions ≥3.10 and \<3.13](https://docs.crewai.com/installation).

```
# Check your Python version
python --version
```

### Create a Python Virtual Environment

We recommend using separate Python virtual environments for CrewAI and AutoGen.

```
# Navigate to stock_advisory_assistant/CrewAI/
cd stock_advisory_assistant/CrewAI/

# Create a virtual environment using Python 3.12
python3.12 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Confirm the Python version
python3 --version
```

### Install Required Libraries

```
pip install -r requirements.txt
```

### Optional: Pre-Build the Docker Image for Code Interpreter 

This step is optional. If the image doesn't exist, the Code Interpreter tool will build it automatically at runtime. Pre-building it can save time.

```
# Navigate to the correct directory
cd stock_advisory_assistant/CrewAI/stock_advisor

# Build the Docker image
docker build -t code-interpreter .
```

### Optional: Patch Code Interpreter for Non-Default Docker Sockets

This is only required if Docker runs on a non-default socket (e.g., using [OrbStack](https://orbstack.dev/) on macOS).

CrewAI’s [code\_interpreter\_tool.py](https://github.com/crewAIInc/crewAI-tools/blob/main/crewai_tools/tools/code_interpreter_tool/code_interpreter_tool.py) (v0.33.0) currently does not support custom Docker sockets out-of-the-box. The patch updates the Docker client to accept a `base_url`.

```
# Navigate to directory stock_advisory_assistant/CrewAI/
cp code_interpreter_patch.py .venv/lib/python3.12/site-packages/crewai_tools/tools/code_interpreter_tool/code_interpreter_tool.py
```

To identify the current Docker context and socket:

```
docker context ls
```

If non-default Docker base\_url is needed, update the `my_docker_base` variable in `stock_advisory_assistant/CrewAI/stock_advisor/src/stock_advisor/main.py`

Example:

```
my_docker_base = 'unix://Users/jaychen/.orbstack/run/docker.sock'
```

## LLM Configurations

By default, the assistant uses **OpenAI**. You can change the provider as needed (see the **Additional Information** section below).

### Set API Keys

Create a `.env` file in the project root (`stock_advisory_assistant/`) with the required credentials: 

```
# Open AI
OPENAI_API_KEY=
OPENAI_MODEL_4o=gpt-4o-2024-08-06

# Azure OpenAI
AZURE_API_KEY=
AZURE_API_BASE=
AZURE_API_VERSION=

# Amazon Bedrock
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_DEFAULT_REGION=
AWS_CLAUDE_35v2=anthropic.claude-3-5-sonnet-20241022-v2:0

# GCP Gemini
GEMINI_API_KEY=

# Serper: Google Search (Get API key from https://serper.dev/)
SERPER_API_KEY=

```

## Running the Assistant

```
# Navigate to the CrewAI directory
cd stock_advisory_assistant/CrewAI/stock_advisor

# Start the assistant
python3 src/stock_advisor/main.py
```

### User Login

A set of 10 default users is available:

```
alice, bob, charlie, david, eve, frank, grace, henry, irene, jack
```

Each user’s default password is: `f"{username.upper()}_2025".`  
For example, Alice’s password id `ALICE_2025`

To disable login authentication, set `login_required = False` in `stock_advisory_assistant/CrewAI/stock_advisor/src/stock_advisor/main.py`

## Additional Information

### Code Interpreter

The stock agent can invoke a **Code Interpreter** to perform analytics and generate plots. This tool runs inside a Docker container. Ensure [Docker](https://docs.docker.com/engine/install/) is installed and accessible from the host.

By default, interpreter outputs are stored in `stock_advisory_assistant/CrewAI/stock_advisor/container_data/` 

### Use Reinforced Prompts

Although not bulletproof, reinforcing system instructions is one of the most effective ways to mitigate prompt injection attacks. The default system prompts and instructions focus only on the functionalities not the security. We provide a reinforced prompt template to demonstrate the prompt hardening strategy.

To use the reinforced prompt, update the `agents_config` variable in `stock_advisory_assistant/CrewAI/stock_advisor/src/stock_advisor/crew.py`  
`agents_config = 'config/agents_reinforced.yaml'`

### Changing LLM Providers

The stock advisory assistant agent has been tested with OpenAI, Azure OpenAI, Claude 3.5 (on Amazon Bedrock), and Google Gemini. To change LLM provider, update `llm_manager` in   
`stock_advisory_assistant/CrewAI/stock_advisor/src/stock_advisor/crew.py`  
For example, to use Azure OpenAI GPT-4o, set the llm variable to   
`llm = llm_manager.get_azure_gpt4o()`

Ensure corresponding keys and configuration variables are correctly set in the `stock_advisory_assistant/.env` file (e.g., `AZURE_API_KEY`, `AZURE_API_BASE`, etc.).

To add new providers or customize configurations, edit: `stock_advisory_assistant/CrewAI/stock_advisor/src/stock_advisor/crew.py`   
Refer to CrewAI’s official documentation for additional examples and setup guidance:  
[LLM Configuration Guide](https://docs.crewai.com/concepts/llms#openai)