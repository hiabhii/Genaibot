import os
from dotenv import load_dotenv

# =========================
# Load Environment Variables
# =========================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

# =========================
# Imports
# =========================
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage


# =========================
# Agent Function (Groq Only)
# =========================
def get_response_from_ai_agent(
    llm_id: str,
    query: str,
    allow_search: bool
):

    # Use Groq LLM
    llm = ChatGroq(
        model=llm_id,
        api_key=GROQ_API_KEY
    )

    # Add search tool if enabled
    tools = []
    if allow_search:
        tools.append(
            TavilySearch(
                tavily_api_key=TAVILY_API_KEY,
                max_results=2
            )
        )

    # Create agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="Act as a smart, friendly, helpful AI assistant."
    )

    # Invoke agent
    response = agent.invoke(
        {"messages": [HumanMessage(content=query)]}
    )

    return response["messages"][-1].content


# =========================
# Test Run
# =========================
if __name__ == "__main__":

    answer = get_response_from_ai_agent(
        llm_id="llama-3.3-70b-versatile",  # Groq model
        query="Who is the current Prime Minister of India?",
        allow_search=True
    )

    print("\nAI Response:\n")
    print(answer)