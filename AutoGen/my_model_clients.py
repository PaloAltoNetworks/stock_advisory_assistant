import os
from azure.core.credentials import AzureKeyCredential
from autogen_core.models import ModelFamily


def get_openai_client(parallel_tool_calls: bool = False):
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    return OpenAIChatCompletionClient(
        model=os.getenv("OPENAI_MODEL_4o"),
        api_key=os.getenv("OPENAI_API_KEY"),
        model_info={
            "json_output": True,
            "function_calling": True,
            "vision": False,
            "family": ModelFamily.GPT_4O,
            "structured_output": False
        },
        parallel_tool_calls=parallel_tool_calls
    )

def get_azure_gpt4o_client(parallel_tool_calls: bool = False):
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    return AzureOpenAIChatCompletionClient(
        azure_deployment=os.getenv("GPT4o_DEPLOYMENT"),
        model=os.getenv("GPT4o_MODEL"),
        api_version=os.getenv("AZURE_2024API_VERSION"),
        azure_endpoint=os.getenv("AZURE_2024APIGW_BASE"),
        api_key=os.getenv("AZURE_API_KEY"),
        model_info={
            "json_output": True,
            "function_calling": True,
            "vision": False,
            "family": ModelFamily.GPT_4O,
            "structured_output": False
        },
        parallel_tool_calls=parallel_tool_calls
    )

def get_azure_gpto3mini_client(parallel_tool_calls: bool = False):
    from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
    return AzureOpenAIChatCompletionClient(
        azure_deployment=os.getenv("GPTo3mini_DEPLOYMENT"),
        model=os.getenv("GPTo3mini_MODEL"),
        api_version=os.getenv("AZURE_2025API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_BASE"),
        api_key=os.getenv("AZURE_API_KEY"),
        model_info={
            "json_output": True,
            "function_calling": True,
            "vision": False,
            "family": ModelFamily.O3,
            "structured_output": False
        },
        parallel_tool_calls=parallel_tool_calls
    )


def get_anthropic_client():
    from autogen_core.models import UserMessage
    from autogen_ext.models.semantic_kernel import SKChatCompletionAdapter
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion, AnthropicChatPromptExecutionSettings
    from semantic_kernel.memory.null_memory import NullMemory

    sk_client = AnthropicChatCompletion(
        ai_model_id="claude-3-5-sonnet-20241022",
        api_key=os.environ["ANTHROPIC_API_KEY"],
    )
    settings = AnthropicChatPromptExecutionSettings(
        temperature=0.2,
        max_tokens=4000
    )

    anthropic_model_client = SKChatCompletionAdapter(
        sk_client, kernel=Kernel(memory=NullMemory()), prompt_settings=settings,
        model_info={
            "json_output": True,
            "function_calling": True,
            "vision": False,
            "family": ModelFamily.CLAUDE_3_5_SONNET
        }
    )
    return anthropic_model_client

def get_gemini_client():
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.0-flash-001",
        api_key=os.getenv("GEMINI_API_KEY"),
        model_info={
            "json_output": True,
            "function_calling": True,
            "vision": False,
            "family": ModelFamily.GEMINI_2_0_FLASH
        }
    )
    return model_client

def get_bedrock_client():
    from semantic_kernel import Kernel
    from autogen_ext.models.semantic_kernel import SKChatCompletionAdapter
    from semantic_kernel.connectors.ai.bedrock import BedrockChatCompletion, BedrockPromptExecutionSettings
    from semantic_kernel.memory.null_memory import NullMemory
    import boto3

    runtime_client = boto3.client('bedrock-runtime')
    client = boto3.client('bedrock')
    sk_client = BedrockChatCompletion(
        model_id=os.getenv("AWS_CLAUDE_35v2"),
        runtime_client=runtime_client,
        client=client
    )
    settings = BedrockPromptExecutionSettings(
        temperature=0.5,
        top_p=0.9,
        max_tokens=4000,
    )
    return SKChatCompletionAdapter(
        sk_client, 
        kernel=Kernel(memory=NullMemory()), 
        prompt_settings=settings,
        model_info={
            "function_calling": True,
            "json_output": True,
            "vision": False,
            "family": ModelFamily.CLAUDE_3_5_SONNET
        }
    )