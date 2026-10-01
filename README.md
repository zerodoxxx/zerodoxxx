## Hi, I'm Nehul

I build LLM systems that have to hold up in production: retrieval, multi-agent workflows, and the data pipelines underneath them.

ML Engineer II at **Revionics** in Bengaluru. Before that, ML at **Coinbase** and engineering at **Goldman Sachs**. Co-author of **[SocialPulse](https://arxiv.org/abs/2602.07248)** (ICWSM 2026).

[LinkedIn](https://linkedin.com/in/nehulbhatnagar) · [Email](mailto:nbhatnagar3010@gmail.com) · [Paper](https://arxiv.org/abs/2602.07248)

&nbsp;

### Side projects

**[ai-usage-dashboard](https://github.com/zerodoxxx/ai-usage-dashboard)**\
A local dashboard for what my AI coding tools actually use and cost. It reads Claude Code, Codex and Antigravity session logs straight off disk (no API keys, nothing uploaded) and breaks spend down by model, session and hour, including cache hit rates and how much caching saved.\
<sub>Python · Chart.js</sub>

**[Quorum](https://github.com/zerodoxxx/Quorum)** · 🔒 private repo\
One prompt, sent to several LLMs at once. Quorum compares their answers, scores how much they agree, pulls out the specific claims where they contradict each other, and writes one consolidated response. It's a personal tool that only my friends and I use, so the repo stays private.\
<sub>Python · FastAPI · LangGraph · OpenRouter</sub>

**[my-own-claude-code](https://github.com/zerodoxxx/my-own-claude-code)**\
Building a coding agent from scratch through the CodeCrafters challenge: the agent loop, tool calling, and file and shell tools.\
<sub>Python</sub>

&nbsp;

### Work

**Revionics** · ML Engineer II · 2023 to now
- Built an enterprise RAG system over internal help docs and client documents. Ticket resolution time dropped 70%+.
- Led technical design of a multi-agent LLM pricing platform: prompt strategy, evals, and the FastAPI workflow engine behind it.
- Built and containerized a REST API on Kubernetes, cutting latency 80%+ and saving $100k+ a year in compute.
- Entity resolution with a Siamese network (triplet loss) and Leiden clustering, replacing 95%+ of manual record linkage.
- Wrote VAT-aware forecasting libraries that opened up $2M+ in new European revenue.

**Coinbase** · ML Engineering Intern · 2023
- Near-real-time pipeline that pulls crypto market narratives out of social media: 15k+ tweets an hour through Airflow, with BERTopic and LLM embeddings for topic detection.

**Goldman Sachs** · Summer Analyst, Engineering · 2022
- Rewrote a Kafka trade-data pipeline (6M+ messages, 60GB+ per run) around multiprocessing. Runtime went from 14 hours to under 2.

&nbsp;

### Research

**[SocialPulse: An Open-Source Subreddit Sensemaking Toolkit](https://arxiv.org/abs/2602.07248)** · ICWSM 2026\
I built the NLP and generative-AI modules that turn raw subreddit threads into structured topic and community analytics.

&nbsp;

### Tools I reach for

**ML / LLMs** PyTorch, scikit-learn, RAG, multi-agent systems, FAISS, Pinecone, BERTopic\
**Backend** Python, FastAPI, Docker, Kubernetes (EKS/GKE), SQL\
**Data** Kafka, Airflow, Spark, Databricks, Snowflake, BigQuery, MongoDB
