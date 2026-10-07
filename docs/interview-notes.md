# Interview talking points

### Why RAG?
The knowledge changes and needs provenance. Fine-tuning is not the right mechanism for frequently updated documents and page-level citations.

### Why page-aware chunks?
Field users need to verify claims. Page metadata makes evidence auditable.

### Why Chroma?
Fast local setup for the take-home. The retrieval interface can be moved to Qdrant/pgvector in production.

### Why refusal?
Commercial hallucinations are more dangerous than unanswered questions. The assistant must not invent distributor margins or schemes.

### What is the real product?
“Retrieval, evidence, citations and safe refusal are the product; the LLM is the language layer.”

### Production next step
Join authenticated user identity with territory/distributor/retailer context and enforce document-level access control before retrieval.
