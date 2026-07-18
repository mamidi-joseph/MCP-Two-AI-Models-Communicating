#!/usr/bin/env python3
"""
MCP SERVER -- the "bridge" between two AI models.

This server exposes ONE tool: ask_second_ai(question).

When the FIRST AI model (Qwen2.5, the one you talk to) decides it wants
a second opinion, it calls this tool. This file then quietly asks the
SECOND AI model (Llama 3.2, a different open-source model) the question,
and hands the answer back.

Both models run on your machine via Ollama. Nothing here uses the
internet or any paid service.
"""

import ollama
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("two-ai-bridge")

# The second, independent AI model. Different from the first model that
# talks to the user -- this is what makes it "two AIs talking".
SECOND_MODEL = "llama3.2:1b"


@mcp.tool()
def ask_second_ai(question: str) -> str:
    """Ask a second, independent open-source AI model (Llama 3.2) for its
    answer or opinion on a question. Use this to get a second perspective,
    double-check an answer, or delegate a sub-question."""
    try:
        response = ollama.chat(
            model=SECOND_MODEL,
            messages=[{"role": "user", "content": question}],
        )
        return response["message"]["content"].strip()
    except Exception as e:
        return (
            f"Could not reach the second AI model ({SECOND_MODEL}). "
            f"Make sure you ran 'ollama pull {SECOND_MODEL}' and that "
            f"Ollama is running. Error: {e}"
        )


if __name__ == "__main__":
    mcp.run(transport="stdio")
