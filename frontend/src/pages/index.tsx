import { useState } from 'react'

import { ChatPanel } from '../components/ChatPanel'
import { Layout } from '../components/Layout'
import { PlanPreview } from '../components/PlanPreview'
import type { ChatPlanResponse } from '../types/chat'

export default function Home() {
  const [plan, setPlan] = useState<ChatPlanResponse | null>(null)

  return (
    <Layout>
      <section className="page-hero" id="workflow">
        <span className="hero-eyebrow">Powered by Gemini 1.5 Pro</span>
        <h1>Compose your dream workstation with a calm, Apple-inspired flow.</h1>
        <p>
          Builda orchestrates crawling, vector indexing, and Gemini planning into a single glassmorphic workspace. Describe your
          scenario, and the assistant drafts balanced builds with alternatives and sourcing hints.
        </p>
        <div className="hero-badges">
          <span>Gemini planning gateway</span>
          <span>Newegg · CanadaComputers crawler samples</span>
          <span>Deterministic vector search bootstrap</span>
        </div>
      </section>

      <div className="layout-grid">
        <ChatPanel onPlanReceived={setPlan} />
        <PlanPreview plan={plan} />
      </div>

      <section className="feature-grid" id="features">
        <div>
          <h3>End-to-end workflow</h3>
          <ul>
            <li>Gemini orchestration with graceful fallback to curated sample plan</li>
            <li>Async crawler facades for Newegg &amp; Canada Computers product payloads</li>
            <li>Hashed embedding vector store with cosine ranking for SKU recall</li>
            <li>FastAPI surface for refreshing crawlers and streaming plan updates</li>
          </ul>
        </div>
        <div>
          <h3>Ready for production hardening</h3>
          <ul>
            <li>Env-configured Gemini API key management via pydantic settings</li>
            <li>Composable pipeline service to extend with real Playwright jobs</li>
            <li>Next.js interface styled with glass, subtle depth, and tactile controls</li>
            <li>Vector search endpoint powering Apple-like instant filtering</li>
          </ul>
        </div>
      </section>
    </Layout>
  )
}
