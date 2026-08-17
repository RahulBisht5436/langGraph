from langgraph.graph import StateGraph , START , END
from langgraph_fundamentals.parallel_workflow.non_llm_parallel_workflow.state import state as st
from langgraph_fundamentals.parallel_workflow.non_llm_parallel_workflow.node import strike_rate , runs_boundary , runs_ball

graph = StateGraph(st)

#Adding the Node
graph.add_node("strike_rate",strike_rate)
graph.add_node("runs_boundary",runs_boundary)
graph.add_node("runs_ball",runs_ball)


#Adding the Edges

#Parallel Execution
graph.add_edge(START,"strike_rate")
graph.add_edge(START,"runs_ball")
graph.add_edge(START,"runs_boundary")


graph.add_edge("strike_rate" , END )
graph.add_edge("runs_ball" , END )
graph.add_edge("runs_boundary" , END )


# Compilation Step
cricketGraph = graph.compile()

cricketGraph.get_graph().print_ascii()

result = cricketGraph.invoke({"runs":100,"balls":68 , "four":4,"six":6 })

print(result)