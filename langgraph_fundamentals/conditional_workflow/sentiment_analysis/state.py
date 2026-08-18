from typing import Literal
from pydantic import BaseModel, Field


# ============================================================
# 1. Sentiment Analysis Output Schema
# ============================================================
# Used by the LLM to determine the overall sentiment
# of the customer feedback.
class SentimentAnalysis(BaseModel):
    sentiment: Literal["positive", "negative"] = Field(
        description="The overall sentiment of the customer feedback."
    )


# ============================================================
# 2. Diagnosis Output Schema
# ============================================================
# Used by the LLM to diagnose the customer's issue.
#
# The diagnosis contains:
#   - Type of issue
#   - Customer's emotional tone
#   - Urgency of the issue
class RunDiagnosis(BaseModel):

    # Type/category of the customer's issue
    issue_type: Literal[
        "software",
        "UI",
        "hardware",
        "network",
        "unidentifiable"
    ] = Field(
        description="The type of issue described in the customer feedback."
    )

    # Emotional tone expressed by the customer
    tone: Literal[
        "anger",
        "frustration",
        "neutral",
        "polite",
        "satisfied"
    ] = Field(
        description="The emotional tone expressed by the customer."
    )

    # How urgently the issue needs to be handled
    urgency: Literal[
        "high",
        "medium",
        "low"
    ] = Field(
        description="The urgency level of the customer's issue."
    )


# ============================================================
# 3. Negative Response Output Schema
# ============================================================
# Used by the LLM to generate a professional and
# empathetic response for negative customer feedback.
class NegativeResponse(BaseModel):
    negative_response: str = Field(
        description=(
            "A professional and empathetic response "
            "to negative customer feedback."
        )
    )


# ============================================================
# 4. Positive Response Output Schema
# ============================================================
# Used by the LLM to generate a professional and
# appreciative response for positive customer feedback.
class PositiveResponse(BaseModel):
    positive_response: str = Field(
        description=(
            "A professional and appreciative response "
            "to positive customer feedback."
        )
    )


# ============================================================
# 5. LangGraph State
# ============================================================
# This represents the complete state that flows through
# the LangGraph workflow.
#
# Each node can update one or more fields in this state.
from typing import Literal
from pydantic import BaseModel


class State(BaseModel):
    # Initial input
    feedback: str

    # Filled by find_sentiment node
    sentiment: Literal["positive", "negative"] | None = None

    # Filled by run_diagnosis node
    issue_type: Literal[
        "software",
        "UI",
        "hardware",
        "network",
        "unidentifiable"
    ] | None = None

    tone: Literal[
        "anger",
        "frustration",
        "neutral",
        "polite",
        "satisfied"
    ] | None = None

    urgency: Literal[
        "high",
        "medium",
        "low"
    ] | None = None

    # Filled by response nodes
    negative_response: str | None = None
    positive_response: str | None = None