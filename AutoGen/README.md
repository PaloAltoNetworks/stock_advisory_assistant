# Stock Advisory Assistant

This assistant is powered by [AutoGen](https://github.com/microsoft/autogen). 

## Installation

AutoGen currently supports [Python versions ≥3.10](https://github.com/microsoft/autogen?tab=readme-ov-file#installation).

```
# Check your Python version
python --version
```

### Create a Python Virtual Environment

We recommend using separate Python virtual environments for CrewAI and AutoGen.

```
# Navigate to stock_advisory_assistant/AutoGen/
cd stock_advisory_assistant/AutoGen/

# Create the virtual environment
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Verify Python version
python3 --version
```

### Install Required Libraries

```
pip install -r requirements.txt
```

### Optional: Pre-Pull Docker Image for Code Executor 

This step is optional. If not pulled ahead of time, the Code Executor will automatically fetch the image at runtime. Pre-pulling can reduce startup latency.

```
# Pull the required Docker image
docker pull python:3.12-slim
```

### Optional: Patch Code Executor for Non-Default Docker Sockets 

This is only necessary if Docker runs on a non-default socket (e.g., with [OrbStack](https://orbstack.dev/) on macOS).

AutoGen’s [\_docker\_code\_executor.py](https://github.com/microsoft/autogen/blob/main/python/packages/autogen-ext/src/autogen_ext/code_executors/docker/_docker_code_executor.py)  (v0.44.0) currently does not support custom Docker sockets by default. The patch allows the Docker client to use a custom `base_url`. 

```
# Navigate to stock_advisory_assistant/AutoGen/
cp _docker_code_executor_patch.py .venv/lib/python3.13/site-packages/autogen_ext/code_executors/docker/_docker_code_executor.py
```

To identify the current Docker context and socket:

```
docker context ls
```

If non-default Docker base\_url is needed, update the `my_docker_base` variable in `main.py`

For example,   
`my_docker_base = 'unix://Users/jaychen/.orbstack/run/docker.sock'`

## LLM Configuration

By default, the assistant uses **OpenAI**. You can switch to other supported providers as needed (see **Additional Information**).

### Set API Keys

Create a `.env` file in the project root (`stock_advisory_assistant/`) with the necessary credentials: 

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
// navigate to directory stock_advisory_assistant/AutoGen
python3 main.py

```

### User Login

A set of 10 default users is available:

```
alice, bob, charlie, david, eve, frank, grace, henry, irene, jack
```

Each user’s default password is: `f"{username.upper()}_2025".`  
For example, Alice’s password id `ALICE_2025`

Disable login requirement by setting `login_required=False` variable in `main.py`

## Additional Information

### Use Code Executor

The stock agent uses a **Code Executor** to analyze data and generate plots. This executor runs inside a Docker container.  
Ensure [Docker](https://docs.docker.com/engine/install/) is installed and properly configured on the host system.

By default, outputs from the code executor are stored in `stock_advisory_assistant/AutoGen/container_data/` 

### Use Reinforced Prompts

Although not bulletproof, reinforcing system instructions is one of the most effective ways to mitigate prompt injection attacks. The default system prompts and instructions focus only on the functionalities not the security. We provide a reinforced prompt template to demonstrate the prompt hardening strategy. 

To use the reinforced prompt, update the `prompt` variable in `stock_advisory_assistant/AutoGen/stock_advisory.py`  
`self.prompts = utils.load_prompts('prompts_reinforced.yaml')`

### Changing LLM Providers

The assistant supports multiple LLMs, including OpenAI, Azure OpenAI, Claude 3.5 (via Amazon Bedrock), and Google Gemini. To change LLM provider, update the `model_client` in the `stock_advisory_assistant/AutoGen/stock_advisory.py`  
For example, to use Azure GPT-4o, set the `model_client` variable to   
`self.model_client = get_azure_gpt4o_client()`

Ensure that the `stock_advisory_assistant/.env` file contains the correct keys and configuration (e.g., `AZURE_API_KEY`, `AZURE_API_BASE`, `AZURE_API_VERSION`, etc.).

To add more LLM providers, modify `my_model_clients.py`.   
Refer to the official [AutoGen supported models guide](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/models.html) for detailed instructions.  