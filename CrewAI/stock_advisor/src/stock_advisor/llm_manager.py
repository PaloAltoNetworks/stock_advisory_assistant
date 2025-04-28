from crewai import LLM


# https://docs.crewai.com/concepts/llms#aws-bedrock

class LLMManager:

    def get_openai_gpt4o(self):
        """Return an instance of the OpenAI GPT-4o model."""
        return LLM(
            model="gpt-4o"
        )

    def get_azure_gpt4o(self):
        """Return an instance of the GPT-4o model."""
        return LLM(
            model="azure/gpt-4o-unfiltered",
            api_version="2024-08-01-preview"
        )

    def get_azure_gpto3mini(self):
        """Return an instance of the GPT-3 mini model."""
        return LLM(
            model="azure/o3-mini",
            api_version="2025-01-01-preview"
        )

    def get_aws_claude_35(self):
        """Return an instance of the Claude 3.5 model."""
        return LLM(
            model="bedrock/anthropic.claude-3-5-sonnet-20241022-v2:0",
            # model="anthropic.claude-3-5-sonnet-20241022-v2:0",
        )

    def get_gemini20flash(self):
        """Return an instance of the Gemini 2.0 Flash model."""
        return LLM(
            model="gemini/gemini-2.0-flash-001",
        )