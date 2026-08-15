from chunking_service import chunk_code


sample_code = """
def hello():
    print("Hello GenCodeX!")


def add(a, b):
    return a + b


def multiply(a, b):
    return a * b
"""


chunks = chunk_code(
    sample_code,
    chunk_size=100,
    overlap=20
)


print("Number of chunks:", len(chunks))

for index, chunk in enumerate(chunks, start=1):
    print("\n--- Chunk", index, "---")
    print(chunk)