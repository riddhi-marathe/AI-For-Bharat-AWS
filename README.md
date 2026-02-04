# AI-For-Bharat-AWS

**LearnFlow AI Empowering Developers to Bridge the Gap Between Documentation and Mastery**

**📖 Overview**

LearnFlow AI is an intelligent developer productivity ecosystem designed to eliminate "tutorial hell" and documentation fatigue. By leveraging Retrieval-Augmented Generation (RAG) and adaptive learning paths, LearnFlow AI transforms static technical information into personalized, interactive skill-building journeys.

Whether you are a student navigating complex data structures or a senior dev mastering a new framework, LearnFlow AI streamlines your workflow by providing context-aware explanations and roadmap generation.

**🚀 Key Features**

**Adaptive Roadmapping**:  Generates dynamic learning paths based on your current GitHub repository history and skill gaps.

**Contextual ELI5** :  Translates complex codebases and "dry" documentation into simplified, digestible concepts using LLMs.

**Interactive Knowledge Graphs**:  Visualizes the hierarchy of technical concepts, showing how languages and frameworks interconnect.

**RAG-Powered Tutor**:  Query specific local repositories or live documentation URLs for instant, grounded technical answers.

**Developer Flow Mode**:  A minimalist interface designed to minimize cognitive load and prevent context switching.

**🛠 Tech Stack**
**Frontend**: Next.js 14 (App Router), Tailwind CSS, Framer Motion.

**Backend**: FastAPI (Python), Pydantic.

**Orchestration**: LangChain / LlamaIndex.

**Intelligence**: GPT-4o / Claude 3.5 Sonnet / Llama-3 (via Groq).Vector Store: ChromaDB or Pinecone.

**Visualizations**: D3.js / React Flow.

**📂 Project Structure**

Plaintext

├── .github/             # CI/CD Workflows & Issue Templates

├── src/

│   ├── api/             # FastAPI backend logic & AI Agents

│   ├── web/             # Next.js frontend application

│   ├── engine/          # RAG pipelines & Embedding logic

│   └── scripts/         # Data ingestion and preprocessing

├── data/                # Sample datasets & Knowledge base

├── tests/               # Unit and Integration tests

├── .env.example         # Environment variable templates

├── requirements.txt     # Python dependencies

└── README.md

**⚡ Quick Start**
Prerequisites

Python 3.10+

Node.js 18+

API Keys for OpenAI or Anthropic1. 



