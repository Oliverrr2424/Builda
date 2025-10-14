# System Architecture Plan

Note: All languages used during development should be English.

## I. Overall Architecture

- **Web Frontend**: React + Next.js (supports SSR/SSG, balances SEO and performance)
- **Backend Services**: Python (FastAPI)
- **Database**: PostgreSQL with pgvector for semantic search
- **Cache**: Redis (session management, RAG retrieval cache, rate limiting)
- **Data Ingestion**: Playwright / Scrapy + scheduled jobs (GitHub Actions or AWS EventBridge)
- **LLM Gateway**: Prefer OpenAI GPT-4; alternatives Azure OpenAI (enterprise compliance) or AWS Bedrock (Claude/Llama)
- **Object Storage / CDN**: Amazon S3 + CloudFront (or Cloudflare)
- **Observability / Logs**: OpenTelemetry + Grafana/Prometheus (or Datadog)
- **Auth**: Auth0 / Clerk (or AWS Cognito)
- **CI/CD**: GitHub Actions (test, build, deploy)

> Note: GPT-4 is not currently available on AWS Bedrock. If GPT-4 is required, choose OpenAI or Azure OpenAI. For compliance-first scenarios, Azure OpenAI is recommended as primary and OpenAI as backup. If you must stay in the AWS ecosystem, consider Claude series on Bedrock.

## II. Data: Collection and Modeling

### 2.1 Data Sources and Update Strategy
- **BestBuy**: Official API (Products/Reviews), fetch categories by `categoryPath.id`.
- **Amazon**: Product Advertising API, fetch details and prices by ASIN; display must include source attribution.
- **Newegg**: No public API; use Playwright (Headless Chromium) + rotating proxies + random waits; honor robots.txt and TOS; only scrape public specs and prices.

**Refresh cadence**
- Full scan every two days to detect new SKUs, delistings, or major price changes.
- Daily calibration of price and stock for high-demand or recommended SKUs.

**Compliance and anti-bot**
- Rate limiting, distributed proxies, exponential backoff on retries.
- Mask sensitive fields; strictly label sources and price timestamps.

### 2.2 Database Design

Centered around PostgreSQL + pgvector. The main table `products` stores common attributes; per-category tables split by type (e.g., `cpus`, `gpus`).

Key fields:
- `products`: `id`, `global_sku`, title, brand, category, source, price, stock, rating, `spec_json`, `scene_tags`, `perf_score`, `updated_at`.
- Per-category tables: CPU (socket, cores/threads, base/boost frequency, TDP), GPU (chip, VRAM, TDP, length), etc.
- `product_prices`: price history.
- `build_templates` / `build_template_items`: preset build templates.
- `dialogs`: conversations, parsed results, and recommended answers.
- `embeddings_*`: vector representations for products and plans using `pgvector`.

Indexing includes a composite index on `products(category, price, perf_score, scene_tags)` and `pgvector`'s `ivfflat`.

## III. AI: RAG Flow and Prompt Engineering

### 3.1 Main Flow
1. **Intent parsing**: Use small models or rules to extract scenario, budget, brand preferences, size requirements, software/games, etc.
2. **Candidate recall**: Embed the requirement text and retrieve K candidates from `embeddings_products` and `embeddings_cases`; filter by price, scenario tags, performance score, and spec compatibility.
3. **Assembler**: Python rules layer enforces compatibility (socket, memory type, case size, PSU headroom, etc.), prioritizing performance thresholds within budget.
4. **LLM decisioning**: Provide candidate list and constraints to the LLM to generate the primary plan, alternatives, explanations, and notes.
5. **Output**: Structured configuration JSON, conversational copy, price validity period, and source links.

### 3.2 Model Selection and Routing
- Primary generation: GPT-4 (OpenAI or Azure OpenAI).
- Lightweight parsing/classification: gpt-4o-mini, gpt-3.5-turbo, or a fine-tuned Llama-3-8B.
- All-AWS option: Claude 3 on Bedrock instead of GPT-4; Cohere Embed instead of OpenAI Embedding.
- Embedding: OpenAI `text-embedding-3-large`; self-host `nomic-embed-text` if necessary.
- Expose FastAPI tool functions with Function Calling.

### 3.3 Key Prompt Templates
- **System Prompt**: Set the role of a "senior PC build consultant"; emphasize real data, compatibility, explanations, and alternatives.
- **Planner Prompt**: Hidden chain-of-thought; analyze scenarios, budget allocation, and constraint checks.
- **Generator Prompt**: Input candidate JSON and constraints; output a structured result including primary plan, total price, alternatives, and notes.

### 3.4 Cost and Performance Optimization
- Prompt prefix caching, conversation summarization, RAG-first strategy.
- User rate limiting, concurrency pools, graceful degradation (GPT-4 → GPT-3.5/Claude).
- Monitor recommendation success rate, user modification count, and click-through conversions.

## IV. Backend API Contract (FastAPI)

- `POST /api/chat/plan`: Return a build plan, total price, alternatives, notes, and price timestamps based on the conversation.
- `GET /api/products/search`: Query products by keyword, category, price range, and scenario.
- `POST /api/builds/validate`: Validate compatibility, power consumption, and PSU recommendations.
- `GET /api/price/history`: Return price history for a given product.
- `POST /api/feedback`: Record user feedback, reasons for modification, and purchase status.

Authentication uses JWT (Auth0/Clerk). Guests have access to limited features only.

## V. Frontend Implementation Notes (Next.js)

- Main chat view combines message stream with configuration cards.
- Configuration cards show component grid, total price, source links, and alternative toggles.
- Optional filters: budget slider, scenario quick buttons, case size preferences.
- One-click copy list, export PDF; support streaming output, optimistic UI, and error tips.
- State management: Zustand or Redux Toolkit; data layer uses SWR/React Query.
- Mobile adaptation, internationalization (EN/zh), currency and measurement localization.
- Analytics: track question → plan → external link click → favorite funnel.

## VI. Data Sync and Cleaning

- Scheduling: GitHub Actions/cron (UTC 3:00) triggers containerized sync jobs.
- Pipeline: crawl → spec extraction → normalization → performance scoring → tag annotation → storage.
- Quality: dirty data detection, deduplication (`global_sku` unified rules).
- Compliance: store only factual specs and prices; keep original image URLs or licensed thumbnails.

## VII. Monitoring, Observability, and Security

- API metrics: P95 latency, error rate, LLM time, and token cost.
- Data metrics: crawler success rate, SKU coverage, price update ratio.
- Business metrics: recommendation revision rate, external click-through rate, return rate.
- Alerts: spikes in LLM errors, price updates older than 48h, high compatibility failure rate.
- Security: HTTPS, CSP, dependency vulnerability scans, rate limiting, WAF, secret management (Secrets Manager/Parameter Store), least privilege.

## VIII. Milestones (10–12 weeks)

- **Sprint 1 (Weeks 1–2)**: Next.js + FastAPI scaffolding, auth, Postgres/Redis basics, minimal chat flow.
- **Sprint 2 (Weeks 3–4)**: Data ingestion and cleaning, pgvector indexing, retrieval API.
- **Sprint 3 (Weeks 5–6)**: Full RAG pipeline, compatibility validation, frontend configuration cards.
- **Sprint 4 (Weeks 7–8)**: Prompt optimization, caching, logging/observability, A/B testing, multi-language.
- **Sprint 5 (Weeks 9–10)**: SEO, price history chart, compliance audit, canary/beta.
- **Sprint 6 (Weeks 11–12)**: Performance testing, risk control, bug fixes, launch preparation.

## IX. MVP Acceptance Criteria

- For repeated identical requirements, return compatible and purchasable plans in >90% of cases.
- Price timestamps ≤ 48 hours; daily update hit rate ≥ 85% for hot SKUs.
- First-token latency ≤ 2 seconds; full answer ≤ 8 seconds (when RAG hits).
- Users need to modify no more than two items to meet requirements.
- All products include source backlinks and compliance statements.

## X. Rollout Checklist

- Docker Compose environment (web/api/db/redis/worker).
- Frontend deps: `next`, `react`, `react-query`, `zustand`, `tailwindcss`, `framer-motion`.
- Backend deps: `fastapi`, `pydantic`, `uvicorn`, `httpx`, `sqlalchemy`, `asyncpg`, `pgvector`, `redis`, `tenacity`.
- Crawler deps: `playwright`, `scrapy`, `selectolax`.
- AI deps: `openai` (or `azure-ai-inference`/`anthropic`), `sentence-transformers`/`nomic`.
- Prompts and API contracts follow this document.
- Apply for BestBuy/PA-API keys; prepare proxy pool and compliance templates.
- Use Jira/Linear to break milestones into Stories and acceptance criteria.

## Recommended Models and Vendor Mix

- **Primary**: Azure OpenAI - GPT-4 (enterprise compliance and stability).
- **Alternative**: OpenAI direct (degrade/scale), Claude 3 on AWS Bedrock (for all-AWS option).
- **Embedding**: OpenAI `text-embedding-3-large` with pgvector; switch to self-hosted at scale.

## Environment Variables

Adjust model vendors, versions, or runtime environment variables as needed to match the best development experience.
