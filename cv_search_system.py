"""
CV Vector Search System
Extract text from PDF CV, create vector chunks, and enable intelligent search with Gemini LLM.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

import PyPDF2
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
from ragchallenge.api.config import settings
from pathlib import Path

class CVSearchSystem:
    """Intelligent CV search system using vector embeddings and Gemini LLM."""
    
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.prompt_template = None
        self.cv_vectorstore_path = "data/cv_vectorstore"
        
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF file."""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    text += f"\n[Page {page_num + 1}]\n{page_text}\n"
                return text
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def initialize_components(self):
        """Initialize embeddings, LLM, and prompt template."""
        print("🔧 Initializing components...")
        
        # Initialize embeddings
        print("📊 Loading embeddings model...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': settings.embedding_model_device}
        )
        
        # Initialize Gemini LLM
        print("🤖 Initializing Gemini LLM...")
        self.llm = ChatGoogleGenerativeAI(
            model=settings.chat_model,
            google_api_key=settings.google_api_key,
            temperature=0.3,  # Lower temperature for more precise CV responses
            max_output_tokens=1024,
        )
        
        # Create prompt template for CV queries
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert HR assistant and career advisor. You have access to a candidate's CV/resume information.

Based on the CV context provided below, answer questions about the candidate's:
- Professional experience and work history
- Skills and technical competencies  
- Education and qualifications
- Projects and achievements
- Contact information and personal details

Provide accurate, professional responses based only on the information available in the CV context.

CV Context:
{context}"""),
            ("human", "{question}")
        ])
        
        print("✅ All components initialized successfully")
    
    def process_cv_pdf(self, pdf_path: str) -> bool:
        """Process CV PDF and create vector store."""
        try:
            print(f"📄 Processing CV PDF: {pdf_path}")
            
            # Extract text from PDF
            cv_text = self.extract_text_from_pdf(pdf_path)
            print(f"📝 Extracted {len(cv_text)} characters from CV")
            
            # Create text chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,  # Smaller chunks for CV content
                chunk_overlap=100,
                length_function=len,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
            
            chunks = text_splitter.split_text(cv_text)
            print(f"🧩 Created {len(chunks)} text chunks")
            
            # Create documents with metadata
            documents = []
            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={
                        "source": "Thanush_Chowdary_CV.pdf",
                        "chunk_id": i,
                        "document_type": "cv",
                        "total_chunks": len(chunks)
                    }
                )
                documents.append(doc)
            
            # Remove existing CV vectorstore if it exists
            import shutil
            if os.path.exists(self.cv_vectorstore_path):
                shutil.rmtree(self.cv_vectorstore_path)
                print("🗑️ Removed existing CV vector store")
            
            # Create new vectorstore for CV
            print("🔧 Creating CV vector store...")
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=self.cv_vectorstore_path
            )
            
            print("✅ CV vector store created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error processing CV PDF: {e}")
            return False
    
    def load_cv_vectorstore(self):
        """Load existing CV vector store."""
        try:
            if not os.path.exists(self.cv_vectorstore_path):
                return False
                
            print("📚 Loading existing CV vector store...")
            self.vectorstore = Chroma(
                persist_directory=self.cv_vectorstore_path,
                embedding_function=self.embeddings
            )
            
            # Check if vectorstore has content
            collection = self.vectorstore._collection
            results = collection.get()
            
            if len(results['ids']) == 0:
                print("⚠️ CV vector store is empty")
                return False
            
            print(f"✅ Loaded CV vector store with {len(results['ids'])} chunks")
            return True
            
        except Exception as e:
            print(f"❌ Error loading CV vector store: {e}")
            return False
    
    def search_cv(self, query: str, k: int = 5) -> dict:
        """Search CV content and generate intelligent response."""
        try:
            print(f"🔍 Searching CV for: '{query}'")
            
            # Retrieve relevant chunks
            search_results = self.vectorstore.similarity_search(query, k=k)
            
            if not search_results:
                return {
                    "query": query,
                    "answer": "I couldn't find relevant information in the CV for your query.",
                    "sources": [],
                    "context": ""
                }
            
            # Prepare context
            context = "\n\n".join([doc.page_content for doc in search_results])
            
            print(f"📄 Retrieved {len(search_results)} relevant chunks")
            
            # Generate response using Gemini
            chain = self.prompt_template | self.llm | StrOutputParser()
            
            response = chain.invoke({
                "context": context,
                "question": query
            })
            
            # Prepare sources information
            sources = []
            for doc in search_results:
                sources.append({
                    "content": doc.page_content[:150] + "...",
                    "chunk_id": doc.metadata.get("chunk_id", "N/A"),
                    "source": doc.metadata.get("source", "CV")
                })
            
            return {
                "query": query,
                "answer": response,
                "sources": sources,
                "context": context[:500] + "..." if len(context) > 500 else context
            }
            
        except Exception as e:
            print(f"❌ Error searching CV: {e}")
            return {
                "query": query,
                "answer": f"Error occurred while searching: {str(e)}",
                "sources": [],
                "context": ""
            }

def main():
    """Main function to run CV search system."""
    print("🎯 CV Vector Search System")
    print("=" * 50)
    
    # Initialize system
    cv_system = CVSearchSystem()
    cv_system.initialize_components()
    
    # CV PDF path
    cv_pdf_path = "data/raw/Thanush_Chowdary_CV.pdf"
    
    # Check if CV PDF exists
    if not os.path.exists(cv_pdf_path):
        print(f"❌ CV PDF not found at: {cv_pdf_path}")
        return
    
    # Try to load existing vectorstore or create new one
    if not cv_system.load_cv_vectorstore():
        print("🔄 Creating new CV vector store...")
        if not cv_system.process_cv_pdf(cv_pdf_path):
            print("❌ Failed to process CV PDF")
            return
    
    # Interactive search loop
    print("\n🚀 CV Search System Ready!")
    print("Ask questions about Thanush's CV (type 'quit' to exit):")
    print("Example questions:")
    print("- What is Thanush's educational background?")
    print("- What programming languages does he know?")
    print("- What work experience does he have?")
    print("- What projects has he worked on?")
    print("-" * 50)
    
    while True:
        try:
            query = input("\n❓ Your question: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not query:
                continue
            
            # Search CV
            result = cv_system.search_cv(query)
            
            # Display results
            print(f"\n🎯 Answer:")
            print("=" * 40)
            print(result['answer'])
            print("=" * 40)
            
            print(f"\n📚 Sources ({len(result['sources'])} chunks):")
            for i, source in enumerate(result['sources'], 1):
                print(f"  {i}. {source['content']}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()