
from langgraph_fundamentals.loop_workflow.state import State , GenerateTweet , EvaluateTweet
from langchain_core.prompts import PromptTemplate
from Models.openAI_llm import llm
tweet_generate_prompt = PromptTemplate(
    template="""
You are a social media content creator.

Generate a short, engaging, and natural-sounding tweet about the following topic:

Topic: {topic}

Requirements:
- Write only the tweet.
- Do not include explanations, labels, quotes, or prefixes.
- Keep it under 280 characters.
- Make it interesting and easy to read.
- Use a conversational tone.
- You may use 1-2 relevant emojis if appropriate.
- Do not add hashtags unless they naturally fit the tweet.

Return only the final tweet.
""",
    input_variables=["topic"]
)



evaluation_prompt = PromptTemplate(
    template="""
You are an expert social media content evaluator.

Evaluate the following tweet based on the given topic.

Topic:
{topic}

Tweet:
{tweet}

Evaluate the tweet using these criteria:
1. Relevance — Does the tweet clearly relate to the given topic?
2. Quality — Is it interesting, clear, and engaging?
3. Conciseness — Is it suitable for a tweet and under 280 characters?
4. Naturalness — Does it sound like a human-written tweet rather than AI-generated text?
5. Completeness — Does it communicate a meaningful idea rather than being vague or generic?

Decision:
- Return "approved" if the tweet satisfies the criteria and is good enough to publish.
- Return "needs_improvement" if the tweet is irrelevant, unclear, overly generic, poorly written, or otherwise needs revision.

Do not rewrite the tweet.
Do not provide any additional output.
Return only the structured evaluation.
""",
    input_variables=["topic", "tweet"]
)

optimize_prompt_tweet = PromptTemplate(
    template="""
You are an expert social media writer.

Improve the following tweet while keeping it relevant to the given topic.

Topic:
{topic}

Original Tweet:
{tweet}

Requirements:
- Rewrite the tweet to make it more engaging, clear, and natural.
- Keep the core idea relevant to the topic.
- Fix any issues with clarity, grammar, wording, or flow.
- Avoid generic or meaningless statements.
- Make the tweet concise and impactful.
- Keep it within 280 characters.
- Use a conversational and human-like tone.
- You may use relevant emojis if they improve the tweet.
- Do not add unnecessary hashtags.
- Do not explain what you changed.
- Do not include labels such as "Improved Tweet:".
- Return ONLY the improved tweet.

Improved Tweet:
""",
    input_variables=["topic", "tweet"]
)


def generate_tweet(state:State)->dict:
    structureLLM = llm.with_structured_output(GenerateTweet)  
    generate_tweet_chain = tweet_generate_prompt | structureLLM
    result = generate_tweet_chain.invoke({
        "topic":state["topic"]
    })  
    
    return {
        "tweet": result.tweet
    }


def evaluate_tweet(state:State)->str:
    if state["max_iteration"]<state["iteration"] :
        return "over_iterated"
    llm_structured = llm.with_structured_output(EvaluateTweet)
    evaluate_chain = evaluation_prompt | llm_structured
    result = evaluate_chain.invoke({"topic":state["topic"],"tweet":state["tweet"]})
    return result.evaluation

def optimize_tweet(state:State)->dict:
    structured_llm = llm.with_structured_output(GenerateTweet)
    optimize_tweet_chain = optimize_prompt_tweet | structured_llm
    result = optimize_tweet_chain.invoke({"topic":state["topic"],"tweet":state["tweet"]})
    return {
        "tweet":result.tweet,
        "iteration":state["iteration"]+1
    }
    