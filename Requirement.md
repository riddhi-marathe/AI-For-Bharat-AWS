## 📄 REQUIREMENTS


### 1. Functional Requirements (FR)

* **FR1: Automated Roadmap Generation:**   The system shall analyze a user's target topic (e.g., "FastAPI") and generate a step-by-step learning path.
 
* **FR2: Technical Documentation RAG:**   Users must be able to upload a URL or PDF of documentation which the AI uses as a "source of truth" for answering questions.
  
* **FR3: Code Explainer (ELI5):**   The system shall provide a feature to simplify complex code snippets into plain English.
  
* **FR4: Progress Tracking:**   The system shall store and visualize the user’s progress through the generated learning path.
 
* **FR5: Context-Aware Debugging:**   The AI must suggest fixes for code errors while explaining the underlying conceptual mistake.


### 2. Non-Functional Requirements (NFR)

* **NFR1: Latency:**  AI responses for text explanations should be delivered in under 3 seconds.
  
* **NFR2: Accuracy:**  The system must cite specific lines or sections of the documentation to reduce AI "hallucinations."
  
* **NFR3: Scalability:**  The backend should handle concurrent RAG queries using asynchronous processing (FastAPI).
 
* **NFR4: Security:**  All API keys and user-uploaded documentation must be handled securely using environment variables.


### 3. User Personas

* **The Student:**  Needs complex technical jargon simplified and a clear path to follow.
  
* **The Developer:**  Needs to quickly understand a new codebase or library to meet a deadline.

---

## 📄 DESIGN


### 1. System Architecture

LearnFlow AI follows a **Modular Monolith** architecture with a focus on a "Data-Centric" AI pipeline.

* **User Interface:** Built with **React.js/Next.js** for a reactive, state-driven learning experience.
  
* **Orchestration Layer:** **LangChain** acts as the glue between the LLM (Llama-3/GPT-4o) and our Vector Database.
  
* **Vector Engine:** **ChromaDB** is used to store high-dimensional embeddings of technical documentation, enabling "Semantic Search."

### 2. Data Flow

1. **Ingestion:** The user provides a documentation source.
 
2. **Processing:** The text is split into "semantic chunks" and converted into vectors using an embedding model.
 
3. **Retrieval:** When a user asks a question, the system finds the top- most relevant chunks from the vector store.
 
4. **Generation:** The LLM receives the chunks + the user's prompt and generates a grounded, accurate response.

### 3. Database Schema

| Table | Description |

| --- | --- |

| **Users** | Stores profile, name, and skill levels. |

| **Roadmaps** | Stores JSON-structured paths for specific topics. |

| **Documents** | Metadata for uploaded PDFs or scraped URLs. |

| **Analytics** | Tracks time spent on specific modules to optimize future paths. |

### 4. Design Decisions & Trade-offs

* **Why FastAPI?** We chose FastAPI over Django because of its native support for `async` operations, which is critical for handling long-running LLM API calls without blocking the server.
 
* **Why RAG over Fine-tuning?** Fine-tuning is expensive and becomes outdated quickly. RAG allows us to swap documentation in real-time, ensuring the developer always gets the latest information.
