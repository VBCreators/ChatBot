# FOLDER_STRUCTURE.md — Where every RAG file lives

> Your existing project structure is preserved. RAG-specific files are added
> inside it, not as a parallel course folder. After all 12 modules, your tree
> will look like this:

```
your-project/
│
├── GUI.py                          # Streamlit UI (existing — we add tabs/pages)
├── config.py                       # Settings (existing — we add RAG env vars)
├── .env                            # Secrets (existing)
├── .env.example                    # NEW — template for collaborators
├── .gitignore                      # (existing)
├── .dockerignore                   # (existing)
├── requirements.txt                # UPDATED — RAG deps
├── Dockerfile                      # UPDATED — pgvector in compose
├── docker-compose.yml              # NEW — Postgres + pgvector + app
│
├── data/                           # NEW — your source documents
│   ├── raw/                        #   originals (PDFs, etc.)
│   └── evaluation/                 #   eval datasets
│
├── brain/                          # (existing folder)
│   ├── engine.py                   #   LLM via LangChain (existing — unchanged)
│   └── rag/                        # NEW — all RAG logic lives here
│       ├── __init__.py
│       ├── config.py               #   RAG-specific config (chunk sizes, k, etc.)
│       ├── loaders.py              #   Module 2: PDF, web, CSV, MD loaders
│       ├── splitters.py            #   Module 2: chunking strategies
│       ├── embeddings.py           #   Module 3: embedding model factory
│       ├── vectorstore.py          #   Module 4: FAISS + pgvector
│       ├── retriever.py            #   Modules 5-6: similarity/MMR/hybrid/re-rank
│       ├── prompts.py              #   All prompt templates (single source of truth)
│       ├── chains.py               #   LCEL chains: basic RAG, conversational, etc.
│       └── observability.py        #   Module 9: callbacks, logging, tracing
│
├── services/                       # (existing folder)
│   ├── GUIstreaming.py             #   (existing)
│   ├── chatservices/
│   │   └── chat_session_mgmt.py    #   (existing — extended in Module 7)
│   └── dbservices/                 # UPDATED
│       ├── db_session.py           #   (existing)
│       ├── db_crud.py              #   (existing)
│       ├── db_create_tables.py     #   UPDATED — adds RAG tables
│       ├── db_table_details.py     #   UPDATED — adds RAG table schemas
│       ├── rag_crud.py             #   NEW — CRUD for documents/chunks/chat_history
│       └── tables/                 # NEW — split table definitions into modules
│           ├── __init__.py
│           ├── user_tables.py      #   (moved from db_table_details.py)
│           └── rag_tables.py       #   NEW — documents, chunks, chat_history, etc.
│
└── logs/                           # NEW — structured logs
    └── rag/
```

## What goes where — the rules

| Concern | Folder | Reason |
|---|---|---|
| LLM/embeddings/retrieval **logic** | `brain/rag/` | "The brain thinks" — pure Python, no I/O |
| **Data access** (CRUD on tables) | `services/dbservices/` | Service layer pattern (clean separation) |
| **UI** (Streamlit) | `GUI.py` + `services/chatservices/` | Presentation only |
| **Config** (env, paths, model names) | `config.py` + `brain/rag/config.py` | One place to change behavior |
| **Documents** (PDFs, etc.) | `data/raw/` | Never in code — mounted in Docker |
| **Eval data** | `data/evaluation/` | Reproducible benchmarks |

## DB tables we'll add (Module 1 + Module 4)

- `rag_documents` — uploaded file metadata (filename, user_id, uploaded_at, etc.)
- `rag_chunks` — chunked text + embedding + reference to document
- `rag_chat_sessions` — chat session metadata
- `rag_chat_messages` — full conversation history (per session)

The exact schemas are in `services/dbservices/tables/rag_tables.py` once we build them.

## Why this layout?

1. **Brain doesn't import services.** The RAG logic stays pure-Python and unit-testable.
2. **Services don't import brain.** The DB layer is dumb CRUD; it doesn't know what an LLM is.
3. **GUI imports both.** It's the only thing that wires everything together.
4. **Swap one tool, change one file.** As you saw in `TOOLS.md`, every abstraction lives in a single file under `brain/rag/`.
