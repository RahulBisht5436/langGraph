from langgraph_fundamentals.conditional_workflow.non_llm_conditional_workflow.state import state

def strike_rate(state:state)->state:
    strike_rate = state["runs"]/state["balls"]
    return {"strike_rate" : strike_rate}
    
def runs_boundary(state:state)->state:
    runs_in_boundary = ( state["four"] * 4 +state["six"] * 6 ) / state["runs"]
    return {"runs_per_boundary": runs_in_boundary * 100}
    
def runs_ball(state:state)->state:
    runs_in_ball = ( state["four"]+state["six"] ) / state["balls"]
    return {"balls_per_boundary": runs_in_ball * 100}

def check_runs_boundary(state:state)->str:
    if state["balls_per_boundary"] > 10: 
        return "good"
    return "improve"

def improve_score(state:state)->state:
    print("Need to imporve score")
    return {}
