from rag.embedder import ChromaEmbedder

embedder = ChromaEmbedder()

# Add documents
docs = [
    "Arrays are data structures used to store elements.",
    "Binary search works on sorted arrays.",
    "Time complexity of binary search is O(log n)."
]

embedder.add_documents(docs)

# Query
results = embedder.query("What is binary search?")

print(results)