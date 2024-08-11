"""Main function to run the crew for documentation generation."""
import os
from datetime import datetime
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from .crew import CodebaseDocumentationCrew

# Load environment variables from .env file
load_dotenv()

class LLMConfigError(Exception):
    """Custom exception class for bad LLM Configuration information."""
    
    def __init__(self, message, error_code=None):
        super().__init__(message)  # Call the base class constructor with the message
        self.error_code = error_code  # Custom attribute for additional context

    def __str__(self):
        # Customize the string representation of the exception
        return f"{super().__str__()} (Error Code: {self.error_code})"

# LLM Factory
def get_llm(model: str, api_key: str, temperature: float = 0):
    if not api_key:
        raise LLMConfigError("API Key not provided.", error_code=400)
    if model.startswith("claude"):
        return ChatAnthropic(anthropic_api_key=api_key, model=model, temperature=temperature)
    elif model.startswith("gpt"):
        return ChatOpenAI(model=model, temperature=temperature, openai_api_key=api_key)
    else:
        raise LLMConfigError("Invalid model provided.", error_code=400)

# Write a file
def write_utf8_file(output_filepath, content):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    directory, filename = os.path.split(output_filepath)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{current_time}{ext}"
    new_filepath = os.path.join(directory, new_filename)
    
    try:
        with open(new_filepath, 'w', encoding=' utf-8') as file:
            file.write(content)
        print(f"File successfully written to {new_filepath}")
    except IOError as e:
        print(f"An error occurred while writing the file: {e}")

def run_code_documentation():
    repo_path = os.getenv('REPO_PATH', "/path/to/your/repository")
    model = os.getenv('LLM_MODEL')
    api_key = os.getenv('LLM_API_KEY')
    temperature = float(os.getenv('LLM_TEMPERATURE', 0))
    llm = get_llm(model, api_key, temperature)
    CodebaseDocumentationCrew(repo_path, llm).code_documentation_crew().kickoff()

def run_deployment_documentation():
    repo_path = os.getenv('REPO_PATH', "/path/to/your/repository")
    model = os.getenv('LLM_MODEL')
    api_key = os.getenv('LLM_API_KEY')
    temperature = float(os.getenv('LLM_TEMPERATURE', 0))
    llm = get_llm(model, api_key, temperature)
    file_label = os.getenv('FILE_LABEL', "code_documentation")
    CodebaseDocumentationCrew(repo_path, llm, file_label).code_documentation_crew().kickoff()

    