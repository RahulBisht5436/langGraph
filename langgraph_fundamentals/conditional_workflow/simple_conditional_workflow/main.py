import sys
from pathlib import Path

if __name__ == "__main__":
    try:
        from streamlit.runtime.scriptrunner_utils.script_run_context import (
            get_script_run_ctx,
        )
        _streamlit_hosting = get_script_run_ctx() is not None
    except Exception:
        _streamlit_hosting = False

    if not _streamlit_hosting:
        from streamlit.web import cli as stcli

        sys.argv = [
            "streamlit",
            "run",
            str(Path(__file__).resolve()),
            "--server.fileWatcherType",
            "none",
        ]
        sys.exit(stcli.main())

import streamlit as st

from langgraph.graph import StateGraph, START, END

from langgraph_fundamentals.parallel_workflow.simple_parallel_workflow.state import state

from langgraph_fundamentals.parallel_workflow.simple_parallel_workflow.node import (
    final_Analysis,
    language_Analysis,
    COT,
    DOA,
    final_Evaluation,
    changeEssageLLM
    

)


# ---------------------------------------------------------
# LangGraph
# ---------------------------------------------------------

graph = StateGraph(state)

# Adding Nodes
graph.add_node("final_Analysis", final_Analysis)
graph.add_node("DOA", DOA)
graph.add_node("COT", COT)
graph.add_node("language_Analysis", language_Analysis)
graph.add_node("final_Evaluation",final_Evaluation)
graph.add_node("changeEssageLLM",changeEssageLLM)
# Parallel Execution
graph.add_edge(START, "DOA")
graph.add_edge(START, "COT")
graph.add_edge(START, "language_Analysis")


# Join all parallel branches
graph.add_edge("DOA", "final_Analysis")
graph.add_edge("COT", "final_Analysis")
graph.add_edge("language_Analysis", "final_Analysis")
graph.add_edge("final_Analysis", "final_Evaluation")

graph.add_conditional_edges(
    "final_Analysis",
    "final_Evaluation",
    {
        "Passed":END,
        "Failed": "changeEssageLLM"
    })

graph.add_edge("changeEssageLLM", "DOA")
graph.add_edge("changeEssageLLM", "COT")
graph.add_edge("changeEssageLLM", "language_Analysis")

st.title("📝 AI Essay Evaluator")

st.write(
    "Evaluate your essay using AI across Depth of Analysis, "
    "Clarity of Thought, and Language & Grammar."
)


# ---------------------------------------------------------
# Input
# ---------------------------------------------------------

topic = st.text_input(
    "Essay Topic",
    placeholder="Enter your essay topic..."
)


essay = st.text_area(
    "Essay",
    placeholder="Write or paste your essay here...",
    height=300
)


# ---------------------------------------------------------
# Evaluate Button
# ---------------------------------------------------------

if st.button("Evaluate Essay", type="primary"):

    if not topic.strip():
        st.warning("Please enter an essay topic.")

    elif not essay.strip():
        st.warning("Please enter your essay.")

    else:

        with st.spinner("Evaluating your essay..."):

            try:

                result = app.invoke(
                    {
                        "topic": topic,
                        "essay": essay
                    }
                )

                # -------------------------------------------------
                # Final Score
                # -------------------------------------------------

                st.success("Evaluation completed!")

                st.divider()

                st.header("Overall Evaluation")

                st.metric(
                    label="Final Score",
                    value=f"{result['final_score']}/10"
                )

                st.write(result["final_summary"])


                # -------------------------------------------------
                # Individual Scores
                # -------------------------------------------------

                st.divider()

                st.header("Detailed Evaluation")

                col1, col2, col3 = st.columns(3)


                # Depth of Analysis
                with col1:

                    st.subheader("🔍 Depth of Analysis")

                    st.metric(
                        "Score",
                        f"{result['DOA_score']}/10"
                    )

                    st.write(
                        result["DOA_summary"]
                    )


                # Clarity of Thought
                with col2:

                    st.subheader("💡 Clarity of Thought")

                    st.metric(
                        "Score",
                        f"{result['COT_score']}/10"
                    )

                    st.write(
                        result["COT_summary"]
                    )


                # Language
                with col3:

                    st.subheader("📚 Language & Grammar")

                    st.metric(
                        "Score",
                        f"{result['language_score']}/10"
                    )

                    st.write(
                        result["language_summary"]
                    )


                # -------------------------------------------------
                # Raw Result
                # -------------------------------------------------

                with st.expander("View Complete LangGraph State"):

                    st.json(result)


            except Exception as e:

                st.error("An error occurred while evaluating the essay.")

                st.exception(e)