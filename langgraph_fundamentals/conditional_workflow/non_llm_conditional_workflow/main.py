from langgraph.graph import StateGraph , START , END
from langgraph_fundamentals.conditional_workflow.non_llm_conditional_workflow.state import state as st
from langgraph_fundamentals.conditional_workflow.non_llm_conditional_workflow.node import strike_rate , runs_boundary , runs_ball , check_runs_boundary , improve_score

graph = StateGraph(st)

#Adding the Node
graph.add_node("strike_rate",strike_rate)
graph.add_node("runs_boundary",runs_boundary)
graph.add_node("runs_ball",runs_ball)
graph.add_node("improve_score", improve_score)


#Adding the Edges

#Parallel Execution
graph.add_edge(START,"strike_rate")
graph.add_edge(START,"runs_ball")
graph.add_edge(START,"runs_boundary")


graph.add_edge("strike_rate" , END )

graph.add_edge("runs_boundary" , END )

graph.add_conditional_edges(
    "runs_ball",
    check_runs_boundary,
    {
        "good":END,
        "improve":"improve_score"
    }
)

graph.add_edge("improve_score",END)

# Compilation Step
cricketGraph = graph.compile()

cricketGraph.get_graph().print_ascii()

result = cricketGraph.invoke({"runs":100,"balls":68 , "four":4,"six":6 })

print(result)