from langgraph_fundamentals.conditional_workflow.sentiment_analysis.state import (
    State,
    SentimentAnalysis,
    RunDiagnosis,
    NegativeResponse,
    PositiveResponse,
)

from Models.openAI_llm import llm
from langchain_core.prompts import PromptTemplate


# ============================================================
# 1. Sentiment Analysis Prompt
# ============================================================

sentiment_prompt = PromptTemplate(
    template="""
You are a sentiment analysis assistant.

Analyze the following customer feedback and determine its overall sentiment.

Customer Feedback:
{feedback}

Classify the sentiment into exactly one of these categories:
- positive
- negative

Rules:
1. Return "positive" when the customer expresses satisfaction,
   appreciation, happiness, or approval.

2. Return "negative" when the customer expresses dissatisfaction,
   anger, frustration, disappointment, or a problem.

3. If the feedback contains both positive and negative statements,
   classify it based on the overall sentiment.

Return the result using the provided structured output schema.
""",
    input_variables=["feedback"]
)


# ============================================================
# 2. Positive Response Prompt
# ============================================================

positive_sentiment_prompt = PromptTemplate(
    template="""
You are a professional customer support assistant.

The customer has provided positive feedback.

Customer Feedback:
{feedback}

Write a warm, professional, and appreciative thank-you response.

Guidelines:
1. Thank the customer for sharing their feedback.
2. Acknowledge their positive experience.
3. Maintain a friendly and professional tone.
4. Keep the response concise, around 2 to 4 sentences.
5. Do not repeat the customer's feedback word-for-word.
6. Do not make unrealistic promises or claims.
7. Do not mention that you are an AI.
8. Return only the final response to the customer.

Response:
""",
    input_variables=["feedback"]
)


# ============================================================
# 3. Negative Diagnosis Prompt
# ============================================================

negative_diagnosis_prompt = PromptTemplate(
    template="""
You are an expert customer support diagnosis assistant.

Analyze the following negative customer feedback and diagnose the issue.

Customer Feedback:
{feedback}

Determine the following:

1. Issue Type

Allowed values:
- software
- UI
- hardware
- network
- unidentifiable

2. Tone

Allowed values:
- anger
- frustration
- neutral
- polite
- satisfied

3. Urgency

Allowed values:
- high
- medium
- low

Important Rules:
- Analyze the overall meaning of the feedback.
- Do not invent information.
- Select exactly one value for each category.
- Return the result using the RunDiagnosis structured output schema.
""",
    input_variables=["feedback"]
)


# ============================================================
# 4. Negative Response Prompt
# ============================================================

negative_response_prompt = PromptTemplate(
    template="""
You are a professional and empathetic customer support assistant.

Generate a thoughtful response to the customer's negative feedback.

Customer Feedback:
{feedback}

Customer Tone:
{tone}

Issue Type:
{issue_type}

Issue Urgency:
{urgency}

Instructions:

1. Acknowledge the customer's concern.
2. Show genuine understanding and empathy.
3. Consider the customer's tone when writing the response.
4. If the tone is angry or frustrated, remain calm and reassuring.
5. Consider the issue type so the response is relevant.
6. Consider the urgency when determining the seriousness of the response.
7. Do not blame the customer.
8. Do not make promises that cannot be guaranteed.
9. Do not invent technical details or solutions.
10. Keep the response professional, concise, and human-like.
11. Do not mention the tone, urgency, or issue type explicitly.
12. Return only the final response.

Response:
""",
    input_variables=[
        "feedback",
        "tone",
        "urgency",
        "issue_type",
    ]
)


# ============================================================
# 5. Sentiment Node
# ============================================================

def find_sentiment(state: State) -> dict:

    llm_structured = llm.with_structured_output(
        SentimentAnalysis
    )

    sentiment_chain = sentiment_prompt | llm_structured

    result = sentiment_chain.invoke({
        "feedback": state.feedback
    })

    return {
        "sentiment": result.sentiment
    }


# ============================================================
# 6. Conditional Routing Function
# ============================================================

def check_sentiment(state: State):

    return state.sentiment


# ============================================================
# 7. Positive Response Node
# ============================================================

def positive_response(state: State) -> dict:

    llm_structured = llm.with_structured_output(
        PositiveResponse
    )

    positive_response_chain = (
        positive_sentiment_prompt
        | llm_structured
    )

    result = positive_response_chain.invoke({
        "feedback": state.feedback
    })

    return {
        "positive_response": result.positive_response
    }


# ============================================================
# 8. Negative Diagnosis Node
# ============================================================

def run_diagnosis(state: State) -> dict:

    llm_structured = llm.with_structured_output(
        RunDiagnosis
    )

    diagnosis_chain = (
        negative_diagnosis_prompt
        | llm_structured
    )

    result = diagnosis_chain.invoke({
        "feedback": state.feedback
    })

    return {
        "issue_type": result.issue_type,
        "urgency": result.urgency,
        "tone": result.tone,
    }


# ============================================================
# 9. Negative Response Node
# ============================================================

def negative_response(state: State) -> dict:

    llm_structured = llm.with_structured_output(
        NegativeResponse
    )

    negative_response_chain = (
        negative_response_prompt
        | llm_structured
    )

    result = negative_response_chain.invoke({
        "feedback": state.feedback,
        "tone": state.tone,
        "urgency": state.urgency,
        "issue_type": state.issue_type,
    })

    return {
        "negative_response": result.negative_response
    }