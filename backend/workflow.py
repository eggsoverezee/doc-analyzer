
from typing import TypedDict, Dict, Any
from typing_extensions import NotRequired

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from .config import MODEL_NAME

class DocState(TypedDict):
    content: str
    summary: NotRequired[str]
    metadata: NotRequired[Dict[str, Any]]


llm = ChatOpenAI(model=MODEL_NAME, temperature=0.2)


def summarize_text(state: DocState) -> DocState:
    content = state["content"]

    prompt = [
        ("system", "You summarize documents."),
        ("user", f"Summarize this in 3–5 bullet points:\n\n{content}"),
    ]

    response = llm.invoke(prompt)
    summary = response.content

    return {**state, "summary": summary}


def generate_metadata(state: DocState) -> DocState:
    content = state["content"]

    prompt = [
        ("system", "You generate metadata for documents."),
        ("user", f"Analyze this and return metadata:\n\n{content}"),
    ]

    response = llm.invoke(prompt)

    metadata: Dict[str, Any] = {
        "raw_metadata_response": response.content,
        "length_chars": len(content),
    }

    return {**state, "metadata": metadata}


def build_graph():
    workflow = StateGraph(DocState)

    workflow.add_node("summarize", summarize_text)
    workflow.add_node("metadata", generate_metadata)

    workflow.set_entry_point("summarize")
    workflow.add_edge("summarize", "metadata")
    workflow.add_edge("metadata", END)

    return workflow.compile()


graph = build_graph()
