from typing import TypedDict
from pydantic import BaseModel, Field


class DOAResult(BaseModel):
    DOA_summary: str = Field(
        description="A concise explanation of the essay's depth of analysis."
    )

    DOA_score: int = Field(
        description="Depth of Analysis score from 0 to 10.",
        ge=0,
        le=10
    )

class COTResult(BaseModel):
    COT_summary: str = Field(
        description="A concise explanation of the essay's clarity of thought, including strengths and weaknesses."
    )

    COT_score: int = Field(
        description="Clarity of Thought score from 0 to 10.",
        ge=0,
        le=10
    )

class FinalResult(BaseModel):
    final_summary: str = Field(
        description=(
            "A concise overall evaluation of the essay based on "
            "Depth of Analysis, Clarity of Thought, and Language and Grammar."
        )
    )

    final_score: int = Field(
        description="Overall essay score from 0 to 10.",
        ge=0,
        le=10
    )


class LanguageResult(BaseModel):
    language_summary: str = Field(
        description=(
            "A concise explanation of the essay's language and grammar quality, "
            "including major strengths and weaknesses."
        )
    )

    language_score: int = Field(
        description="Language and Grammar score from 0 to 10.",
        ge=0,
        le=10
    )

class state(TypedDict):
    
    topic:str
    essay:str
    
    # Clarity of thought
    COT_summary:str
    COT_score:int
    
    # Depth of Analysis
    DOA_summary:str
    DOA_score:int
    
    #Language and Grammer
    language_summary:str
    language_score:int
    
    #Final Result
    final_summary:str
    final_score:int
    