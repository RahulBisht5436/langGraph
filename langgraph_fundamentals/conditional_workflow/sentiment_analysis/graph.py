from langgraph_fundamentals.conditional_workflow.sentiment_analysis.state import State
from langgraph.graph import StateGraph, START, END

from langgraph_fundamentals.conditional_workflow.sentiment_analysis.node import (
    find_sentiment,
    check_sentiment,
    positive_response,
    run_diagnosis,
    negative_response,
)


graph = StateGraph(State)

graph.add_node("find_sentiment", find_sentiment)
graph.add_node("positive_response", positive_response)
graph.add_node("run_diagnosis", run_diagnosis)
graph.add_node("negative_response", negative_response)

graph.add_edge(START, "find_sentiment")

graph.add_conditional_edges(
    "find_sentiment",
    check_sentiment,
    {
        "positive": "positive_response",
        "negative": "run_diagnosis",
    }
)

graph.add_edge(
    "run_diagnosis",
    "negative_response"
)

graph.add_edge(
    "positive_response",
    END
)

graph.add_edge(
    "negative_response",
    END
)

sentimentGraph = graph.compile()