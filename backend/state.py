# from typing import TypedDict, Optional
# from operator import add
# from typing import Annotated

# # Yeh humari Shared Memory hai jo teeno agents use karenge
# class AgentState(TypedDict):
#     # 1. User Input
#     user_prompt: str
    
#     # 2. Architect's Output
#     architecture_plan: Optional[str]
#     folder_structure: Optional[dict]
#     pydantic_schemas: Optional[str]
    
#     # 3. Developer's Output
#     generated_code: Optional[str]
    
#     # 4. Tester's Output
#     validation_feedback: Optional[str]
#     test_passed: bool
    
#     # 5. System Controls (Infinite loop se bachne ke liye)
#     iterations: int
#     error_logs: Annotated[list[str], add] # Sare errors ki history yahan add hoti jayegi


from typing import TypedDict, Optional
from operator import add
from typing import Annotated

class AgentState(TypedDict):
    # 1. User Input
    user_prompt: str
    
    # 2. Architect's Output
    architecture_plan: Optional[str]
    folder_structure: Optional[dict]
    pydantic_schemas: Optional[str]
    
    # 3. Developer's Output
    generated_code: Optional[str]
    
    # 4. Tester's Output
    validation_feedback: Optional[str]
    test_passed: bool
    
    # 5. System Controls
    iterations: int
    error_logs: Annotated[list[str], add]