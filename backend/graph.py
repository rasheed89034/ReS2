from langgraph.graph import StateGraph, END
from backend.state import AgentState
from backend.agents import architect_node, developer_node, tester_node

# ==========================================
# ROUTING LOGIC (The Feedback Loop)
# ==========================================
def tester_router(state: AgentState):
    """
    This function decides what happens after the Tester checks the code.
    """
    passed = state.get("test_passed", False)
    iterations = state.get("iterations", 0)
    
    # Condition 1: If code passes, we are done.
    if passed:
        return "end"
    
    # Condition 2: If code fails but we reached max attempts, stop to prevent infinite loops.
    if iterations >= 3:
        return "end"
        
    # Condition 3: Code failed, send back to Developer to fix it.
    return "continue"

# ==========================================
# GRAPH CONSTRUCTION
# ==========================================
# 1. Initialize the graph with our shared memory
workflow = StateGraph(AgentState)

# 2. Add our agents as nodes in the graph
workflow.add_node("architect", architect_node)
workflow.add_node("developer", developer_node)
workflow.add_node("tester", tester_node)

# 3. Define the sequential flow
workflow.set_entry_point("architect")
workflow.add_edge("architect", "developer")
workflow.add_edge("developer", "tester")

# 4. Add the Conditional Edge (The Loop)
workflow.add_conditional_edges(
    "tester",
    tester_router,
    {
        "continue": "developer", # Go back to Developer
        "end": END               # Finish the process
    }
)

# 5. Compile the engine
graph_engine = workflow.compile()