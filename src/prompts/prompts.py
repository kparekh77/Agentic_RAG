from langchain_core.messages import SystemMessage, HumanMessage


def haiku_about(topic: str) -> str:
    """
    Returns user‐facing prompt asking for a haiku about `topic`.
    """
    return (
        f"Write a classic 5-7-5 syllable haiku about {topic},\n"
        "evoking both wonder and simplicity."
    )


def briefing_prompt(topic: str, snippets: list[str]) -> str:
    context = "\n".join(f"- {s}" for s in snippets)
    return (
        f"Give me the official documentation links for how to use '{topic}':\n"
        f"{context}\n\n"
    )


def make_system_message(package: str) -> SystemMessage:
    return SystemMessage(
        content=(
            "You are an expert Python instructor. "
            "When you need documentation context, call the retrieve_context tool with the package name. "
            "Once you have the docs, write a clear tutorial on how to use the package, "
            "including FIVE distinct, runnable code examples demonstrating key features."
        )
    )


def make_user_message(package: str) -> HumanMessage:
    return HumanMessage(
        content=(
            f"I’d like a step-by-step tutorial on using the `{package}` package in Python. "
            "Please include five code examples that I can run."
        )
    )
