# Yatranook — AI / RAG Pipeline

This folder is a standalone RAG module for the Yatranook project. It is intended to be developed on the `feature/rag-pipeline` Git branch. It does **not** create a second backend or a second web application.

## What it does

1. Reads tourism knowledge from TXT, Markdown, JSON, and text-based PDF files.
2. Cleans the text and divides it into overlapping chunks.
3. Creates local text embeddings with Sentence Transformers.
4. Stores the chunks and vectors in a persistent Chroma database.
5. Retrieves relevant chunks for a question.
6. Sends the retrieved context to Gemini to draft a grounded answer.
7. Returns the answer together with source details for the backend/chatbot to display.

The starter JSON file contains a few sample entries only. They are starter content, not a complete or officially verified tourism database. Add reliable, current sources before presenting visitor information to users.

## 0. Agree the integration point with your backend teammate

Before coding in the shared repository, agree that the RAG module will live in a top-level `rag/` folder (or use the location agreed by the team). The backend teammate should call this public function:

```python
from rag.rag_pipeline import answer_question

result = answer_question("What can I visit in Puri?")
# result = {"answer": "...", "sources": [{...}, ...]}
```

The backend developer owns the API route, authentication, frontend communication, and deployment. You own the RAG package and its data-ingestion/retrieval logic. Coordinate changes to shared files such as `requirements.txt` and `.gitignore`.

## 1. Create your branch and get the project

If the repository owner has already created the GitHub repository, clone it once:

```bash
git clone https://github.com/OWNER/REPOSITORY.git
cd REPOSITORY
```

Replace `OWNER/REPOSITORY` with the real GitHub path. Then create your work branch:

```bash
git checkout main
git pull origin main
git checkout -b feature/rag-pipeline
```

Put this `rag/` folder, `cli.py`, and the relevant dependency/configuration entries at the agreed location in the shared repository. Do not create a second `backend/` folder if another teammate owns backend development. If the repository already has a root `requirements.txt`, merge the required package lines into it instead of replacing it.

## 2. Install Python and create a virtual environment

Use Python 3.11 or 3.12. From the project root, open the VS Code terminal.

**Windows PowerShell:**

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks activation, use Command Prompt instead:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS/Linux:**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

The first embedding run downloads the selected Sentence Transformers model. The download can take time and requires an internet connection. Later runs use the local model cache.

## 3. Configure the Gemini API key

Copy `.env.example` to `.env` in the project root. In Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace `your_api_key_here` with your own Gemini API key. Do not share the key and do not commit `.env`. Keep `.env.example` in Git, but never put the actual key in it.

The default generation model is `gemini-flash-latest`; you can change `GEMINI_MODEL` in `.env` if your Google AI Studio account supports a different model name.

## 4. Add tourism knowledge

Add trusted material under:

```text
rag/data/raw/
```

Supported file types:

- `.json`: a list of records or an object containing `documents`, `items`, `places`, `destinations`, or `records`.
- `.txt` and `.md`: plain text/Markdown.
- `.pdf`: text-based PDFs. Scanned/image-only PDFs need a separate OCR preparation step and will not produce useful text through this loader.

Example JSON record:

```json
{
  "place": "Konark Sun Temple",
  "destination": "Konark",
  "district": "Puri",
  "category": "Heritage",
  "content": "Write a sourced, checked description of the destination here.",
  "source": "Official source name and URL"
}
```

Use facts from reliable sources such as official tourism authorities, site/temple authorities, government departments, and recognised heritage organisations. Keep the source name or URL in each record. Check opening hours, fees, access restrictions, transport, and safety details before publishing because these may change. The sample JSON file is only to demonstrate the format.

## 5. Build the vector database (ingestion)

Run this command from the project root:

```bash
python cli.py ingest
```

The script loads supported files from `rag/data/raw/`, cleans/chunks them, generates embeddings, and writes them to `rag/chroma_db/`. It prints how many chunks were indexed from each source file.

When you update a data file, run `python cli.py ingest` again. The current implementation replaces the stored chunks belonging to each source file before inserting the new chunks. It does not automatically delete a source that you have removed from the raw folder; remove such records from Chroma deliberately if you delete a data file.

## 6. Test retrieval without the LLM

This checks whether the vector database finds relevant knowledge. It does not use a Gemini API key:

```bash
python cli.py search "What can visitors see in Puri?"
python cli.py search "Tell me about the Sun Temple at Konark" --top-k 3
```

Look at the returned source, text, and similarity. Similarity is a ranking signal, not a guaranteed probability of correctness. Try many questions and confirm that the retrieved chunks actually answer them. If results are poor, improve the source documents, chunk size, or embedding model before blaming the generator.

## 7. Ask the complete RAG pipeline

After setting `GEMINI_API_KEY` in `.env` and ingesting data:

```bash
python cli.py ask "What is the Konark Sun Temple?"
python cli.py ask "Suggest heritage places near Bhubaneswar" --top-k 5
```

The output is JSON with:

- `answer`: answer produced using the retrieved context.
- `sources`: the retrieved source filename, place/category when available, similarity score, and excerpt.

If the retriever returns no records, the module responds that the knowledge base does not contain enough information. The prompt also tells Gemini not to invent facts. This is a guardrail, not a guarantee; review answers and sources during testing.

## 8. Run automated tests

From the project root:

```bash
python -m pytest -q
```

These tests cover document loading and text chunking. They do not test live Gemini generation or prove tourism facts are accurate.

## 9. Integration with the backend teammate

The backend teammate can call the RAG function from their existing service/API code:

```python
from rag.rag_pipeline import answer_question


def chatbot_service(user_message: str) -> dict:
    return answer_question(user_message, top_k=5)
```

A possible API response shape is:

```json
{
  "answer": "...",
  "sources": [
    {
      "source": "odisha_tourism.json",
      "place": "Puri Beach",
      "category": "Beach",
      "reference": "Source citation or URL, if supplied in the JSON record",
      "similarity": 0.72,
      "excerpt": "..."
    }
  ]
}
```

This module is synchronous. If the backend uses an async framework, the backend teammate can call it from a worker thread or adapt it to an async service. Do not add a second FastAPI app just for this module unless the team has explicitly chosen a separate RAG service.

## 10. Commit and push your branch

Check what changed:

```bash
git status
```

Add only the RAG source files, data files that the team has approved for Git, and dependency updates. Do **not** commit `.env`, `.venv/`, or `rag/chroma_db/`.

```bash
git add rag cli.py tests requirements.txt .gitignore README.md
git commit -m "Build Odisha tourism RAG pipeline"
git push -u origin feature/rag-pipeline
```

Then open a Pull Request on GitHub. Describe the ingestion format, embedding model, vector database, test commands, and backend integration function. Ask the backend teammate to review the function contract before merging.

## Suggested completion checklist

- [ ] Team agreed the RAG folder location and integration function.
- [ ] Python environment and dependencies installed.
- [ ] Gemini key stored only in local `.env`.
- [ ] Reliable tourism source material collected and checked.
- [ ] Ingestion successfully indexes documents.
- [ ] Retrieval returns useful source passages for test questions.
- [ ] Gemini answers are grounded in retrieved passages.
- [ ] Sources are returned to the chatbot/backend.
- [ ] Tests pass and limitations are documented.
- [ ] Pull Request created from `feature/rag-pipeline`.
