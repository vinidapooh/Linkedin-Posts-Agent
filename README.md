# 🚀 LinkedIn Content Architect Agentic Pipeline

A production-ready Multi-Agent system engineered to automate industry trend analysis and high-engagement professional copy generation. Built using **CrewAI**, **Streamlit**, and integrated with local and cloud infrastructure.

## 🏗️ System Architecture & Data Flow

The system runs as a decoupled state machine utilizing two specialized agent roles:
1. **LinkedIn Trend & Topic Strategist:** Uses search engine APIs (`SerperDevTool`) to ingest live 2026 industry discussions, extracting key terminology banks and high-value technical themes.
2. **Expert Professional Ghostwriter:** ingests processed trends and outputs scannable, mobile-optimized professional prose with strict constraint compliance (zero random hashtags, programmatic white-spacing).

## 🛠️ Tech Stack & Production Decisions
- **Orchestration:** CrewAI (Sequential Process Management for highly dependable text outputs).
- **Frontend / UI:** Streamlit (Pure Python dashboarding for high-velocity deployment).
- **Environment Management:** `uv` (Fast dependency resolution and reproducible environments).
- **Dynamic Compute Routing:**
  - **Local Development:** Pulls context from a local `Ollama` instance running `gemma4:latest` locally on an Apple Silicon cluster.
  - **Cloud Infrastructure:** Automatically switches context when deployed to target instances, routing execution to a cloud-hosted LLM wrapper via `Groq` API endpoints to optimize latency and eliminate cold-start lag.

