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


