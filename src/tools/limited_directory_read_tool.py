"""A custom tool to list files in a directory with the option to ignore specific subdirectories."""
import os
from typing import Optional, Type, Any, List
from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
    
class DirectoryReadToolSchema(BaseModel):
    """
    Schema for the CustomDirectoryReadTool.

    Attributes:
        directory (str): Mandatory directory to list content.
        ignore_dirs (Optional[List[str]]): List of subdirectories to ignore. Defaults to None.
    """
    directory: str = Field(..., description="Mandatory directory to list content")
    ignore_dirs: Optional[List[str]] = Field(default=None, description="List of subdirectories to ignore")

class DirectoryReadTool(BaseTool):
    """
    A tool that can be used to recursively list a directory's content.
    Args:
        directory (Optional[str]): The directory to list the content of. If not provided, the directory will be set to None.
        ignore_dirs (Optional[List[str]]): A list of directories to ignore during the listing process. If not provided, the list will be set to None.
    Attributes:
        name (str): The name of the tool, set to "List files in directory".
        description (str): The description of the tool, initially set to "A tool that can be used to recursively list a directory's content.".
        args_schema (Type[BaseModel]): The schema for the tool's arguments, set to CustomDirectoryReadToolSchema.
        directory (Optional[str]): The directory to list the content of. If not provided, the directory will be set to None.
        ignore_dirs (Optional[List[str]]): A list of directories to ignore during the listing process. If not provided, the list will be set to None.
    Methods:
        __init__(self, directory: Optional[str] = None, ignore_dirs: Optional[List[str]] = None, **kwargs):
            Initializes the CustomDirectoryReadTool instance.
        _run(self, **kwargs: Any) -> Any:
            Executes the tool and returns the list of file paths in the specified directory.
        _generate_description(self) -> None:
            Generates the description of the tool based on the provided directory and ignore_dirs.
    """
    name: str = "List files in directory"
    description: str = "A tool that can be used to recursively list a directory's content."
    args_schema: Type[BaseModel] = CustomDirectoryReadToolSchema
    directory: Optional[str] = None
    ignore_dirs: Optional[List[str]] = None

    def __init__(self, directory: Optional[str] = None, ignore_dirs: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)
        self.ignore_dirs = ignore_dirs or []
        if directory is not None:
            self.directory = directory
            self.description = f"A tool that can be used to list {directory}'s content."
            self.args_schema = CustomDirectoryReadToolSchema
            self._generate_description()

    def _run(
            self, 
            **kwargs,
            ) -> Any:
        directory = kwargs.get('directory', self.directory)
        ignore_dirs = kwargs.get('ignore_dirs', self.ignore_dirs)
        
        if directory[-1] == "/":
            directory = directory[:-1]
        
        files_list = []
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            for filename in files:
                file_path = os.path.join(root, filename).replace(directory, '').lstrip(os.path.sep)
                files_list.append(f"{directory}/{file_path}")
        
        files = "\n- ".join(files_list)
        return f"File paths: \n- {files}"

    def _generate_description(self) -> None:
        ignore_dirs_str = ", ".join(self.ignore_dirs) if self.ignore_dirs else "None"
        self.description = (
            f"A tool that can be used to list {self.directory}'s content. "
            f"Ignoring subdirectories: {ignore_dirs_str}"
        )