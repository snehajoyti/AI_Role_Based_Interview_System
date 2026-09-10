from app.rag.retriever import retrieve_relevant_chunks 


ROLE_KNOWLEDGE_BASES = {
    "AI/ML Engineer": [
        {
            "index_path": r"vector_store\ai_ml\mitchell.index",
            "metadata_path": r"vector_store\ai_ml\mitchell_metadata.json",
            "source": "Machine Learning - Tom Mitchell"
        },
        {
            "index_path": r"vector_store\ai_ml\burkov.index",
            "metadata_path": r"vector_store\ai_ml\burkov_metadata.json",
            "source": "The Hundred-Page Machine Learning Book"
        },
        {
            "index_path": r"vector_store\ai_ml\absolute_beginners.index",
            "metadata_path": r"vector_store\ai_ml\absolute_beginners_metadata.json",
            "source": "Machine Learning for Absolute Beginners"
        },
        {
            "index_path": r"vector_store\advanced\ai_ml_dl.index",
            "metadata_path": r"vector_store\advanced\ai_ml_dl_metadata.json",
            "source": "Artifical Intelligence, Machine Learning and Deep Learning"
        },
        {
            "index_path": r"vector_store\advanced\bishop.index",
            "metadata_path": r"vector_store\advanced\bishop_metadata.json",
            "source": "Pattern Recognition and Machine Learning - Christopher Bishop"
        },
    ],

    "Data Scientist": [
        {
            "index_path": r"vector_store\data_science\intro_ml_python.index",
            "metadata_path": r"vector_store\data_science\intro_ml_python_metadata.json",
            "source": "Introduction to Machine Learning With Python"
        },
        {
            "index_path": r"vector_store\data_science\brownle.index",
            "metadata_path": r"vector_store\data_science\brownlee_metadata.json",
            "source": "Master Machine Learning Algorithms"
        },
        {
            "index_path": r"vector_store\ai_ml\mitchell.index",
            "metadata_path": r"vector_store\ai_ml\mitchell_metadata.json",
            "source": "Machine Learning - Tom Mitchell"
        },
        {
            "index_path": r"vector_store\advanced\bishop.index",
            "metadata_path": r"vector_store\advanced\bishop_metadata.json",
            "source": "Pattern Recognition and Machine Learning - Christopher Bishop"
        },
    ]
}


def retrieve_for_role(role: str, query: str, top_k_per_book: int = 2):
    knowledge_bases = ROLE_KNOWLEDGE_BASES.get(role)

    if not knowledge_bases:
        raise ValueError(f"Unsupported role: {role}")

    all_results = []

    for kb in knowledge_bases:
        results = retrieve_relevant_chunks(
            query=query,
            index_path=kb["index_path"],
            metadata_path=kb["metadata_path"],
            top_k=top_k_per_book 
        )

        for result in results:
            result["source"] = kb['source']
            all_results.append(result)

    all_results.sort(key=lambda item: item["distance"])

    return all_results 
