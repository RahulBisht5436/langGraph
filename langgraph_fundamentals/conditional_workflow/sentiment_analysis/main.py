from langgraph_fundamentals.conditional_workflow.sentiment_analysis.state import State 
from langgraph.graph import StateGraph ,START , END
from langgraph_fundamentals.conditional_workflow.sentiment_analysis.node  import (
    find_sentiment,
    check_sentiment,
    positive_response,
    run_diagnosis,
    negative_response,
)

graph = StateGraph(State)

# =================>>> ADDING NODES

graph.add_node("find_sentiment", find_sentiment)

graph.add_node("positive_response", positive_response)

graph.add_node("run_diagnosis", run_diagnosis)

graph.add_node("negative_response", negative_response)



# =================>>> ADDING EDGES

graph.add_edge(START, "find_sentiment")

graph.add_conditional_edges(
    "find_sentiment",
    check_sentiment,
    {
        "positive": "positive_response",
        "negative": "run_diagnosis",
    }
)

graph.add_edge("run_diagnosis","negative_response")
graph.add_edge("positive_response",END)
graph.add_edge("negative_response",END)



# =================>>> Compiling Graph
sentimentGraph = graph.compile()

result = sentimentGraph.invoke( {
    "feedback": "this hotel is very shitty",
    "sentiment": None,
    "issue_type": None,
    "tone": None,
    "urgency": None,
    "negative_response": None,
    "positive_response": None
})


sentimentGraph.get_graph().print_ascii()
print(result)
