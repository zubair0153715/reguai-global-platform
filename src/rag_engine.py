import os
import chromadb

class RegulatoryRAGEngine:
    """Vector database RAG engine to store and semantically search PDF guidelines."""

    def __init__(self, db_path: str = "database/chroma_db"):
        os.makedirs(db_path, exist_ok=True)
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name="pdf_regulatory_guidelines")

    def seed_baseline_knowledge(self):
        """Seeds official ICH, FDA, and DRAP guideline citations into vector DB."""
        if self.collection.count() == 0:
            docs = [
                "US FDA 21 CFR 312.23: Investigational New Drug Application (IND) must contain Module 1 Administrative Information and Module 2 Summaries.",
                "ICH Q1A(R2) Stability Testing: Long-term testing at 25°C ± 2°C/60% RH ± 5% RH for Zone I/II, and 30°C ± 2°C/75% RH ± 5% RH for Zone IVb.",
                "DRAP SRO 436(I)/2017: Drug registration applications require Form 5 submission along with cGMP verification from the Drug Licensing Board.",
                "SFDA eCTD Module 1.2: Cover letter must be signed by the Authorized Local Representative in Saudi Arabia along with 3DTron Track & Trace GTIN barcodes.",
                "EU EMA SmPC Guidelines: Section 4.3 Contraindications must explicitly list hypersensitivity to active substances or any excipients.",
                "MOHAP UAE Resolution 321: All medicinal packaging imported into the UAE must feature bilingual labeling in both Arabic and English."
            ]
            metadatas = [
                {"authority": "US_FDA", "source": "21 CFR 312.23"},
                {"authority": "ICH_GLOBAL", "source": "ICH Q1A(R2)"},
                {"authority": "PK_DRAP", "source": "SRO 436(I)/2017"},
                {"authority": "SA_SFDA", "source": "SFDA eCTD v3.2"},
                {"authority": "EU_EMA", "source": "EMA SmPC Guideline"},
                {"authority": "UAE_MOHAP", "source": "MOHAP Res 321"}
            ]
            ids = [f"guideline_{i}" for i in range(len(docs))]
            self.collection.add(documents=docs, metadatas=metadatas, ids=ids)

    def query_context(self, text_snippet: str, n_results: int = 2) -> list:
        try:
            results = self.collection.query(query_texts=[text_snippet], n_results=n_results)
            return results.get("documents", [[]])[0]
        except Exception:
            return []