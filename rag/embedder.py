from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings


class ChromaEmbedder:
    def __init__(self):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")


        self.client = chromadb.Client(
            Settings(
                persist_directory="rag/vector_store",
                is_persistent=True
            )
        )


        self.collection = self.client.get_or_create_collection(
            name="study_material"
        )


    def embed(self, texts):
        return self.model.encode(texts).tolist()


    def add_documents(self, documents):
        """
        documents: list of strings
        """
        embeddings = self.embed(documents)

        ids = [f"doc_{i}" for i in range(len(documents))]

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids
        )


    def query(self, query_text, n_results=3):
        query_embedding = self.embed([query_text])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        return results["documents"][0]