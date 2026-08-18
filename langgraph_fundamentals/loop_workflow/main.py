from langgraph_fundamentals.loop_workflow.state import State
from langgraph_fundamentals.loop_workflow.node import (
    evaluate_tweet,
    generate_tweet,
    optimize_tweet
)
from langgraph.graph import StateGraph, START, END


graph = StateGraph(State)


# -------------------------
# Add Nodes
# -------------------------

graph.add_node("generate_tweet", generate_tweet)
graph.add_node("optimize_tweet", optimize_tweet)


# -------------------------
# Add Edges
# -------------------------

# START → generate_tweet
graph.add_edge(
    START,
    "generate_tweet"
)


# generate_tweet → conditional router
graph.add_conditional_edges(
    "generate_tweet",
    evaluate_tweet,
    {
        "over_iterated": END,
        "approved": END,
        "needs_improvement": "optimize_tweet"
    }
)


# optimize_tweet → generate_tweet
graph.add_edge(
    "optimize_tweet",
    "generate_tweet"
)


# -------------------------
# Compile Graph
# -------------------------

tweetGraph = graph.compile()


# -------------------------
# Display Graph
# -------------------------

tweetGraph.get_graph().print_ascii()


# -------------------------
# Invoke Graph
# -------------------------

result = tweetGraph.invoke({
    "topic": "Dimagi Naxal",
    "iteration": 0,
    "max_iteration": 10
})


print(result)