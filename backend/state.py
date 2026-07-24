from operator import add
from typing import Annotated, TypedDict, Optional, List
from pydantic import BaseModel, Field

class AgentState(TypedDict):
    user_prompt: str
    architecture_plan: Optional[str]
    folder_structure: Optional[dict]
    generated_code: Optional[dict]
    validation_feedback: Optional[str]
    test_passed: bool
    iterations: int
    error_logs: Annotated[list[str], add]


class FileContent(BaseModel):
    file_path: str = Field(
        description="Exact path and filename from the architecture, e.g., 'src/main.py', 'public/index.html', or 'app/api.go'"
    )
    code_content: str = Field(
        description="The complete, functional source code for this file written in the appropriate programming language."
    )

class DeveloperOutput(BaseModel):
    files: List[FileContent] = Field(
        description="List of all required files along with their complete generated source code."
    )
