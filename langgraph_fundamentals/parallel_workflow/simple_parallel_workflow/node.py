from langgraph_fundamentals.parallel_workflow.simple_parallel_workflow.state import state , DOAResult , COTResult ,LanguageResult ,FinalResult
from Models.openAI_llm import llm
from langchain_core.prompts import PromptTemplate


DOA_prompt = PromptTemplate(
    template="""
You are an expert essay evaluator.

Analyze the following essay based on its Depth of Analysis.

Topic:
{topic}

Essay:
{essay}

Evaluate the essay based on:

1. Understanding of the topic
2. Depth of reasoning
3. Quality of arguments
4. Supporting evidence
5. Critical thinking
6. Different perspectives
7. Causes, effects, and implications
8. Whether the essay goes beyond superficial statements

Scoring:

0-2: Very shallow analysis
3-4: Limited analysis
5-6: Moderate analysis
7-8: Strong analysis
9-10: Exceptional and highly insightful analysis

Provide your evaluation using the requested structured output.
""",
    input_variables=["topic", "essay"]
)


from pydantic import BaseModel, Field
from langchain_core.prompts import PromptTemplate


class COTResult(BaseModel):
    COT_summary: str = Field(
        description="A concise explanation of the essay's clarity of thought, including strengths and weaknesses."
    )

    COT_score: int = Field(
        description="Clarity of Thought score from 0 to 10.",
        ge=0,
        le=10
    )


COT_prompt = PromptTemplate(
    template="""
You are an expert essay evaluator.

Analyze the given essay based ONLY on the **Clarity of Thought (COT)** demonstrated in the response.

Topic:
{topic}

Essay:
{essay}

Evaluate the clarity of thought based on the following criteria:

1. Clarity of the main idea
2. Clear expression of thoughts and arguments
3. Logical flow between ideas
4. Organization and coherence of the essay
5. Whether each paragraph contributes clearly to the main argument
6. Clear relationships between claims, reasons, and conclusions
7. Avoidance of vague, confusing, or contradictory statements
8. Ability to communicate complex ideas in an understandable manner
9. Consistency of the argument throughout the essay
10. Whether the reader can easily understand what the writer is trying to communicate

Scoring criteria:

0-2:
Very unclear. Ideas are confusing, disconnected, or difficult to understand.

3-4:
Limited clarity. The main idea can be understood, but the essay contains significant
confusion, weak organization, or unclear connections between ideas.

5-6:
Moderately clear. The main argument is understandable and ideas generally follow a
logical structure, but some parts lack clarity or coherence.

7-8:
Strong clarity. Ideas are clearly expressed, logically organized, and easy to follow.
Arguments and conclusions are communicated effectively.

9-10:
Exceptional clarity. Thoughts are extremely clear, precise, coherent, and logically
structured. Complex ideas are communicated effectively with no significant ambiguity.

Important:
- Evaluate ONLY the clarity of thought.
- Do not primarily judge grammar, spelling, vocabulary, or writing style.
- A grammatically correct essay can still have poor clarity of thought.
- A grammatically imperfect essay can still demonstrate strong clarity of thought.
- Focus on whether the writer's thinking and reasoning are clear to the reader.

Provide the evaluation using the requested structured output.
""",
    input_variables=["topic", "essay"]
)



language_prompt = PromptTemplate(
    template="""
You are an expert English language and grammar evaluator.

Analyze the given essay based ONLY on its **Language and Grammar** quality.

Topic:
{topic}

Essay:
{essay}

Evaluate the essay based on the following criteria:

1. Grammatical correctness
   - Correct use of tenses
   - Subject-verb agreement
   - Correct use of articles
   - Correct use of prepositions
   - Correct sentence structures

2. Sentence construction
   - Properly constructed sentences
   - Appropriate sentence length
   - Avoidance of incomplete or run-on sentences
   - Effective use of simple and complex sentences

3. Vocabulary
   - Appropriate word choice
   - Correct use of words
   - Variety of vocabulary
   - Avoidance of unnecessary repetition

4. Spelling
   - Correct spelling of words
   - Consistent spelling throughout the essay

5. Punctuation
   - Correct use of commas
   - Full stops
   - Apostrophes
   - Semicolons
   - Colons
   - Other relevant punctuation

6. Language fluency
   - Natural flow of English
   - Appropriate phrasing
   - Avoidance of awkward expressions

7. Formality and appropriateness
   - Appropriate language for an essay
   - Avoidance of overly informal or conversational expressions

8. Overall language quality
   - How effectively the writer uses English to communicate their ideas.

Scoring criteria:

0-2:
Very poor language and grammar. Frequent grammatical errors, incorrect sentence
structures, spelling mistakes, and punctuation problems make the essay difficult
to understand.

3-4:
Poor language quality. There are frequent grammar and sentence construction errors.
Vocabulary is limited and several mistakes affect readability.

5-6:
Average language quality. The essay is generally understandable but contains
noticeable grammatical, vocabulary, spelling, punctuation, or sentence construction
errors.

7-8:
Good language quality. Grammar is mostly correct, sentences are well constructed,
vocabulary is appropriate, and errors are relatively minor.

9-10:
Excellent language quality. Grammar, sentence construction, vocabulary, spelling,
punctuation, and overall English usage are highly accurate and polished.

Important:
- Evaluate ONLY Language and Grammar.
- Do NOT evaluate the depth of analysis.
- Do NOT evaluate the quality of arguments.
- Do NOT evaluate whether the ideas are insightful.
- Do NOT give a higher score simply because the essay has strong arguments.
- Focus on the correctness, quality, and effectiveness of the English language used.
- Minor errors should have a smaller impact than frequent or serious errors.
- Consider the overall essay rather than penalizing a single isolated mistake.

Provide the evaluation using the requested structured output.
""",
    input_variables=["topic", "essay"]
)

Final_prompt = PromptTemplate(
    template="""
You are an expert essay evaluator.

You have received evaluations of an essay across three dimensions:

1. Depth of Analysis
2. Clarity of Thought
3. Language and Grammar

Topic:
{topic}

Essay:
{essay}

--- Depth of Analysis ---
Score: {DOA_score}
Summary:
{DOA_summary}

--- Clarity of Thought ---
Score: {COT_score}
Summary:
{COT_summary}

--- Language and Grammar ---
Score: {language_score}
Summary:
{language_summary}

Your task is to provide an overall evaluation of the essay.

For the final summary:

- Consider all three evaluation dimensions.
- Identify the essay's strongest aspects.
- Identify the major weaknesses or areas for improvement.
- Give a concise overall assessment.
- Do not simply repeat the three individual summaries.
- The final summary should provide a holistic evaluation of the essay.

The final score will be calculated separately as the average of:

Depth of Analysis score
Clarity of Thought score
Language and Grammar score

Return the final evaluation using the requested structured output.
""",
    input_variables=[
        "topic",
        "essay",
        "DOA_score",
        "DOA_summary",
        "COT_score",
        "COT_summary",
        "language_score",
        "language_summary"
    ]
)


def DOA(state:state)->dict:
     DOA_structured_llm = llm.with_structured_output(DOAResult)
     DOA_chain = DOA_prompt | DOA_structured_llm
     result = DOA_chain.invoke({"topic":state["topic"],"essay":state["essay"]})
     return {
         "DOA_summary":result.DOA_summary,
         "DOA_score":result.DOA_score
     }
    
def COT(state:state)->dict:
     COT_structured_llm = llm.with_structured_output(COTResult)
     COT_chain = COT_prompt | COT_structured_llm
     result = COT_chain.invoke({"topic":state["topic"],"essay":state["essay"]})
     return {
         "COT_summary":result.COT_summary,
         "COT_score":result.COT_score
     }
    
def language_Analysis(state:state)->dict:
     Language_structured_llm = llm.with_structured_output(LanguageResult)
     Language_chain = language_prompt | Language_structured_llm
     result = Language_chain.invoke({"topic":state["topic"],"essay":state["essay"]})
     return {
    "language_summary": result.language_summary,
    "language_score": result.language_score
}
     
     
     
def final_Analysis(state: state) -> dict:

    final_structured_llm = llm.with_structured_output(FinalResult)

    final_chain = Final_prompt | final_structured_llm

    result = final_chain.invoke({
        "topic": state["topic"],
        "essay": state["essay"],

        "DOA_summary": state["DOA_summary"],
        "DOA_score": state["DOA_score"],

        "COT_summary": state["COT_summary"],
        "COT_score": state["COT_score"],

        "language_summary": state["language_summary"],
        "language_score": state["language_score"]
    })

    return {
        "final_summary": result.final_summary,
        "final_score": result.final_score
    }
   