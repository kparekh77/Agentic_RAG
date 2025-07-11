import sys
import logging
from typing import Literal

from langchain_openai.chat_models import ChatOpenAI
from langgraph.graph import MessagesState, END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver

from src.clients.context_retriever import retrieve_context
from src.config.config import MODEL_NAME
from src.prompts.prompts import make_system_message, make_user_message

# ─── Enable INFO logs from our retriever ───────────────────────────────
logging.basicConfig(level=logging.INFO)

# 1) Register your retrieval tool
tools = [retrieve_context]
tool_node = ToolNode(tools)

# 2) Bind the LLM to your tool
model = ChatOpenAI(model=MODEL_NAME, temperature=0.2).bind_tools(tools)


# 3) Control flow: loop back to tools if a tool call was made
def should_continue(state: MessagesState) -> Literal["tools", END]:
    last = state["messages"][-1]
    return "tools" if last.tool_calls else END


# 4) Wrap the LLM invocation
def call_model(state: MessagesState):
    resp = model.invoke(state["messages"])
    return {"messages": [resp]}


# 5) Assemble the LangGraph workflow
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

app = workflow.compile(checkpointer=MemorySaver())


# 6) CLI entrypoint
def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main <package_name>")
        sys.exit(1)

    package = sys.argv[1]
    sys_msg = make_system_message(package)
    user_msg = make_user_message(package)

    final_state = app.invoke(
        {"messages": [sys_msg, user_msg]},
        config={"configurable": {"thread_id": package}}
    )

    # The tutorial will include our [DOCS_FETCH:*] flag in its context,
    # or you can just watch the console for INFO/WARNING logs.
    print(final_state["messages"][-1].content)


if __name__ == "__main__":
    main()
