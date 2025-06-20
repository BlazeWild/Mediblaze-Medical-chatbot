from langchain_core.messages import HumanMessage, ToolMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import logging
from typing_extensions import Literal
from agent.utils.prompt import system_prompt
from agent.utils.tools import rag_tool, medical_web_search

load_dotenv()
# Configure logging
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# LLM Setup for MediBlaze
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    api_key=GOOGLE_API_KEY,
    temperature=0.3,  # Lower temperature for more consistent medical responses
    max_tokens=1200,  # Increased for comprehensive medical responses with formatting
)

# MediBlaze Medical Tools
tools = [
    rag_tool,  # Primary: Medical knowledge base retrieval
    medical_web_search,  # Secondary: Current medical web search for updated information
]
tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)

# Agent Nodes
def llm_call(state: MessagesState):
    """🧠 LLM processes the medical query and decides on tool usage."""
    return {
        "messages": [
            llm_with_tools.invoke(
                [SystemMessage(content=system_prompt)]
                + state["messages"]
            )
        ]
    }

def tool_node(state: dict):
    """🔧 Executes medical tools with comprehensive error handling."""
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        try:
            tool = tools_by_name[tool_call["name"]]
            observation = tool.invoke(tool_call["args"])
            result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
        except Exception as e:
            result.append(ToolMessage(content=f"⚠️ Tool error occurred. Providing response based on available knowledge.", tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: MessagesState) -> Literal["Action", "END"]:
    """
    🔄 Determines whether to continue with tool execution or provide final response.
    """
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls:
        return "Action"
    return "END"


# 🏗️ Build MediBlaze Agent Workflow
agent_builder = StateGraph(MessagesState)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("environment", tool_node)
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    {
        "Action": "environment",
        "END": END,
    },
)
agent_builder.add_edge("environment", "llm_call")

# 🚀 Compile the MediBlaze Agent
agent = agent_builder.compile()