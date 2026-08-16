# Import the core classes/constants required to build a LangGraph.
#
# StateGraph → Used to create a graph based on a state schema.
# START      → Special node representing the starting point of the graph.
# END        → Special node representing the ending point of the graph.
from langgraph.graph import StateGraph, START, END


# Import the LLM.
#
# The LLM is not directly used in this graph file.
# However, it may be used inside one of the nodes,
# such as getSuggestionBMI(), to generate BMI suggestions.
from Models.openAI_llm import llm


# Import the functions that will act as nodes in our graph.
#
# calculate_BMI:
#     Calculates BMI using weight and height.
#
# getSuggestionBMI:
#     Generates suggestions based on the calculated BMI.
from langgraph_fundamentals.Introduction.nodeBMI import (
    calculate_BMI,
    getSuggestionBMI
)


# Import the state definition used by the graph.
#
# BMIState is a TypedDict that defines the structure
# of the data that flows between the nodes.
#
# Example:
#
# class BMIState(TypedDict):
#     weight: float
#     height: float
#     BMI: float
#
# The state acts as the shared data/context of the graph.
from langgraph_fundamentals.Introduction.state import BMIState


# =========================================================
# 1. CREATE THE GRAPH
# =========================================================

# Create a StateGraph using BMIState as the state schema.
#
# This tells LangGraph:
# "The data flowing through this graph should follow
# the structure defined by BMIState."
#
# The graph will maintain and update this state
# as different nodes execute.
graph = StateGraph(BMIState)


# =========================================================
# 2. ADD NODES
# =========================================================

# A node represents a unit of work in LangGraph.
#
# add_node() takes:
#     1. A unique name for the node.
#     2. A Python function that should be executed
#        when the node is activated.
#
# First node:
#     calculate_BMI
#
# This node reads weight and height from the state
# and calculates the BMI.
graph.add_node("calculate_BMI", calculate_BMI)


# Second node:
#     BMI_suggestion
#
# This node receives the updated state containing BMI
# and generates suggestions based on the BMI value.
graph.add_node("BMI_suggestion", getSuggestionBMI)


# =========================================================
# 3. DEFINE THE GRAPH FLOW
# =========================================================

# START → calculate_BMI
#
# START is the entry point of the graph.
# When the graph starts executing, LangGraph will
# activate the calculate_BMI node first.
graph.add_edge(START, "calculate_BMI")


# calculate_BMI → BMI_suggestion
#
# Once calculate_BMI finishes execution,
# its updated state is passed to the BMI_suggestion node.
#
# Therefore, BMI_suggestion can access the BMI
# calculated by the previous node.
graph.add_edge("calculate_BMI", "BMI_suggestion")


# BMI_suggestion → END
#
# After BMI_suggestion completes its work,
# the graph reaches the END node.
#
# This means there are no more nodes to execute
# and the graph execution is completed.
graph.add_edge("BMI_suggestion", END)


# =========================================================
# 4. COMPILE THE GRAPH
# =========================================================

# compile() converts the graph definition into
# an executable LangGraph application.
#
# After compilation, we can use:
#
#     app.invoke(...)
#
# to execute the graph.
app = graph.compile()


# =========================================================
# 5. INVOKE / EXECUTE THE GRAPH
# =========================================================

# Provide the initial state to the graph.
#
# weight = 100 kg
# height = 1.2 meters
#
# This initial state is passed to the first node:
#
#     calculate_BMI
#
# The node calculates the BMI and returns an
# updated state containing the calculated BMI.
result = app.invoke({
    "weight": 100.00,
    "height": 1.2
})


# =========================================================
# 6. READ THE FINAL STATE
# =========================================================

# result contains the final state produced after
# all nodes in the graph have completed execution.
#
# The execution flow is:
#
# START
#   ↓
# calculate_BMI
#   ↓
# BMI_suggestion
#   ↓
# END
#
# The final state may contain:
#     weight
#     height
#     BMI
#     suggestions
#
# depending on what the nodes return.
print(result)