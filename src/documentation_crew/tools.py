"""A custom tool to list files in a directory with the option to ignore specific subdirectories."""
import os
from pathlib import Path
from typing import Optional, Type, Any, List, Dict
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
    args_schema: Type[BaseModel] = DirectoryReadToolSchema
    directory: Optional[str] = None
    ignore_dirs: Optional[List[str]] = None

    def __init__(self, directory: Optional[str] = None, ignore_dirs: Optional[List[str]] = None, **kwargs):
        super().__init__(**kwargs)
        self.ignore_dirs = ignore_dirs or []
        if directory is not None:
            self.directory = directory
            self.description = f"A tool that can be used to list {directory}'s content."
            self.args_schema = DirectoryReadToolSchema
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
                path = Path(f"{directory}/{file_path}")
                files_list.append(path.as_posix())
        
        files = "\n- ".join(files_list)
        return f"File paths: \n- {files}"

    def _generate_description(self) -> None:
        ignore_dirs_str = ", ".join(self.ignore_dirs) if self.ignore_dirs else "None"
        self.description = (
            f"A tool that can be used to list {self.directory}'s content. "
            f"Ignoring subdirectories: {ignore_dirs_str}"
        )

class AbsPathFileReadToolSchema(BaseModel):
    """Schema for the AbsPathFileReadTool."""
    file_path: str = Field(..., description="The path to a specific file to be read.")
    encoding: str = Field("utf-8", description="The encoding to use when reading the file.")

class AbsPathFileReadTool(BaseTool):
    """Tool to read file contents with path normalization based on a provided base path."""
    name: str = "Read File"
    description: str = "Reads the contents of a file. Normalizes all relative and absolute file paths to a base path."
    args_schema: type[BaseModel] = AbsPathFileReadToolSchema
    base_path: Path
    max_file_size: int = 10 * 1024 * 1024  # 10 MB limit

    def __init__(self, base_path: str, max_file_size: int = 10 * 1024 * 1024, **kwargs):
        """
        Initialize the tool with a base path and optional maximum file size.

        Args:
            base_path (str): The base path for file operations.
            max_file_size (int): Maximum file size in bytes (default 10MB).
        """
        super().__init__(base_path=Path(base_path).resolve(), max_file_size=max_file_size, **kwargs)
        self._cache: Dict[str, str] = {}

    def _normalize_path(self, file_path: str) -> Path:
        """
        Normalize the given file path relative to the base path.

        Args:
            file_path (str): The file path to normalize.

        Returns:
            Path: The normalized absolute path.

        Raises:
            ValueError: If the normalized path is outside the base path.
        """
        normalized_path = (self.base_path / Path(file_path)).resolve()
        if self.base_path not in normalized_path.parents and normalized_path != self.base_path:
            raise ValueError(f"Access denied. File path '{file_path}' is outside the base directory.")
        return normalized_path

    def _run(self, file_path: str, encoding: str = "utf-8") -> str:
        """
        Read and return the contents of the specified file.

        Args:
            file_path (str): The path to the file to be read.
            encoding (str): The encoding to use when reading the file.

        Returns:
            str: The content of the file or an error message.
        """
        try:
            full_path = self._normalize_path(file_path)
            cache_key = f"{full_path}:{encoding}"

            if cache_key in self._cache:
                return f"Content of {full_path} (cached):\n\n{self._cache[cache_key]}"

            if not full_path.is_file():
                return f"Error: '{full_path}' is not a file or does not exist."

            if full_path.stat().st_size > self.max_file_size:
                return f"Error: File '{full_path}' exceeds the maximum allowed size of {self.max_file_size} bytes."

            with open(full_path, 'r', encoding=encoding) as file:
                content = file.read()

            self._cache[cache_key] = content
            return f"Content of {full_path}:\n\n{content}"

        except UnicodeDecodeError:
            return f"Error: Unable to decode '{file_path}' with encoding '{encoding}'. Try a different encoding."
        except ValueError as ve:
            return str(ve)
        except PermissionError:
            return f"Error: Permission denied when trying to read '{file_path}'."
        except Exception as e:
            return f"Error reading file '{file_path}': {str(e)}"
