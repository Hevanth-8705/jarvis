import os
import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorMemory:

    def __init__(self, index_path="vector.index", meta_path="vector_meta.pkl"):

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.index_path = index_path
        self.meta_path = meta_path

        self.dimension = 384

        if os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
            with open(meta_path, "rb") as f:
                self.metadata = pickle.load(f)
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            self.metadata = []

    # ==========================
    # ADD MEMORY
    # ==========================

    def add(self, text):

        embedding = self.model.encode([text])
        self.index.add(np.array(embedding, dtype=np.float32))
        self.metadata.append(text)

        self.save()

    # ==========================
    # SEARCH MEMORY
    # ==========================

    def search(self, query, top_k=3):

        if self.index.ntotal == 0:
            return []

        query_vec = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(query_vec, dtype=np.float32),
            top_k
        )

        results = []

        for idx in indices[0]:
            if idx < len(self.metadata):
                results.append(self.metadata[idx])

        return results

    # ==========================
    # SAVE
    # ==========================

    def save(self):

        faiss.write_index(self.index, self.index_path)

        with open(self.meta_path, "wb") as f:
            pickle.dump(self.metadata, f)