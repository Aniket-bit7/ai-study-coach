# rag/rag_pipeline.py

import os
from rag.embedder import ChromaEmbedder


class RAGPipeline:
    def __init__(self):
        self.embedder = ChromaEmbedder()

    # Load file
    def load_documents(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_path} not found")

        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        return text

    # Split into chunks
    def split_text(self, text):
        # Split by sections (double newline OR topic separation)
        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        return chunks

    # Run full pipeline
    def run(self, file_path="rag/documents/study_material.txt"):
        print("📥 Loading study material...")
        text = self.load_documents(file_path)

        print("✂️ Splitting into chunks...")
        chunks = self.split_text(text)

        print(f"📦 Total chunks: {len(chunks)}")

        print("🧠 Generating embeddings and storing in ChromaDB...")
        self.embedder.add_documents(chunks)

        print("✅ RAG pipeline completed!")