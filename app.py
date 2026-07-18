import asyncio
import json
import streamlit as st
import ollama

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


FIRST_MODEL = "qwen2.5:1.5b"
SERVER_SCRIPT = "server.py"
MAX_TOOL_ROUNDS = 5


def mcp_tools_to_ollama_format(mcp_tools):
    converted = []

    for t in mcp_tools:
        converted.append(
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description or "",
                    "parameters": t.inputSchema,
                },
            }
        )

    return converted


async def get_ai_response(user_input):

    server_params = StdioServerParameters(
        command="python3",
        args=[SERVER_SCRIPT],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()

            tools_result = await session.list_tools()
            ollama_tools = mcp_tools_to_ollama_format(
                tools_result.tools
            )

            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant. "
                        "You have access to a tool called "
                        "ask_second_ai which lets you consult "
                        "a second independent AI model. "
                        "Use it whenever needed and combine "
                        "both answers."
                    ),
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ]

            tool_logs = []

            for _ in range(MAX_TOOL_ROUNDS):

                response = ollama.chat(
                    model=FIRST_MODEL,
                    messages=messages,
                    tools=ollama_tools,
                )

                msg = response["message"]
                messages.append(msg)

                tool_calls = msg.get("tool_calls")

                # Final response
                if not tool_calls:
                    return (
                        msg.get("content", "").strip(),
                        tool_logs,
                    )

                # Tool usage
                for call in tool_calls:

                    name = call["function"]["name"]
                    args = call["function"]["arguments"]

                    if isinstance(args, str):
                        args = json.loads(args)

                    question = args.get("question", str(args))

                    tool_logs.append(
                        f"Model 1 asked Model 2:\n{question}"
                    )

                    result = await session.call_tool(
                        name,
                        args,
                    )

                    result_text = "\n".join(
                        block.text
                        for block in result.content
                        if hasattr(block, "text")
                    )

                    tool_logs.append(
                        f"Model 2 replied:\n{result_text}"
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "content": result_text,
                        }
                    )

            return (
                "Too many tool calls.",
                tool_logs,
            )


# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(
    page_title="Two AI Chatbot",
    page_icon="🤖",
)

st.title("Two AI Chatbot")
st.write(
    "Model 1 (Qwen) can privately consult "
    "Model 2 (Llama) whenever required."
)

prompt = st.text_input(
    "Ask anything:"
)

if st.button("Ask AI"):

    if prompt.strip():

        with st.spinner("Thinking..."):

            answer, logs = asyncio.run(
                get_ai_response(prompt)
            )

        st.subheader("Answer")
        st.write(answer)

        if logs:
            with st.expander(
                "View AI Collaboration"
            ):
                for item in logs:
                    st.write(item)
                    st.write("---")
