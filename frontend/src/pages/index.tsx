import { useState } from 'react'

import { ChatPanel } from '../components/ChatPanel'
import { Layout } from '../components/Layout'
import { PlanPreview } from '../components/PlanPreview'
import type { ChatPlanResponse } from '../types/chat'

export default function Home() {
  const [plan, setPlan] = useState<ChatPlanResponse | null>(null)

  return (
    <Layout>
      <section className="page-hero">
        <div>
          <h1>Builda PC Building Workbench</h1>
          <p>
            A PC building assistant powered by RAG retrieval and LLM planning, with compatibility checks, price history, and alternatives.
          </p>
        </div>
        <div className="hero-meta">
          <span>FastAPI · PostgreSQL · Redis · pgvector</span>
          <span>Next.js · React Query · Zustand</span>
        </div>
      </section>

      <div className="layout-grid">
        <ChatPanel onPlanReceived={setPlan} />
        <PlanPreview plan={plan} />
      </div>

      <section className="feature-grid">
        <div>
          <h3>Planning Flow</h3>
          <ul>
            <li>Intent parsing: extract budget, scenario, brand preferences</li>
            <li>Candidate recall: pgvector + Redis cache for efficient retrieval</li>
            <li>Assembly validation: rule layer checks power and compatibility</li>
            <li>LLM generation: primary/alternative plans, notes, and price timestamps</li>
          </ul>
        </div>
        <div>
          <h3>Integration Prep</h3>
          <ul>
            <li>Playwright/Scrapy to crawl multi-channel SKU data</li>
            <li>PostgreSQL + pgvector for specs and embeddings</li>
            <li>Redis for sessions, caching, and rate limiting</li>
            <li>OpenAI / Azure OpenAI API keys stored in .env</li>
          </ul>
        </div>
      </section>
    </Layout>
  )
}
