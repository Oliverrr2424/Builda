import Head from 'next/head'
import { PropsWithChildren } from 'react'

interface LayoutProps {
  title?: string
  description?: string
}

export function Layout({
  title = 'Builda - 智能装机顾问',
  description = 'Next.js 前端 + FastAPI 后端基础框架',
  children,
}: PropsWithChildren<LayoutProps>) {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="description" content={description} />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className="layout-root">
        <header className="layout-header">
          <div className="layout-header-content">
            <div>
              <span className="layout-brand">Builda</span>
              <p className="layout-subtitle">React + FastAPI 装机推荐平台</p>
            </div>
            <div className="layout-tech-stack">
              <span>LLM 驱动的装机规划</span>
              <span>RAG 检索与兼容性校验</span>
            </div>
          </div>
        </header>
        <main className="layout-main">{children}</main>
      </div>
    </>
  )
}
