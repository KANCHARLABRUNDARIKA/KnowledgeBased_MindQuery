# 🚀 Quick Start Guide - RAG System

## ⚡ Get Started in 5 Minutes!

### Step 1: Configure API Key (30 seconds)

1. Get your Google Gemini API key from: https://makersuite.google.com/app/apikey

2. Open `.env` file and add:
```env
GOOGLE_API_KEY=your_api_key_here
```

That's it! 🎉

---

### Step 2: Start the Backend (10 seconds)

```bash
python main.py
```

You should see:
```
✅ Successfully initialized Gemini LLM
✅ Server running on http://localhost:8082
```

---

### Step 3: Test It! (2 minutes)

#### Option A: Use the Test Script
```bash
# Open another terminal
python test_complete_flow.py
```

This will automatically:
- ✅ Upload a test document
- ✅ Ask a question
- ✅ Show the AI response
- ✅ Clean up

---

#### Option B: Use the GUI
```bash
# Open another terminal
python src/ragchallenge/gui/enhanced_main.py
```

Then visit: http://localhost:7860

1. **Upload Tab**: Drop your PDF/DOCX/TXT/MD file
2. **Q&A Tab**: Ask questions about your document
3. **Get AI answers!** 🤖

---

#### Option C: Use the API Directly

```bash
# Upload a document
curl -X POST "http://localhost:8082/documents/upload?user_id=my-user" \
  -F "file=@your_document.pdf"

# Ask a question
curl -X POST "http://localhost:8082/generate-answer?user_id=my-user" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is this document about?"}]}'
```

---

## 🎯 What You Can Do

### Upload Any Document Type
- 📄 PDF files
- 📄 Word documents (DOCX)
- 📄 Text files (TXT)
- 📄 Markdown files (MD)

### Ask Any Question
- "What is the main topic?"
- "Summarize this document"
- "What are the key points?"
- "Explain [specific concept]"
- "What does it say about [topic]?"

### Works With ANY Content
- ✅ Research papers
- ✅ Legal documents
- ✅ Technical manuals
- ✅ Business reports
- ✅ Educational content
- ✅ Personal documents
- ✅ **Anything else!**

---

## 📋 Quick Commands Reference

```bash
# Start backend
python main.py

# Start GUI
python src/ragchallenge/gui/enhanced_main.py

# Run tests
python test_complete_flow.py

# View API docs
# Visit: http://localhost:8082/docs
```

---

## 🔍 Verify It's Working

### ✅ Backend Running?
Visit: http://localhost:8082/docs
- Should see API documentation

### ✅ Can Upload Documents?
```bash
curl -X POST "http://localhost:8082/documents/upload?user_id=test" \
  -F "file=@README.md"
```
- Should return `"status": "success"`

### ✅ Can Ask Questions?
```bash
curl -X POST "http://localhost:8082/generate-answer?user_id=test" \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "What is this?"}]}'
```
- Should return an AI-generated answer

---

## ⚠️ Troubleshooting

### "Cannot connect to API"
```bash
# Make sure backend is running
python main.py
```

### "Mock LLM" responses instead of Gemini
```bash
# Check .env file has valid API key
GOOGLE_API_KEY=your_key_here

# Restart the application
```

### "Upload failed"
- Check file type (must be PDF/DOCX/TXT/MD)
- Verify file is not corrupted
- Try a different file

---

## 📚 Learn More

For detailed documentation, see:
- `COMPLETE_SUMMARY.md` - Everything you need to know
- `USAGE_GUIDE.md` - Detailed API and GUI usage
- `FLOW_VISUALIZATION.md` - System architecture diagrams
- `README.md` - Full project documentation

---

## 🎉 That's It!

You're ready to:
1. ✅ Upload ANY document (PDF, DOCX, TXT, MD)
2. ✅ Ask questions about it
3. ✅ Get AI-powered answers using RAG + Gemini

**No hardcoding. No configuration per document. Just upload and go!** 🚀

---

*Need help? Check `COMPLETE_SUMMARY.md` for full details!*
