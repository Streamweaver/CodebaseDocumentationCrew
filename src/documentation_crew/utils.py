# Various Utilities
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

# LLM Factory

class LLMConfigError(Exception):
    """Custom exception class for bad LLM Configuration information."""
    
    def __init__(self, message, error_code=None):
        super().__init__(message)  # Call the base class constructor with the message
        self.error_code = error_code  # Custom attribute for additional context

    def __str__(self):
        # Customize the string representation of the exception
        return f"{super().__str__()} (Error Code: {self.error_code})"
    
def get_llm(model: str, api_key: str, temperature: float = 0):
    """A simple LLM factory"""
    if not api_key:
        raise LLMConfigError("API Key not provided.", error_code=400)
    if model.startswith("claude"):
        return ChatAnthropic(anthropic_api_key=api_key, model=model, temperature=temperature)
    elif model.startswith("gpt"):
        return ChatOpenAI(model=model, temperature=temperature, openai_api_key=api_key)
    else:
        raise LLMConfigError("Invalid model provided.", error_code=400)