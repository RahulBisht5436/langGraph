from typing import TypedDict , Literal
from pydantic import BaseModel , Field


class GenerateTweet(BaseModel):
    tweet: str = Field(
        ...,
        min_length=1,
        max_length=280
    )
class EvaluateTweet(BaseModel):
    evaluation: Literal["approved", "needs_improvement"] = Field(
        description="Whether the generated tweet is acceptable or needs improvement."
    )

class State(TypedDict):
    topic: str
    tweet:str
    evaluation : Literal["approved","needs_improvement"]
    feedback:str
    iteration:int
    max_iteration:int