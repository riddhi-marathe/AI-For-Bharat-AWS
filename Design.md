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
