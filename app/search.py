from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def search_chunks(chunks: list[str], query: str, top_k: int = 1) -> list[str]:
    if not chunks:
        return []

    documents = chunks + [query]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    chunk_vectors = tfidf_matrix[:-1]
    query_vector = tfidf_matrix[-1]

    similarities = cosine_similarity(query_vector, chunk_vectors).flatten()
    ranked_indices = similarities.argsort()[::-1][:top_k]

    return [chunks[i] for i in ranked_indices]
