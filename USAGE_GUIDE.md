# RAG System - Complete User Guide

## Table of Contents
1. [System Overview](#system-overview)
2. [User Flow](#user-flow)
3. [Getting Started](#getting-started)
4. [Using the API](#using-the-api)
5. [Using the GUI](#using-the-gui)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

---

## System Overview

This RAG (Retrieval-Augmented Generation) system allows you to:
- Upload documents (PDF, DOCX, TXT, MD)
- Ask questions about your documents
- Get AI-powered answers using Google Gemini
- Manage personal knowledge bases

**Key Principle**: The system does NOT hardcode any specific document types. It works with ANY content you upload!

---

## User Flow

```
┌─────────────────┐
│  1. Upload PDF  │
│  DOCX, TXT, MD  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. Extract &   │
│  Chunk Text     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Generate    │
│  Embeddings     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. Store in    │
│  Vector DB      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. Ask         │
│  Question       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. Retrieve    │
│  Relevant       │
│  Chunks (RAG)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  7. Generate    │
│  Answer with    │
│  Gemini AI      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  8. Return      │
│  Response       │
└─────────────────┘
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Setup Steps

1. **Configure Environment**
   ```bash
   # Copy environment template
   cp .env-template .env
   
   # Edit .env and add your API key
   GOOGLE_API_KEY=your_api_key_here
   ```

2. **Start the Backend**
   ```bash
   python main.py
   ```
   API will be available at: http://localhost:8082

3. **Start the Frontend (Optional)**
   ```bash
   python src/ragchallenge/gui/enhanced_main.py
   ```
   GUI will be available at: http://localhost:7860

---

## Using the API

### 1. Upload a Document

**Endpoint**: `POST /documents/upload`

```bash
# Upload a document
curl -X POST "http://localhost:8082/documents/upload?user_id=my-user-123" \
  -F "file=@/path/to/document.pdf"
```

**Response**:
```json
{
  "status": "success",
  "message": "Successfully processed document.pdf",
  "document_name": "document.pdf",
  "chunks_created": 25,
  "vectorstore_path": "data/user_vectorstores/my-user-123",
  "user_id": "my-user-123",
  "text_preview": "First 200 characters of text..."
}
```

**Supported File Types**:
- PDF (`.pdf`)
- Word Document (`.docx`)
- Text File (`.txt`)
- Markdown (`.md`)

---

### 2. List Uploaded Documents

**Endpoint**: `GET /documents/list/{user_id}`

```bash
curl -X GET "http://localhost:8082/documents/list/my-user-123"
```

**Response**:
```json
{
  "user_id": "my-user-123",
  "documents": [
    {
      "name": "document.pdf",
      "chunks": 25,
      "document_type": "uploaded_document"
    }
  ],
  "total_documents": 1
}
```

---

### 3. Ask Questions

**Endpoint**: `POST /generate-answer`

```bash
curl -X POST "http://localhost:8082/generate-answer?user_id=my-user-123" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "What is the main topic of this document?"}
    ]
  }'
```

**Response**:
```json
{
  "messages": [
    {"role": "user", "content": "What is the main topic of this document?"},
    {"role": "system", "content": "Based on the document, the main topic is..."}
  ],
  "questions": ["paraphrased question 1", "paraphrased question 2"],
  "documents": ["Relevant chunk 1...", "Relevant chunk 2..."],
  "user_id": "my-user-123",
  "knowledge_base_type": "personal"
}
```

---

### 4. Delete a Document

**Endpoint**: `DELETE /documents/{user_id}/{document_name}`

```bash
curl -X DELETE "http://localhost:8082/documents/my-user-123/document.pdf"
```

---

### 5. Clear All Documents

**Endpoint**: `POST /documents/clear/{user_id}`

```bash
curl -X POST "http://localhost:8082/documents/clear/my-user-123"
```

---

## Using the GUI

### 1. Upload Documents

1. Navigate to the **Document Management** tab
2. Click **Choose File** or drag and drop
3. Click **Upload Document**
4. Wait for confirmation (shows chunks created)
5. Your user ID is automatically generated and saved

### 2. View Uploaded Documents

1. Click **Refresh Document List**
2. See all uploaded documents with chunk counts
3. View vectorstore statistics

### 3. Ask Questions

1. Navigate to the **Q&A** tab
2. Select knowledge base type:
   - **Personal**: Search only your uploaded documents
   - **Combined**: Search both your documents and default knowledge base
   - **Default**: Search only default knowledge base
3. Type your question
4. Click **Ask Question**
5. View:
   - AI-generated answer
   - Expanded queries used for search
   - Retrieved document chunks
   - Knowledge base type used

### 4. Delete Documents

1. In Document Management tab
2. Enter document name
3. Click **Delete Document**

---

## Advanced Features

### Query Expansion

The system automatically expands your query by:
1. Paraphrasing your question multiple ways
2. Searching with all variations
3. Combining results for better accuracy

Example:
- Your question: "How do I install this?"
- Expanded queries:
  - "What are the installation steps?"
  - "How can I set this up?"
  - "What is the installation process?"

### Personal vs Combined Knowledge Bases

**Personal Knowledge Base**:
- Only searches YOUR uploaded documents
- Isolated from other users
- Best for private/confidential documents

**Combined Knowledge Base**:
- Searches both personal AND default documents
- Useful when you want general + specific information

**Default Knowledge Base**:
- Pre-loaded documents (if any)
- Shared across all users

### Multi-Document Upload

Upload multiple documents at once:
```bash
curl -X POST "http://localhost:8082/documents/upload-multiple?user_id=my-user-123" \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.pdf" \
  -F "files=@doc3.docx"
```

---

## Troubleshooting

### Problem: "I don't have enough information to answer..."

**Causes**:
1. Document not uploaded yet
2. Question not related to document content
3. Document chunks don't match query

**Solutions**:
- Verify document uploaded successfully
- Check document contains relevant information
- Rephrase your question
- Try more specific questions

---

### Problem: API returns mock responses

**Cause**: Google Gemini API key not configured

**Solution**:
1. Get API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Add to `.env` file:
   ```
   GOOGLE_API_KEY=your_actual_key_here
   ```
3. Restart the application

---

### Problem: Upload fails with "Error processing PDF"

**Causes**:
- Corrupted PDF
- Encrypted/password-protected PDF
- Scanned PDF without OCR

**Solutions**:
- Try converting to different format (DOCX, TXT)
- Remove password protection
- Use OCR software to extract text first

---

### Problem: Slow response times

**Causes**:
- Large documents (many chunks)
- Multiple documents in knowledge base
- Slow embedding model

**Solutions**:
- Split very large documents into smaller ones
- Use more specific queries (retrieves fewer chunks)
- Consider upgrading hardware (GPU helps with embeddings)

---

## Best Practices

### 1. Document Preparation
- ✅ Use clear, well-formatted documents
- ✅ Include headings and structure
- ✅ Keep documents focused on specific topics
- ❌ Avoid very long documents without structure
- ❌ Don't upload scanned images without OCR

### 2. Asking Questions
- ✅ Be specific and clear
- ✅ Use terms from your document
- ✅ Ask one question at a time
- ❌ Avoid very broad questions
- ❌ Don't ask about content not in documents

### 3. Managing Documents
- ✅ Use descriptive filenames
- ✅ Delete old/irrelevant documents
- ✅ Keep knowledge base organized
- ❌ Don't upload duplicate documents
- ❌ Don't mix unrelated content

---

## Example Workflows

### Workflow 1: Research Paper Analysis

```bash
# 1. Upload research paper
curl -X POST "http://localhost:8082/documents/upload?user_id=researcher-1" \
  -F "file=@research_paper.pdf"

# 2. Ask about methodology
curl -X POST "http://localhost:8082/generate-answer?user_id=researcher-1" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What methodology was used?"}]}'

# 3. Ask about results
curl -X POST "http://localhost:8082/generate-answer?user_id=researcher-1" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What were the key findings?"}]}'
```

### Workflow 2: Technical Documentation

```bash
# 1. Upload multiple docs
curl -X POST "http://localhost:8082/documents/upload-multiple?user_id=dev-team" \
  -F "files=@api_guide.pdf" \
  -F "files=@setup_instructions.docx" \
  -F "files=@troubleshooting.md"

# 2. Ask technical questions
curl -X POST "http://localhost:8082/generate-answer?user_id=dev-team" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "How do I configure the API?"}]}'
```

### Workflow 3: Legal Document Review

```bash
# 1. Upload contract
curl -X POST "http://localhost:8082/documents/upload?user_id=legal-001" \
  -F "file=@contract.pdf"

# 2. Extract key terms
curl -X POST "http://localhost:8082/generate-answer?user_id=legal-001" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What are the payment terms?"}]}'

# 3. Find obligations
curl -X POST "http://localhost:8082/generate-answer?user_id=legal-001" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What are the parties obligations?"}]}'
```

---

## API Complete Reference

### Base URL
```
http://localhost:8082
```

### Authentication
Currently no authentication required. Each user isolated by `user_id`.

### Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/documents/upload` | Upload single document |
| POST | `/documents/upload-multiple` | Upload multiple documents |
| GET | `/documents/list/{user_id}` | List user's documents |
| DELETE | `/documents/{user_id}/{doc_name}` | Delete specific document |
| POST | `/documents/clear/{user_id}` | Clear all user documents |
| GET | `/documents/vectorstore/info/{user_id}` | Get vectorstore stats |
| POST | `/generate-answer` | Ask question (RAG + Gemini) |
| POST | `/generate-answer-personal` | Ask question (personal KB only) |

---

## Support & Contact

For issues, questions, or contributions:
- GitHub Issues: [Repository Issues](https://github.com/julianschelb/RAG-based-Knowledge-Extraction-Challenge/issues)
- Documentation: [README.md](./README.md)

---

**Remember**: This system is completely generic - it works with ANY document type without hardcoding!
