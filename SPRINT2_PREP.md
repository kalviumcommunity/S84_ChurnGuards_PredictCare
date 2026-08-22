# Sprint 2 Preparation - RAG Implementation Roadmap

## ✅ Completed (Sprint 1)
- [x] **Module 2.36** - Real risk calculation algorithm
- [x] **Module 2.37** - Database schema & SQL integration
- [x] **Module 2.38-2.40** - SQL query functions
- [x] **Module 2.52** - Data upload interface
- [x] **Module 2.58** - Automated data pipeline
- [x] **Module 3.10** - Development environment setup ✅ **JUST COMPLETED**
- [x] **Module 3.11** - GitHub workflow setup ✅ **JUST COMPLETED**

---

## 🎯 Sprint 2: AI Application Development with RAG

### **Phase 1: Foundation (Weeks 1-2)**

#### - [x] **Module 3.12 - LLM API Access** ✅ **JUST COMPLETED**
**What:** Make first working call to OpenAI API
**Files to create:**
- `config/llm_config.py` - API client configuration
- `utils/llm_client.py` - OpenAI API wrapper
- `tests/test_llm_connection.py` - API connection tests

**Action items:**
1. Add `openai` to requirements.txt
2. Add `OPENAI_API_KEY` to `.env`
3. Create basic completion function
4. Test with simple prompt

---

#### - [x] **Module 3.13 - Prompt Construction** ✅ **JUST COMPLETED**
**What:** Structure prompts with system/user roles
**Files to create:**
- `prompts/system_prompts.py` - Reusable system messages
- `prompts/user_templates.py` - User prompt templates

**Action items:**
1. Define customer support assistant persona
2. Create prompt templates for churn prediction
3. Test different prompt variations

---

#### - [x] **Module 3.14 - Tokens & Cost Estimation** ✅ **JUST COMPLETED**
**What:** Measure tokens and estimate costs
**Files to create:**
- `utils/token_counter.py` - Token counting utilities
- `utils/cost_tracker.py` - Usage and cost tracking

---

### **Phase 2: Document Processing (Weeks 3-4)**

#### **Module 3.19 - Document Loading**
**What:** Load customer documents (tickets, emails, notes)
**Files to create:**
- `rag/document_loader.py` - Multi-format document loader
- `data/documents/` - Customer interaction documents

**Use cases:**
- Load support ticket threads
- Parse customer email communications
- Extract meeting notes

---

#### **Module 3.21 - Document Chunking**
**What:** Break documents into retrievable chunks
**Files to create:**
- `rag/chunking.py` - Chunking strategies
- `tests/test_chunking.py` - Chunking validation

**Strategy for ChurnGuard:**
- Chunk size: 500 tokens
- Overlap: 50 tokens
- Preserve ticket/email boundaries

---

#### **Module 3.22 - Chunk Metadata**
**What:** Track source information for citations
**Files to create:**
- `rag/metadata_manager.py` - Metadata extraction

**Metadata to track:**
- Customer ID
- Ticket ID
- Date
- Sentiment
- Source type (ticket/email/call)

---

### **Phase 3: Embeddings & Vector Storage (Weeks 5-6)**

#### **Module 3.25-3.26 - Embeddings**
**What:** Generate embeddings for semantic search
**Files to create:**
- `rag/embeddings.py` - Embedding generation
- `rag/similarity.py` - Similarity calculations

**Model:** `text-embedding-3-small`

---

#### **Module 3.30-3.31 - Vector Database**
**What:** Store and index embeddings
**Files to create:**
- `rag/vector_store.py` - Vector DB interface
- `config/vector_config.py` - Chroma/FAISS configuration

**Options:**
- **ChromaDB** (recommended for local dev)
- **FAISS** (fast, in-memory)
- **Pinecone** (production, cloud)

---

#### **Module 3.32-3.33 - Similarity Search**
**What:** Retrieve relevant context
**Files to create:**
- `rag/retriever.py` - Retrieval functions
- `rag/reranker.py` - Re-ranking logic

**Use case:**
- Query: "Why is customer X at risk?"
- Retrieve: Top 5 relevant ticket/interaction chunks

---

### **Phase 4: RAG Pipeline (Weeks 7-8)**

#### **Module 3.37 - RAG Architecture**
**What:** Connect all components
**Files to create:**
- `rag/pipeline.py` - End-to-end RAG flow
- `rag/context_builder.py` - Context assembly

**Flow:**
```
User Query → Embed Query → Retrieve Chunks → 
Build Context → LLM Generation → Return Answer + Citations
```

---

#### **Module 3.38-3.39 - Context Injection**
**What:** Build grounded prompts
**Files to create:**
- `rag/prompt_builder.py` - Context injection
- `prompts/rag_templates.py` - RAG-specific prompts

**Template:**
```
System: You are a customer success analyst. Answer based ONLY on the provided context.

Context:
{retrieved_chunks}

User: {user_query}
```

---

#### **Module 3.40 - Source Citation**
**What:** Make answers verifiable
**Implementation:**
- Return chunk metadata with answers
- Link back to original tickets/emails
- Show confidence scores

---

### **Phase 5: Application Integration (Weeks 9-10)**

#### **Module 3.44 - Backend API**
**What:** Serve RAG over API
**Files to create:**
- `api/rag_endpoints.py` - FastAPI/Flask endpoints
- `api/schemas.py` - Request/response models

**Endpoints:**
```
POST /api/chat - Ask a question
POST /api/upload - Index new document
GET /api/sources/{id} - Get source document
```

---

#### **Module 3.46 - Chat Interface**
**What:** Add RAG chat to Streamlit app
**Files to update:**
- `streamlit_app.py` - Add "AI Assistant" page

**Features:**
- Chat interface
- Source citations display
- Conversation history

---

#### **Module 3.47 - Streaming Responses**
**What:** Real-time response streaming
**Implementation:**
- Use OpenAI streaming API
- Update UI progressively
- Show sources as they're used

---

### **Phase 6: Deployment (Week 11)**

#### **Module 3.49 - Deployment**
**Files to create:**
- `Dockerfile` - Container configuration
- `docker-compose.yml` - Multi-service setup
- `deploy/` - Deployment scripts

**Services:**
- Streamlit app
- Vector database
- API backend (if separate)

---

## 📦 New Dependencies (Sprint 2)

```txt
# LLM & Embeddings
openai>=1.0.0
tiktoken>=0.5.0

# Vector Database
chromadb>=0.4.0
# OR faiss-cpu>=1.7.0

# Document Processing
pypdf>=3.0.0
python-docx>=1.0.0
beautifulsoup4>=4.12.0

# API Framework (if building separate API)
fastapi>=0.104.0
uvicorn>=0.24.0

# Utilities
python-dotenv>=1.0.0  # Already have
tenacity>=8.2.0  # For retries
```

---

## 🗂️ Proposed Directory Structure (Sprint 2)

```
S84_ChurnGuards_PredictCare/
│
├── rag/                          # RAG components
│   ├── __init__.py
│   ├── document_loader.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── pipeline.py
│   └── context_builder.py
│
├── prompts/                      # Prompt templates
│   ├── system_prompts.py
│   ├── user_templates.py
│   └── rag_templates.py
│
├── api/                          # API layer (optional)
│   ├── rag_endpoints.py
│   └── schemas.py
│
├── config/                       # Configuration
│   ├── llm_config.py
│   └── vector_config.py
│
├── utils/                        # Utilities
│   ├── llm_client.py
│   ├── token_counter.py
│   └── cost_tracker.py
│
├── data/
│   └── documents/                # Customer documents for RAG
│
├── vector_store/                 # Vector DB storage (gitignored)
│
├── tests/
│   ├── test_llm_connection.py
│   ├── test_chunking.py
│   ├── test_embeddings.py
│   └── test_rag_pipeline.py
│
└── streamlit_app.py              # Updated with RAG chat page
```

---

## 🎯 Immediate Next Steps

### **This Week (Module 3.12)**
1. **Add OpenAI dependency**
   ```bash
   pip install openai tiktoken python-dotenv
   pip freeze > requirements.txt
   ```

2. **Create LLM configuration**
   - Create `config/llm_config.py`
   - Add API key to `.env`
   - Test connection

3. **First completion call**
   - Create simple test script
   - Verify API access
   - Measure token usage

---

## 📊 Success Metrics

**By End of Sprint 2:**
- [ ] RAG pipeline retrieving relevant customer context
- [ ] Chat interface answering questions about customers
- [ ] Source citations linking back to original tickets/emails
- [ ] Deployed and accessible to team
- [ ] <$50 spent on API costs during development

---

## 🔒 Security Checklist

- [x] `.env` file never committed
- [x] `.env.example` template created
- [x] API keys stored securely
- [ ] Vector store data gitignored
- [ ] Rate limiting implemented
- [x] Cost monitoring active

---

## 👥 Team Responsibilities

**Week-by-week rotation:**
- **Week 1-2:** Foundation & LLM setup
- **Week 3-4:** Document processing
- **Week 5-6:** Embeddings & vector DB
- **Week 7-8:** RAG pipeline
- **Week 9-10:** Application integration
- **Week 11:** Deployment & polish

---

**Status:** 🟢 Ready to start Sprint 2  
**Next Module:** 3.12 - LLM API Access  
**Estimated Duration:** 11 weeks  
**Team:** Akshit Sharma, Arman Singh, Saksham Kaushal
