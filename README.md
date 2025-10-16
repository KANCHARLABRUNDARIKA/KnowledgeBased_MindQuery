<h1>RAG-based Knowledge Extraction System</h1>
<p>
A flexible and scalable Retrieval-Augmented Generation (RAG) system that allows users to upload documents (PDF, DOCX, TXT, MD) and ask questions about their content. The system uses advanced techniques like query expansion and vector search to provide accurate, context-aware answers powered by Google Gemini.
</p>

<h2>Overview</h2>
<p>This repository contains a complete RAG-based question-answering system with:</p>
<ul>
  <li><b>Document Upload & Processing</b>: Upload any PDF/DOCX/TXT/MD document</li>
  <li><b>Intelligent Chunking</b>: Automatic text splitting and embedding generation</li>
  <li><b>Vector Search</b>: Semantic search using ChromaDB and HuggingFace embeddings</li>
  <li><b>Query Expansion</b>: Enhanced retrieval through paraphrasing</li>
  <li><b>AI-Powered Answers</b>: Response generation using Google Gemini</li>
  <li><b>Personal Knowledge Bases</b>: Each user gets their own isolated document store</li>
  <li><b>RESTful API</b>: Built with FastAPI for easy integration</li>
  <li><b>User-Friendly GUI</b>: Interactive Gradio interface</li>
</ul>

<h2>Technology Stack</h2>
<ul>
  <li><b>API Framework:</b> FastAPI - High-performance REST API</li>
  <li><b>User Interface:</b> Gradio - Interactive web interface</li>
  <li><b>RAG Framework:</b> LangChain - RAG pipeline orchestration</li>
  <li><b>LLM:</b> Google Gemini</li>
  <li><b>Embeddings:</b> HuggingFace Transformers</li>
  <li><b>Vector Store:</b> ChromaDB</li>
</ul>

<h2>User Flow</h2>
<ol>
  <li>Upload Document</li>
  <li>Document Processing</li>
  <li>Vector Storage</li>
  <li>Ask Questions</li>
  <li>RAG Retrieval</li>
  <li>AI Response</li>
  <li>Get Answer</li>
</ol>

<h2>🎥 Demo Video</h2>
<p>Watch the system in action:</p>
<p><a href="https://drive.google.com/file/d/1Tzg4nhgU_Eg74ARPJRMVIxhjgJ9y7JPY/view" target="_blank">
👉 Click here to watch the demo video
</a></p>

<h2>Installation</h2>
<pre><code>git clone https://github.com/julianschelb/RAG-based-Knowledge-Extraction-Challenge
cd RAG-based-Knowledge-Extraction-Challenge

<h3>Configure API Keys</h3>
<pre><code>
Rename .env-template to .env
GOOGLE_API_KEY=your_gemini_api_key_here
</code></pre>

<h2>Start Backend</h2>
<pre><code>python main.py</code></pre>
<p>Visit: <a href="http://localhost:8082/docs">http://localhost:8082/docs</a></p>

<h2>Start Frontend</h2>
<pre><code>python src/ragchallenge/gui/enhanced_main.py</code></pre>
<p>Visit: <a href="http://localhost:7860/">http://localhost:7860/</a></p>

<h2>System Architecture</h2>
<h3>Document Processing Pipeline</h3>
<p><b>Phase 1:</b> Upload & Extract</p>
<p><b>Phase 2:</b> Chunk & Embed</p>
<p><b>Phase 3:</b> Question Answering</p>

<h2>Retrieval and Question-Answering Process</h2>
<ol>
  <li>User enters query</li>
  <li>Query Expansion</li>
  <li>Vector Retrieval</li>
  <li>Context + Query → LLM</li>
  <li>Generate Answer</li>
</ol>

<hr>
<h2>⭐ RAG_KB</h2>
<p>High-performance, modular, scalable, and user-friendly knowledge extraction system.</p>

