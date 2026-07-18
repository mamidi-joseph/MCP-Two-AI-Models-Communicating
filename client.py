#!/usr/bin/env python3
"""
CHAT CLIENT -- this is the program you actually run and type into.

It starts the FIRST AI model (Qwen2.5), which you chat with directly.
That model has one tool available: ask_second_ai. Whenever it decides
to use that tool, it is really talking to the SECOND AI model (Llama 3.2)
through the MCP server (server.py), and using that answer to help reply
to you.

This is two independent open-source AI models communicating with each
other through MCP, running entirely on your machine.
"""

import asyncio
import json

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

FIRST_MODEL = "qwen2.5:1.5b"     # the model you talk to directly
SERVER_SCRIPT = "server.py"       # starts automatically, bridges to the 2nd model
MAX_TOOL_ROUNDS = 5


def mcp_tools_to_ollama_format(mcp_tools):
    converted = []
    for t in mcp_tools:
        converted.append({
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description or "",
                "parameters": t.inputSchema,
            },
        })
    return converted


async def chat_loop():
    server_params = StdioServerParameters(command="python3", args=[SERVER_SCRIPT])

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()
            ollama_tools = mcp_tools_to_ollama_format(tools_result.tools)

            print("=" * 60)
            print("Two AI models are now connected.")
            print("You are talking to Model 1 (Qwen2.5).")
            print("It can privately consult Model 2 (Llama 3.2) when useful.")
            print("Type 'quit' to exit.")
            print("=" * 60 + "\n")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. You have access to a tool "
                        "called ask_second_ai, which lets you consult a second, "
                        "independent AI model for a second opinion. Use it when "
                        "a second perspective would improve your answer, then "
                        "combine both views into your final reply to the user."
                    ),
                }
            ]

            while True:
                user_input = input("You: ").strip()
                if user_input.lower() in ("quit", "exit"):
                    break
                if not user_input:
                    continue

                messages.append({"role": "user", "content": user_input})

                for _ in range(MAX_TOOL_ROUNDS):
                    response = ollama.chat(
                        model=FIRST_MODEL,
                        messages=messages,
                        tools=ollama_tools,
                    )
                    msg = response["message"]
                    messages.append(msg)

                    tool_calls = msg.get("tool_calls")
                    if not tool_calls:
                        print(f"\nModel 1 (final answer): {msg.get('content', '').strip()}\n")
                        break

                    for call in tool_calls:
                        name = call["function"]["name"]
                        args = call["function"]["arguments"]
                        if isinstance(args, str):
                            args = json.loads(args)

                        print(f"  [Model 1 is asking Model 2]: {args.get('question', args)}")
                        result = await session.call_tool(name, args)
                        result_text = "\n".join(
                            block.text for block in result.content if hasattr(block, "text")
                        )
                        print(f"  [Model 2 replied]: {result_text}\n")

                        messages.append({
                            "role": "tool",
                            "content": result_text,
                        })
                else:
                    print("Model 1: (stopped after too many tool calls)\n")


if __name__ == "__main__":
    asyncio.run(chat_loop())
