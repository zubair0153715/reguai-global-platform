import os
import chromadb

class RegulatoryRAGEngine:
    """Vector database RAG engine to store and query regulatory guidelines semantically."""

    def __init__(self, db_path: str = "database/chroma_db"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="regulatory_guidelines")

    def seed_baseline_knowledge(self):
        """Seeds initial vector store with global compliance knowledge."""
        if self.collection.count() == 0:
            docs = [
                "US FDA 21 CFR 312 mandates IND Protocol submission prior to clinical studies.",
                "DRAP SRO guidelines specify Zone IVb stability testing (40C / 75% RH) for Pakistan.",
                "SFDA requires 3DTron Track and Trace barcode integration on packaging.",
                "EMA Annex 1 requires strict environmental monitoring for sterile medicinal products."
            ]
            ids = [f"rule_{i}" for i in range(len(docs))]
            self.collection.add(documents=docs, ids=ids)

    def query_context(self, text_snippet: str, n_results: int = 2) -> list:
        results = self.collection.query(query_texts=[text_snippet], n_results=n_results)
        return results.get("documents", [[]])[0]