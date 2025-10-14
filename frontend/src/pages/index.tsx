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
          <h1>Builda 智能装机工作台</h1>
          <p>
            结合 RAG 检索与 LLM 规划的装机顾问，提供兼容性校验、价格历史与备选方案。
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
          <h3>规划流程</h3>
          <ul>
            <li>意图解析：抽取预算、场景、品牌偏好</li>
            <li>候选召回：pgvector + Redis 缓存高效检索</li>
            <li>组装校验：规则层校对功耗与兼容性</li>
            <li>LLM 生成：主/备方案、说明与价格时间戳</li>
          </ul>
        </div>
        <div>
          <h3>接入准备</h3>
          <ul>
            <li>Playwright/Scrapy 抓取多渠道 SKU 数据</li>
            <li>PostgreSQL + pgvector 存储规格与嵌入</li>
            <li>Redis 处理会话、缓存与频控</li>
            <li>OpenAI / Azure OpenAI API 密钥保存在 .env</li>
          </ul>
        </div>
      </section>
    </Layout>
  )
}
