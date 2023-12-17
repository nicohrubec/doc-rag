def build_prompt_with_context(prompt, contexts):
    context = "\n\n".join(contexts)

    return f"""
Context information: "{context}".
Given the context information and not prior knowledge, answer the query.
Query: {prompt}
Answer: \
"""

