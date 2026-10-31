# RAG ↔ Backend Integration Contract

**Owner:** AI / RAG developer  
**Public function:** `rag.rag_pipeline.answer_question`

## Function

```python
answer_question(question: str, top_k: int = 5) -> dict
```

## Input

- `question`: non-empty text provided by the user.
- `top_k`: maximum number of knowledge chunks to retrieve (default 5).

## Output

```json
{
  "answer": "Grounded text response",
  "sources": [
    {
      "source": "relative/file/name.json",
      "place": "Destination or place, if available",
      "category": "Category, if available",
      "reference": "Citation name or URL, if provided in the data",
      "similarity": 0.83,
      "excerpt": "Retrieved passage excerpt"
    }
  ]
}
```

## Responsibilities

- RAG module: data loading, preprocessing, embeddings, vector search, prompt construction, LLM response, source details.
- Backend module: HTTP route, request validation, authentication, rate limiting, conversation/user state, frontend response handling, deployment.

## Shared requirements

The RAG developer will notify the backend developer before changing the function name, input parameters, output keys, Python dependencies, or package location. The backend developer should not import internal RAG modules individually; use the public `answer_question` interface unless the team agrees otherwise.
