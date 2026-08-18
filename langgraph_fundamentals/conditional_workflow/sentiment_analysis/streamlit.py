import streamlit as st

from langgraph_fundamentals.conditional_workflow.sentiment_analysis.graph import (
    sentimentGraph,
)


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Customer Feedback Analyzer",
    page_icon="💬",
    layout="wide",
)


# ============================================================
# Title
# ============================================================

st.title("💬 Customer Feedback Analyzer")

st.write(
    "Enter customer feedback and let the LangGraph workflow "
    "analyze the sentiment, diagnose the issue, and generate "
    "an appropriate response."
)


# ============================================================
# Input
# ============================================================

feedback = st.text_area(
    "Customer Feedback",
    placeholder="Example: The hotel staff was extremely helpful and the room was excellent!",
    height=150,
)


# ============================================================
# Analyze Button
# ============================================================

if st.button("🔍 Analyze Feedback", type="primary"):

    if not feedback.strip():
        st.warning("Please enter some customer feedback.")

    else:

        # ----------------------------------------------------
        # Initial State
        # ----------------------------------------------------

        initial_state = {
            "feedback": feedback,
            "sentiment": None,
            "issue_type": None,
            "tone": None,
            "urgency": None,
            "negative_response": None,
            "positive_response": None,
        }

        # ----------------------------------------------------
        # Run LangGraph
        # ----------------------------------------------------

        with st.spinner("Analyzing feedback..."):

            result = sentimentGraph.invoke(initial_state)


        # ====================================================
        # Result
        # ====================================================

        st.success("Analysis completed successfully!")


        # ====================================================
        # Display Analysis
        # ====================================================

        st.subheader("📊 Analysis")


        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.metric(
                "Sentiment",
                result.get("sentiment", "N/A")
            )


        with col2:
            st.metric(
                "Issue Type",
                result.get("issue_type", "N/A")
            )


        with col3:
            st.metric(
                "Tone",
                result.get("tone", "N/A")
            )


        with col4:
            st.metric(
                "Urgency",
                result.get("urgency", "N/A")
            )


        # ====================================================
        # Customer Feedback
        # ====================================================

        st.subheader("📝 Customer Feedback")

        st.info(result["feedback"])


        # ====================================================
        # Generated Response
        # ====================================================

        sentiment = result.get("sentiment")


        if sentiment == "positive":

            st.subheader("💚 Generated Positive Response")

            st.success(
                result.get(
                    "positive_response",
                    "No response generated."
                )
            )

        elif sentiment == "negative":

            st.subheader("❤️ Generated Negative Response")

            st.error(
                result.get(
                    "negative_response",
                    "No response generated."
                )
            )


        # ====================================================
        # Raw State
        # ====================================================

        with st.expander("🔎 View Complete LangGraph State"):

            st.json(result)


# ============================================================
# Graph Visualization
# ============================================================

st.divider()

st.subheader("🔀 LangGraph Workflow")

st.write(
    "This is the workflow used to process the customer feedback:"
)


try:

    graph = sentimentGraph.get_graph()

    st.code(
        graph.draw_ascii(),
        language="text"
    )

except Exception as e:

    st.warning(
        f"Could not render graph visualization: {e}"
    )