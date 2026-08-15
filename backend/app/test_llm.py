from .llm_service import generate_answer


question = "What is FastAPI?"

context = """
FastAPI is a Python web framework used to build APIs.
It provides automatic API documentation and uses Python
type hints for request validation.
"""


answer = generate_answer(
    question,
    context
)


print("Question:", question)
print("\nAI Answer:")
print(answer)