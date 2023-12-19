def build_prompt_with_context(prompt, contexts):
    context = "\n\n".join(contexts)

    return f"""
Context information: "{context}".
Given the context information and not prior knowledge, answer the query.
Query: {prompt}
Answer: \
"""


def build_system_prompt_for_tool(tool):
    tool_str = ''

    if tool == 'archicad':
        tool_str = 'ArchiCAD'
    elif tool == 'rfem':
        tool_str = 'RFEM'

    return f"You are a helpful assistant, skilled in explaining complex {tool_str} problems in simple terms."

