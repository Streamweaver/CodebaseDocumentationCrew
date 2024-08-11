
import os
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field

class CustomFileReadToolSchema(BaseModel):
    file_path: str = Field(..., description="The path to the file to read, relative to the repository root")

class CustomFileReadTool(BaseTool):
    name: str = "Read File"
    description: str = "Reads the content of a file from the repository. Provide the file path relative to the repository root."
    args_schema: type[BaseModel] = CustomFileReadToolSchema
    base_path: str = Field(..., description="The absolute path to the repository root")

    def __init__(self, base_path: str, **data):
        super().__init__(base_path=os.path.abspath(base_path), **data)

    def _run(self, file_path: str) -> str:
        full_path = os.path.join(self.base_path, file_path.lstrip('/'))
        try:
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return f"Content of {file_path}:\n\n{content}"
        except FileNotFoundError:
            return f"Error: File '{file_path}' not found in the repository."
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"