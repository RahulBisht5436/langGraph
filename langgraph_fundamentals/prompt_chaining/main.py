# Import the core components required to build the LangGraph
from langgraph.graph import StateGraph, END, START

# Import the node functions.
# Each node represents a step in our graph workflow.
from langgraph_fundamentals.prompt_chaining.node_functions import (
    search_details,
    search_outline
)

# Import the state definition used by the graph.
# This state contains the data that flows between nodes.
from langgraph_fundamentals.prompt_chaining.state import searchState


# ---------------------------------------------------------
# 1. Create the Graph
# ---------------------------------------------------------

# StateGraph creates a graph whose state will follow
# the structure defined in searchState.
graph = StateGraph(searchState)


# ---------------------------------------------------------
# 2. Add Nodes
# ---------------------------------------------------------

# Add the "search_outline" node.
# This node will generate/create the outline for the topic.
graph.add_node("search_outline", search_outline)

# Add the "search_details" node.
# This node will generate detailed information based
# on the outline produced by the previous node.
graph.add_node("search_details", search_details)


# ---------------------------------------------------------
# 3. Define the Flow / Edges
# ---------------------------------------------------------

# START -> search_outline
#
# The graph execution starts from START and moves
# to the search_outline node.
graph.add_edge(START, "search_outline")


# search_outline -> search_details
#
# After the outline is generated, the result/state
# is passed to the search_details node.
graph.add_edge("search_outline", "search_details")


# search_details -> END
#
# Once the detailed information is generated,
# the graph execution finishes.
graph.add_edge("search_details", END)


# ---------------------------------------------------------
# 4. Compile the Graph
# ---------------------------------------------------------

# compile() converts the graph definition into an
# executable LangGraph application.
searcImplementation = graph.compile()


# ---------------------------------------------------------
# 5. Get User Input
# ---------------------------------------------------------

# Ask the user which topic they want to understand.
topic = input("What is the topic You want to understand \n")


# ---------------------------------------------------------
# 6. Execute / Invoke the Graph
# ---------------------------------------------------------

# invoke() starts the graph execution.
#
# We pass the user's topic as the initial state.
#
# Flow:
#
# topic
#   ↓
# search_outline
#   ↓
# search_details
#   ↓
# END
result = searcImplementation.invoke({
    "topic": topic
})


# ---------------------------------------------------------
# 7. Display the Final Result
# ---------------------------------------------------------

# Print the final state returned by the graph.
print(result)