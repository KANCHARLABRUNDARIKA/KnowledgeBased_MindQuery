# RAG System - User Flow Visualization

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    RAG SYSTEM USER FLOW                      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┐
│   1. USER       │
│   UPLOADS       │
│   DOCUMENT      │
│                 │
│  📄 PDF         │
│  📄 DOCX        │
│  📄 TXT         │
│  📄 MD          │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   2. DOCUMENT PROCESSOR             │
│                                     │
│   ✓ Read file content               │
│   ✓ Extract text based on type:    │
│     • PDF    → PyPDF2               │
│     • DOCX   → python-docx          │
│     • TXT/MD → Direct read          │
│   ✓ Validate content exists         │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│   3. TEXT CHUNKING                  │
│                                     │
│   RecursiveCharacterTextSplitter    │
│   • Chunk Size: 1000 chars          │
│   • Overlap: 200 chars              │
│   • Separators: \n\n, \n, space     │
│                                     │
│   Metadata per chunk:               │
│   • source: filename                │
│   • chunk_id: sequential number     │
│   • document_type: uploaded_doc     │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│   4. EMBEDDING GENERATION           │
│                                     │
│   HuggingFace Embeddings            │
│   • Model: sentence-transformers    │
│   • Converts text → vectors         │
│   • Captures semantic meaning       │
│   • Same model for docs & queries   │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│   5. VECTOR STORAGE                 │
│                                     │
│   ChromaDB                          │
│   Path: data/user_vectorstores/     │
│         {user_id}/                  │
│                                     │
│   ✓ Persistent storage              │
│   ✓ Isolated per user               │
│   ✓ Fast similarity search          │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────┐
│   DOCUMENT      │
│   READY FOR     │
│   QUERYING!     │
│   ✅ Stored     │
└─────────────────┘


═══════════════════════════════════════════════════════════════
                    QUERY PROCESSING FLOW
═══════════════════════════════════════════════════════════════

┌─────────────────┐
│   USER ASKS     │
│   QUESTION      │
│                 │
│   "What is X?"  │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│   6. QUERY EXPANSION                │
│                                     │
│   Paraphraser (Question Generator)  │
│   • Original: "What is X?"          │
│   • Paraphrase 1: "Explain X"       │
│   • Paraphrase 2: "Describe X"      │
│   • Paraphrase 3: "Define X"        │
│                                     │
│   Purpose: Improve retrieval recall │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│   7. EMBEDDING & SEARCH             │
│                                     │
│   For each query variant:           │
│   1. Generate query embedding       │
│   2. Search vector database         │
│   3. Find most similar chunks       │
│   4. Calculate cosine similarity    │
│                                     │
│   Returns: Top K relevant chunks    │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│   8. CONTEXT PREPARATION            │
│                                     │
│   Combine retrieved chunks:         │
│   • Remove duplicates               │
│   • Rank by relevance               │
│   • Format for LLM                  │
│                                     │
│   Context Template:                 │
│   "Context from documents:          │
│    [chunk 1]                        │
│    [chunk 2]                        │
│    ...                              │
│    Question: {user_question}"       │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│   9. LLM PROCESSING (GEMINI)        │
│                                     │
│   Google Gemini AI                  │
│   • Receives: Context + Question    │
│   • Instructions: Answer ONLY       │
│     based on provided context       │
│   • No external knowledge           │
│   • Format with markdown            │
│                                     │
│   If context insufficient:          │
│   → "I don't have enough info..."   │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────────────────────────┐
│   10. RESPONSE GENERATION           │
│                                     │
│   Gemini generates:                 │
│   • Comprehensive answer            │
│   • Well-formatted (markdown)       │
│   • Context-grounded                │
│   • Relevant to query               │
│                                     │
│   Additional info returned:         │
│   • Expanded queries used           │
│   • Retrieved document chunks       │
│   • Knowledge base type             │
└───────────────┬─────────────────────┘
                │
                ▼
┌─────────────────┐
│   11. RETURN    │
│   TO USER       │
│                 │
│   ✅ Answer     │
│   📝 Sources    │
│   🔍 Queries    │
└─────────────────┘
```

---

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                         USER LAYER                            │
├──────────────────────┬───────────────────────────────────────┤
│   Web Browser        │       API Clients                     │
│   (Gradio GUI)       │       (curl, Python, etc.)            │
└──────────┬───────────┴─────────────────┬─────────────────────┘
           │                             │
           ▼                             ▼
┌────────────────────────────────────────────────────────────┐
│                    FASTAPI BACKEND                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Routers                                         │  │
│  │  • document_router.py  (Upload, List, Delete)        │  │
│  │  • qa_service.py       (Question Answering)          │  │
│  │  • query_service.py    (Query Expansion)             │  │
│  │  • question_service.py (Hypothetical Questions)      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────┬────────────────────────────┬─────────────────┘
              │                            │
              ▼                            ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│  DOCUMENT PROCESSOR      │   │  RAG MODEL               │
│                          │   │                          │
│  • PDF extraction        │   │  • Query expansion       │
│  • DOCX parsing          │   │  • Vector search         │
│  • TXT/MD reading        │   │  • Context preparation   │
│  • Text chunking         │   │  • LLM invocation        │
│  • Metadata management   │   │  • Response formatting   │
└────────────┬─────────────┘   └─────────┬────────────────┘
             │                           │
             ▼                           ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│  EMBEDDING SERVICE       │   │  LLM SERVICE             │
│                          │   │                          │
│  HuggingFace             │   │  Google Gemini API       │
│  • sentence-transformers │   │  • gemini-pro            │
│  • 384-dim vectors       │   │  • Temperature: 0.7      │
│  • Cached model          │   │  • Max tokens: 2048      │
└────────────┬─────────────┘   └──────────────────────────┘
             │
             ▼
┌───────────────────────────────────────────────────────────┐
│  VECTOR DATABASE (ChromaDB)                               │
│                                                           │
│  data/user_vectorstores/                                  │
│  ├── user-1/                                              │
│  │   ├── chroma.sqlite3                                   │
│  │   └── {collection_id}/                                │
│  │       └── [vector embeddings]                         │
│  ├── user-2/                                              │
│  │   └── ...                                             │
│  └── user-N/                                              │
│                                                           │
│  Features:                                                │
│  • Persistent storage                                     │
│  • Fast similarity search (cosine distance)               │
│  • Metadata filtering                                     │
│  • User isolation                                         │
└───────────────────────────────────────────────────────────┘
```

---

## Data Flow for Document Upload

```
FILE (user's computer)
    |
    | HTTP POST multipart/form-data
    ▼
┌─────────────────────┐
│ FastAPI Endpoint    │
│ /documents/upload   │
└──────────┬──────────┘
           │
           | UploadFile object
           ▼
┌─────────────────────┐
│ DocumentProcessor   │
│ .process_and_store  │
└──────────┬──────────┘
           │
           ├──> save_upload_file()
           │    (temp storage)
           │
           ├──> extract_text_from_file()
           │    • PDF → PyPDF2.PdfReader
           │    • DOCX → python-docx.Document
           │    • TXT/MD → file.read()
           │
           ├──> create_documents_from_text()
           │    • RecursiveCharacterTextSplitter
           │    • Add metadata (source, chunk_id)
           │
           ├──> get_embeddings()
           │    • HuggingFaceEmbeddings
           │    • Load cached model
           │
           ├──> Load or Create Chroma vectorstore
           │    • persist_directory: user_vectorstores/{user_id}
           │
           ├──> vectorstore.add_documents()
           │    • Generate embeddings for chunks
           │    • Store in ChromaDB
           │
           └──> vectorstore.persist()
                (save to disk)

Response JSON:
{
  "status": "success",
  "document_name": "example.pdf",
  "chunks_created": 42,
  "user_id": "abc-123",
  "vectorstore_path": "data/user_vectorstores/abc-123"
}
```

---

## Data Flow for Question Answering

```
QUESTION (user input)
    |
    | HTTP POST application/json
    ▼
┌─────────────────────┐
│ FastAPI Endpoint    │
│ /generate-answer    │
└──────────┬──────────┘
           │
           | ChatRequest (messages list)
           ▼
┌─────────────────────┐
│ get_user_rag_model  │
│ (or combined)       │
└──────────┬──────────┘
           │
           | Load user's vectorstore
           ▼
┌─────────────────────────────┐
│ QuestionAnsweringWith       │
│ QueryExpansion              │
└──────────┬──────────────────┘
           │
           ├──> 1. PARAPHRASER.generate_paraphrases()
           │    Input: "How do I install?"
           │    Output: [
           │      "How do I install?",
           │      "What are installation steps?",
           │      "How to set this up?"
           │    ]
           │
           ├──> 2. For each paraphrase:
           │    │
           │    ├──> Embed query
           │    │    (HuggingFace embeddings)
           │    │
           │    └──> vectorstore.similarity_search()
           │         (ChromaDB cosine similarity)
           │         Returns: Top 3-5 chunks per query
           │
           ├──> 3. Combine & deduplicate chunks
           │    Remove duplicates across queries
           │    Rank by similarity score
           │
           ├──> 4. Format prompt
           │    Template:
           │    "You are an intelligent assistant...
           │     Context: {retrieved_chunks}
           │     Question: {original_question}"
           │
           └──> 5. LLM.invoke(prompt)
                │
                | Google Gemini API call
                ▼
           ┌────────────────┐
           │  Gemini Pro    │
           │  • Reads ctx   │
           │  • Generates   │
           │  • Formats MD  │
           └────────┬───────┘
                    │
                    | AI-generated answer
                    ▼
           ┌────────────────┐
           │ Format Response│
           │ • messages[]   │
           │ • questions[]  │
           │ • documents[]  │
           └────────┬───────┘
                    │
                    ▼

Response JSON:
{
  "messages": [
    {"role": "user", "content": "How do I install?"},
    {"role": "system", "content": "Based on the docs..."}
  ],
  "questions": ["How do I install?", "What are steps?"],
  "documents": ["Chunk 1 text...", "Chunk 2 text..."],
  "user_id": "abc-123",
  "knowledge_base_type": "personal"
}
```

---

## Technology Stack Flow

```
┌──────────────────────────────────────────────────────┐
│                    FRONTEND                           │
│  Gradio UI (Python-based web interface)              │
│  • File upload widget                                 │
│  • Chat interface                                     │
│  • Document management                                │
└─────────────────┬────────────────────────────────────┘
                  │ HTTP Requests
                  ▼
┌──────────────────────────────────────────────────────┐
│                    BACKEND                            │
│  FastAPI (Python async web framework)                │
│  • RESTful API endpoints                              │
│  • Request validation (Pydantic)                      │
│  • CORS middleware                                    │
│  • Auto-generated docs (/docs)                        │
└─────────────────┬────────────────────────────────────┘
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
┌───────────────┐   ┌──────────────────┐
│   LangChain   │   │  Document        │
│   Framework   │   │  Processing      │
│               │   │                  │
│  • RAG setup  │   │  • PyPDF2        │
│  • Prompts    │   │  • python-docx   │
│  • Chains     │   │  • Text split    │
└───────┬───────┘   └─────────┬────────┘
        │                     │
        ▼                     ▼
┌──────────────────────────────────────┐
│        HuggingFace Ecosystem          │
│  • Transformers library               │
│  • sentence-transformers              │
│  • Embedding models                   │
│  • Model caching                      │
└─────────────────┬────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────┐
│          ChromaDB                     │
│  • Vector storage                     │
│  • Similarity search                  │
│  • SQLite backend                     │
│  • Metadata filtering                 │
└──────────────────────────────────────┘

┌──────────────────────────────────────┐
│      Google Gemini API                │
│  • Cloud-based LLM                    │
│  • REST API calls                     │
│  • Streaming responses                │
│  • Context-aware generation           │
└──────────────────────────────────────┘
```

---

## File Types Support Matrix

```
┌─────────┬─────────────┬──────────────┬───────────────────┐
│ Format  │ Extension   │ Extraction   │ Use Cases         │
├─────────┼─────────────┼──────────────┼───────────────────┤
│ PDF     │ .pdf        │ PyPDF2       │ • Research papers │
│         │             │ PdfReader    │ • Reports         │
│         │             │              │ • eBooks          │
│         │             │              │ • Manuals         │
├─────────┼─────────────┼──────────────┼───────────────────┤
│ Word    │ .docx       │ python-docx  │ • Documents       │
│         │             │ Document     │ • Proposals       │
│         │             │              │ • Contracts       │
│         │             │              │ • Reports         │
├─────────┼─────────────┼──────────────┼───────────────────┤
│ Text    │ .txt        │ Direct read  │ • Notes           │
│         │             │ UTF-8/Latin1 │ • Logs            │
│         │             │              │ • Plain text      │
├─────────┼─────────────┼──────────────┼───────────────────┤
│ MD      │ .md         │ Direct read  │ • Documentation   │
│         │             │ UTF-8        │ • READMEs         │
│         │             │              │ • Wiki pages      │
└─────────┴─────────────┴──────────────┴───────────────────┘

All formats supported WITHOUT hardcoding!
```

---

## User Isolation Architecture

```
data/user_vectorstores/
│
├── user-alice-123/
│   ├── chroma.sqlite3
│   │   (Alice's vector database)
│   │
│   └── collection-xyz/
│       ├── document1.pdf chunks
│       ├── document2.docx chunks
│       └── document3.txt chunks
│
├── user-bob-456/
│   ├── chroma.sqlite3
│   │   (Bob's vector database)
│   │
│   └── collection-abc/
│       ├── contract.pdf chunks
│       └── report.docx chunks
│
└── user-carol-789/
    ├── chroma.sqlite3
    │   (Carol's vector database)
    │
    └── collection-def/
        └── research.pdf chunks

Each user's data is COMPLETELY ISOLATED!
• No cross-user contamination
• Privacy-preserving
• Individual knowledge bases
```

---

## Performance Characteristics

```
┌────────────────────────────────────────────────────┐
│ Operation            │ Time      │ Notes           │
├──────────────────────┼───────────┼─────────────────┤
│ Upload 1MB PDF       │ ~2-3s     │ + embedding     │
│ Upload 10MB PDF      │ ~10-15s   │ + embedding     │
│ Create 100 chunks    │ ~5-8s     │ embedding time  │
│ Query (simple)       │ ~1-2s     │ local search    │
│ Query (complex)      │ ~3-5s     │ expansion + LLM │
│ Gemini API call      │ ~2-4s     │ network latency │
│ List documents       │ <100ms    │ metadata only   │
│ Delete document      │ ~500ms    │ DB operation    │
└────────────────────────────────────────────────────┘

Bottlenecks:
1. Embedding generation (CPU/GPU bound)
2. LLM API calls (network bound)
3. Large PDF text extraction (I/O bound)
```

---

*This visualization shows the complete, generic RAG system flow with NO hardcoding!*
