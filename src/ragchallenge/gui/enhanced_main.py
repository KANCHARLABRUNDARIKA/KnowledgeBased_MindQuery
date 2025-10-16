"""
Enhanced RAG GUI with Document Upload Functionality
Provides a comprehensive interface for document management and Q&A.
"""

import gradio as gr
import requests
import json
import uuid
from typing import List, Optional
import os

# Configuration
API_URL = "http://localhost:8082"

# Global user session
user_session = {"user_id": str(uuid.uuid4())}

def upload_document(file_path: str, user_id: str = None) -> dict:
    """Upload a document to the RAG system."""
    if not file_path:
        return {"error": "No file selected"}
    
    if not user_id:
        user_id = user_session["user_id"]
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            params = {'user_id': user_id}
            response = requests.post(f"{API_URL}/documents/upload", files=files, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Upload failed: {response.text}"}
    except Exception as e:
        return {"error": f"Error uploading file: {str(e)}"}

# def upload_multiple_documents(files: List[str], user_id: str = None) -> dict:
#     """Upload multiple documents to the RAG system."""
#     if not files:
#         return {"error": "No files selected"}
    
#     if not user_id:
#         user_id = user_session["user_id"]
    
#     try:
#         files_data = []
#         for file_path in files:
#             if file_path and os.path.exists(file_path):
#                 files_data.append(('files', open(file_path, 'rb')))
        
#         if not files_data:
#             return {"error": "No valid files found"}
        
#         params = {'user_id': user_id}
#         response = requests.post(f"{API_URL}/documents/upload-multiple", files=files_data, params=params)
        
#         # Close all opened files
#         for _, file_obj in files_data:
#             file_obj.close()
        
#         if response.status_code == 200:
#             return response.json()
#         else:
#             return {"error": f"Upload failed: {response.text}"}
#     except Exception as e:
#         return {"error": f"Error uploading files: {str(e)}"}

def list_user_documents(user_id: str = None) -> dict:
    """List documents in user's knowledge base."""
    if not user_id:
        user_id = user_session["user_id"]
    
    try:
        response = requests.get(f"{API_URL}/documents/list/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to list documents: {response.text}"}
    except Exception as e:
        return {"error": f"Error listing documents: {str(e)}"}

def delete_document(document_name: str, user_id: str = None) -> dict:
    """Delete a document from user's knowledge base."""
    if not user_id:
        user_id = user_session["user_id"]
    
    try:
        response = requests.delete(f"{API_URL}/documents/{user_id}/{document_name}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to delete document: {response.text}"}
    except Exception as e:
        return {"error": f"Error deleting document: {str(e)}"}

def get_vectorstore_info(user_id: str = None) -> dict:
    """Get information about user's vector store."""
    if not user_id:
        user_id = user_session["user_id"]
    
    try:
        response = requests.get(f"{API_URL}/documents/vectorstore/info/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to get vectorstore info: {response.text}"}
    except Exception as e:
        return {"error": f"Error getting vectorstore info: {str(e)}"}

def clear_vectorstore(user_id: str = None) -> dict:
    """Clear all documents from user's vector store."""
    if not user_id:
        user_id = user_session["user_id"]
    
    try:
        response = requests.post(f"{API_URL}/documents/clear/{user_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to clear vectorstore: {response.text}"}
    except Exception as e:
        return {"error": f"Error clearing vectorstore: {str(e)}"}

def ask_question(question: str, knowledge_base_type: str = "personal", user_id: str = None) -> tuple:
    """Ask a question using the RAG system."""
    if not question.strip():
        return "Please enter a question.", "", "", ""
    
    if not user_id:
        user_id = user_session["user_id"]
    
    try:
        messages = [{"role": "user", "content": question}]
        
        # Prepare request based on knowledge base type
        if knowledge_base_type == "personal":
            params = {"user_id": user_id, "use_combined": False}
        elif knowledge_base_type == "combined":
            params = {"user_id": user_id, "use_combined": True}
        else:  # default
            params = {}
        
        response = requests.post(
            f"{API_URL}/generate-answer",
            json={"messages": messages},
            params=params
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Extract answer
            answer = ""
            for msg in result.get("messages", []):
                if msg.get("role") == "system":
                    answer = msg.get("content", "")
            
            # Format additional info
            questions = "\\n".join(result.get("questions", []))
            documents = "\\n---\\n".join(result.get("documents", []))
            kb_type = result.get("knowledge_base_type", knowledge_base_type)
            
            return answer, questions, documents, f"Knowledge Base: {kb_type}"
        else:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            return error_msg, "", "", ""
    
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        return error_msg, "", "", ""

# Gradio interface functions
def handle_file_upload(file):
    """Handle single file upload."""
    if file is None:
        return "No file selected", ""
    
    result = upload_document(file.name)
    
    if "error" in result:
        return f"❌ {result['error']}", ""
    else:
        success_msg = f"✅ {result['message']}\\n"
        success_msg += f"📄 Document: {result['document_name']}\\n"
        success_msg += f"📊 Chunks: {result['chunks_created']}\\n"
        success_msg += f"👤 User ID: {result['user_id']}"
        
        # Update global user session
        user_session["user_id"] = result["user_id"]
        
        return success_msg, get_document_list_display()

# def handle_multiple_file_upload(files):
#     """Handle multiple file upload."""
#     if not files:
#         return "No files selected", ""
    
#     file_paths = [f.name for f in files if f is not None]
#     result = upload_multiple_documents(file_paths)
    
#     if "error" in result:
#         return f"❌ {result['error']}", ""
#     else:
#         success_msg = f"✅ Processed {result['total_files']} files\\n"
#         success_msg += f"📈 Successful: {result['successful_uploads']}\\n"
#         success_msg += f"❌ Failed: {result['failed_uploads']}\\n"
#         success_msg += f"👤 User ID: {result['user_id']}"
        
#         # Update global user session
#         user_session["user_id"] = result["user_id"]
        
#         return success_msg, get_document_list_display()

def get_document_list_display():
    """Get formatted display of user documents."""
    result = list_user_documents()
    
    if "error" in result:
        return f" {result['error']}"
    
    if not result.get("documents"):
        return "📭 No documents uploaded yet."
    
    display = f"*Knowledge Base ({result['total_documents']} documents)*\\n\\n"
    
    for doc in result["documents"]:
        display += f" *{doc['name']}*\\n"
        display += f"    Chunks: {doc['chunks']}\\n"
        display += f"    Type: {doc['document_type']}\\n\\n"
    
    return display

def handle_document_deletion(document_name):
    """Handle document deletion."""
    if not document_name.strip():
        return "Please enter a document name", ""
    
    result = delete_document(document_name.strip())
    
    if "error" in result:
        return f"❌ {result['error']}", get_document_list_display()
    else:
        success_msg = f"✅ {result['message']}\\n"
        success_msg += f"🗑 Deleted {result['deleted_chunks']} chunks"
        return success_msg, get_document_list_display()

def handle_vectorstore_clear():
    """Handle clearing the vectorstore."""
    result = clear_vectorstore()
    
    if "error" in result:
        return f"❌ {result['error']}", ""
    else:
        return f"✅ {result['message']}", "📭 No documents uploaded yet."

def get_vectorstore_info_display():
    """Get vectorstore information display."""
    result = get_vectorstore_info()
    
    if "error" in result:
        return f"❌ {result['error']}"
    
    info = f"📊 *Vector Store Information*\\n\\n"
    info += f"👤 User ID: {result['user_id']}\\n"
    info += f"📚 Total Documents: {result['total_documents']}\\n"
    info += f"📊 Total Chunks: {result['total_chunks']}\\n"
    info += f"📋 Status: {result['status']}\\n"
    
    return info

# Custom theme with neon cyberpunk style
def create_custom_theme():
    return gr.themes.Base(
        font=["JetBrains Mono", "Orbitron", "monospace"],
        neutral_hue="slate",
        primary_hue="cyan",
        secondary_hue="pink",
    ).set(
        body_background_fill="#E89D9D",
        body_text_color="#0a0a0a",
        block_title_text_color="#D2FD10",
        block_label_text_color="#d0e22f",
        input_background_fill="#f3f3fa",
        input_border_color="#00ff99",
        input_placeholder_color="#4d4d69",
        button_primary_background_fill="linear-gradient(90deg, #582baa, #00ffff)",
        button_primary_background_fill_hover="linear-gradient(90deg, #582baa, #ff00ff)",
        button_primary_text_color="#000000",
        button_secondary_background_fill="#f3f1f5",
        button_secondary_background_fill_hover="#582baa",
        button_secondary_text_color="#7df5c5",
        block_background_fill="rgba(13, 13, 26, 0.8)",
        background_fill_primary="#f2f2fb",
        background_fill_secondary="#e3e0e9",
        border_color_primary="#07022f",
    )

# Custom CSS with cyberpunk neon styling and liquid animations
CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

:root {
    --neon-cyan:#07022f ;
    --neon-pink: #07022f;
    --neon-green:#f3f3fa;
}

.liquid-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: 
        linear-gradient(125deg, #e8c3df 0%, #e8c3df 100%),
        radial-gradient(circle at 50% 50%, rgba(0, 255, 255, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(255, 0, 255, 0.03) 0%, transparent 50%);
    background-size: 100% 100%, 100% 100%, 100% 100%;
    background-position: 0 0, 0 0, 0 0;
    animation: gradientMove 20s ease infinite;
}

@keyframes gradientMove {
    0% {
        background-position: 0% 0%, 0 0, 30px 30px;
    }
    50% {
        background-position: 100% 100%, 60px 60px, 90px 90px;
    }
    100% {
        background-position: 0% 0%, 0 0, 30px 30px;
    }
}

.container {
    backdrop-filter: blur(5px);
    border-radius: 0;
    border: 2px solid var(--neon-cyan);
    padding: 24px;
    margin: 24px 0;
    background: rgba(13, 13, 26, 0.8);
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    position: relative;
    overflow: hidden;
}

.container::before {
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    border: 2px solid var(--neon-pink);
    clip-path: polygon(0 0, 100% 0, 100% 100%, 95% 100%, 95% 90%, 85% 90%, 85% 100%, 15% 100%, 15% 90%, 5% 90%, 5% 100%, 0 100%);
    animation: borderFlash 3s infinite;
}

.title-container {
    text-align: center;
    margin-bottom: 3rem;
    background: linear-gradient(90deg, rgba(0, 255, 255, 0.1), rgba(255, 0, 255, 0.1));
    padding: 2rem;
    border: 2px solid var(--neon-cyan);
    position: relative;
    clip-path: polygon(0 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%);
}

.title-container h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.5em;
    color: var(--neon-cyan);
    text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
    letter-spacing: 2px;
    margin: 0;
}

.gradio-button {
    font-family: 'Orbitron', sans-serif !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    clip-path: polygon(10px 0, 100% 0, calc(100% - 10px) 100%, 0 100%) !important;
}

.gradio-button.primary {
    background: linear-gradient(90deg, var(--neon-cyan), var(--neon-pink)) !important;
    border: none !important;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.3) !important;
    color: #000000 !important;
    font-weight: bold !important;
}

.gradio-button.secondary {
    background: transparent !important;
    border: 2px solid var(--neon-green) !important;
    color: var(--neon-green) !important;
}

.input-container {
    border: 2px solid var(--neon-cyan);
    background: rgba(13, 13, 26, 0.8);
    padding: 20px;
    margin: 10px 0;
    clip-path: polygon(0 0, calc(100% - 20px) 0, 100% 20px, 100% 100%, 20px 100%, 0 calc(100% - 20px));
}

.output-container {
    border: 2px solid var(--neon-pink);
    background: rgba(13, 13, 26, 0.8);
    padding: 20px;
    margin: 10px 0;
    clip-path: polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px);
}

@keyframes matrix {
    0% { background-position: 0 0; }
    100% { background-position: 0 1000px; }
}

@keyframes borderFlash {
    0%, 100% { border-color: var(--neon-pink); }
    50% { border-color: var(--neon-cyan); }
}

@keyframes glitch {
    0% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
    100% { transform: translate(0); }
}

/* Custom styling for components */
.gradio-textbox, .gradio-dropdown, .gradio-radio {
    font-family: 'JetBrains Mono', monospace !important;
    background: rgba(13, 13, 26, 0.8) !important;
    border: 2px solid var(--neon-cyan) !important;
    color: var(--neon-green) !important;
}

.gradio-markdown {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--neon-cyan) !important;
    text-shadow: 0 0 5px rgba(0, 255, 255, 0.5) !important;
}

.tab-nav {
    border-bottom: 2px solid var(--neon-cyan) !important;
}

.tab-nav button {
    font-family: 'Orbitron', sans-serif !important;
    color: var(--neon-green) !important;
    border: none !important;
    background: transparent !important;
    position: relative !important;
    clip-path: polygon(10px 0, calc(100% - 10px) 0, 100% 100%, 0 100%) !important;
}

.tab-nav button.selected {
    color: var(--neon-cyan) !important;
    border-bottom: 2px solid var(--neon-pink) !important;
}
"""

# Create Gradio interface
def create_interface():
    with gr.Blocks(
        title="Query Mind",
        theme=create_custom_theme(),
        css=CUSTOM_CSS
    ) as app:
        gr.HTML('<div class="liquid-bg"></div>')
        
        with gr.Column(elem_classes="title-container"):
            gr.HTML("""
                <div style="position: relative; text-align: center;">
                    <h1 style="font-size: 5em; margin-bottom: 0.5em;">
                        <span style="color: #ffffff; ">Query</span><span style="color: #ffffff;">Mind</span>
                    </h1>
                    <div style="font-family: 'JetBrains Mono', monospace; color: #00ff99; text-shadow: 0 0 5px #00ff99; font-size: 1.2em; margin-top: -0.5em;">
                       Smart Assistant
                    </div>
                    
                </div>
            """)
        
        with gr.Tab("File Upload"):
            with gr.Column(elem_classes="container"):
                gr.Markdown("##  Upload Center", elem_classes="section-header")
                gr.Markdown("Convert your documents into a smart knowledge system")
                
                with gr.Row():
                    with gr.Column(scale=1, elem_classes="glass-panel"):
                        gr.Markdown("### Upload a File", elem_classes="panel-header")
                        file_upload = gr.File(
                            label="Select Document",
                            file_types=[".pdf", ".docx", ".txt", ".md"],
                            elem_classes="file-upload"
                        )
                        upload_btn = gr.Button(
                            "Upload Document",
                            variant="primary",
                            elem_classes="upload-btn"
                        )
                        upload_result = gr.Textbox(
                            label="Upload Status",
                            lines=4,
                            elem_classes="result-box"
                        )
                    
                    # with gr.Column(scale=1, elem_classes="glass-panel"):
                    #     gr.Markdown("### Batch Upload", elem_classes="panel-header")
                    #     files_upload = gr.File(
                    #         label="Select Multiple Documents",
                    #         file_count="multiple",
                    #         file_types=[".pdf", ".docx", ".txt", ".md"],
                    #         elem_classes="file-upload"
                    #     )
                    #     multi_upload_btn = gr.Button(
                    #         "Upload Multiple",
                    #         variant="primary",
                    #         elem_classes="upload-btn"
                    #     )
                    #     multi_upload_result = gr.Textbox(
                    #         label="Batch Upload Status",
                    #         lines=4,
                    #         elem_classes="result-box"
                    #     )
        
        with gr.Tab("Document Repository"):
            with gr.Column(elem_classes="container"):
                gr.Markdown("## Knowledge Base Management", elem_classes="section-header")
                gr.Markdown("Manage and explore your smart document library")
                
                with gr.Row():
                    with gr.Column(scale=2, elem_classes="glass-panel"):
                        with gr.Group():
                            gr.Markdown("###Document Repository", elem_classes="panel-header")
                            doc_list = gr.Markdown(
                                value=get_document_list_display(),
                                elem_classes="doc-list"
                            )
                            refresh_btn = gr.Button(
                                " Refresh List",
                                variant="secondary",
                                elem_classes="refresh-btn"
                            )
                    
                    with gr.Column(scale=1, elem_classes="glass-panel"):
                        with gr.Group():
                            gr.Markdown("###  Document Management", elem_classes="panel-header")
                            doc_to_delete = gr.Textbox(
                                label="Document to Delete",
                                placeholder="Enter exact document name...",
                                elem_classes="delete-input"
                            )
                            delete_btn = gr.Button(
                                " Delete ",
                                variant="secondary",
                                elem_classes="delete-btn"
                            )
                            delete_result = gr.Textbox(
                                label="Operation Result",
                                lines=2,
                                elem_classes="result-box"
                            )
                        
                        with gr.Group(elem_classes="info-panel"):
                            gr.Markdown("### System Statistics", elem_classes="panel-header")
                            info_btn = gr.Button(
                                " View Statistics",
                                variant="secondary",
                                elem_classes="info-btn"
                            )
                            vectorstore_info = gr.Markdown(elem_classes="info-display")
                        
                        with gr.Group(elem_classes="danger-zone"):
                            gr.Markdown("### Danger Zone", elem_classes="panel-header")
                            clear_btn = gr.Button(
                                "Clear All Documents",
                                variant="stop",
                                elem_classes="clear-btn"
                            )
                            clear_result = gr.Textbox(
                                label="Clear Operation Result",
                                lines=2,
                                elem_classes="result-box"
                            )
        
        with gr.Tab("Ask Questions"):
            with gr.Column(elem_classes="container qa-container"):
                gr.Markdown("##  AI Knowledge Assistant", elem_classes="section-header")
                gr.Markdown("Interact with your documents through intelligent conversation")
                
                with gr.Row():
                    with gr.Column(scale=2, elem_classes="glass-panel input-panel"):
                        question_input = gr.Textbox(
                            label="Your Question",
                            placeholder="Ask anything about your documents...",
                            lines=3,
                            elem_classes="question-input"
                        )
                        
                        with gr.Group(elem_classes="kb-selector"):
                            gr.Markdown("###  Knowledge Source", elem_classes="subsection-header")
                            knowledge_base_choice = gr.Radio(
                                choices=["personal", "combined", "default"],
                                label="Select Knowledge Base",
                                value="personal",
                                info="🔹 Personal: Your documents only\n🔹 Combined: Your + default docs\n🔹 Default: Built-in docs only",
                                elem_classes="kb-radio"
                            )
                        
                        ask_btn = gr.Button(
                            "Ask AI ",
                            variant="primary",
                            size="lg",
                            elem_classes="ask-btn"
                        )
                    
                    with gr.Column(scale=3, elem_classes="glass-panel output-panel"):
                        answer_output = gr.Textbox(
                            label="AI Response",
                            lines=8,
                            max_lines=20,
                            elem_classes="answer-box"
                        )
                        
                        with gr.Accordion(
                            "Analysis Details",
                            open=False,
                            elem_classes="details-accordion"
                        ):
                            questions_output = gr.Textbox(
                                label="Generated Search Queries",
                                lines=3,
                                elem_classes="details-box"
                            )
                            documents_output = gr.Textbox(
                                label="Reference Documents",
                                lines=4,
                                elem_classes="details-box"
                            )
                            kb_info_output = gr.Textbox(
                                label="Knowledge Base Details",
                                lines=1,
                                elem_classes="details-box"
                            )
        
        # Event handlers
        upload_btn.click(
            handle_file_upload,
            inputs=[file_upload],
            outputs=[upload_result, doc_list]
        )
        
        # multi_upload_btn.click(
        #     handle_multiple_file_upload,
        #     inputs=[files_upload],
        #     outputs=[multi_upload_result, doc_list]
        # )
        
        refresh_btn.click(
            lambda: get_document_list_display(),
            outputs=[doc_list]
        )
        
        delete_btn.click(
            handle_document_deletion,
            inputs=[doc_to_delete],
            outputs=[delete_result, doc_list]
        )
        
        info_btn.click(
            get_vectorstore_info_display,
            outputs=[vectorstore_info]
        )
        
        clear_btn.click(
            handle_vectorstore_clear,
            outputs=[clear_result, doc_list]
        )
        
        ask_btn.click(
            ask_question,
            inputs=[question_input, knowledge_base_choice],
            outputs=[answer_output, questions_output, documents_output, kb_info_output]
        )
        
        # Auto-refresh document list on tab switch
        app.load(
            lambda: get_document_list_display(),
            outputs=[doc_list]
        )
    
    return app

if __name__ == "__main__":
    # Display user session info
    print(f"🚀 Starting RAG Knowledge Base Manager")
    print(f"👤 User Session ID: {user_session['user_id']}")
    print(f"🔗 API URL: {API_URL}")
    
    # Create and launch the interface
    app = create_interface()
    # Add additional CSS for enhanced styling
    app.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True,
        height=1000,  # Set a good default height
        width="100%"
    )