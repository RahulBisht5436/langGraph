# Import the state definition used by our LangGraph.
#
# BMIState defines the structure of the data that flows
# between different nodes in the graph.
from langgraph_fundamentals.Introduction.state import BMIState


# Import the LLM that will be used to generate
# personalized BMI suggestions.
from Models.openAI_llm import llm


# Import StrOutputParser to convert the LLM response
# into a simple string.
from langchain_core.output_parsers import StrOutputParser


# Import PromptTemplate to create a reusable prompt
# with dynamic input variables.
from langchain_core.prompts import PromptTemplate


# =========================================================
# 1. CREATE THE BMI SUGGESTION PROMPT
# =========================================================

# PromptTemplate allows us to dynamically insert the
# calculated BMI into the prompt using {BMI}.
#
# The LLM will analyze the BMI and provide suggestions
# depending on whether the BMI is low or high.
getSuggestionprompt = PromptTemplate(
    template="""
    For the given BMI: {BMI},

    Provide tips to achieve a healthy BMI.

    CASE 1:
    If the BMI is low, provide tips for increasing it.

    CASE 2:
    If the BMI is high, provide tips for decreasing it.

    Provide the suggestions in a clear and simple format.
    """,
    
    # Define the variables that will be passed
    # to the prompt at runtime.
    input_variables=["BMI"]
)


# =========================================================
# 2. CREATE THE OUTPUT PARSER
# =========================================================

# StrOutputParser converts the LLM response into
# a normal Python string.
#
# Without this parser, the result may be an
# AIMessage object instead of a plain string.
getSuggestionParser = StrOutputParser()


# =========================================================
# 3. CALCULATE BMI NODE
# =========================================================

# This function acts as a LangGraph node.
#
# It receives the current graph state and calculates BMI
# using the standard BMI formula:
#
# BMI = weight / height²
#
# The calculated BMI is then added to the state.
def calculate_BMI(state: BMIState) -> BMIState:

    return {
        # Preserve all existing values in the state.
        **state,

        # Calculate BMI using weight and height.
        "BMI": state["weight"] / (state["height"] * state["height"])
    }


# =========================================================
# 4. BMI SUGGESTION NODE
# =========================================================

# This function acts as the second LangGraph node.
#
# It receives the state after calculate_BMI() has executed.
#
# The calculated BMI is passed to the LLM prompt,
# and the LLM generates suggestions based on the BMI.
def getSuggestionBMI(state: BMIState) -> BMIState:

    # Create an LCEL chain:
    #
    # PromptTemplate
    #       ↓
    #      LLM
    #       ↓
    # StrOutputParser
    #
    # The prompt generates the input,
    # the LLM generates the response,
    # and the parser converts the response into a string.
    getSuggestionChain = (
        getSuggestionprompt
        | llm
        | getSuggestionParser
    )


    # Execute the chain and pass the calculated BMI
    # as the input to the prompt.
    result = getSuggestionChain.invoke({
        "BMI": state["BMI"]
    })


    # Return the updated state.
    #
    # The existing state is preserved using **state,
    # and the generated suggestion is added as
    # BMI_suggestion.
    return {
        **state,
        "BMI_suggestion": result
    }