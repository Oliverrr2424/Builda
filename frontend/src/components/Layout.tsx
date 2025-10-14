import Head from 'next/head'
import { PropsWithChildren } from 'react'

interface LayoutProps {
  title?: string
  description?: string
}

export function Layout({
  title = 'Builda - PC Build Assistant',
  description = 'Next.js frontend + FastAPI backend starter',
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
              <p className="layout-subtitle">React + FastAPI PC build recommendation platform</p>
            </div>
            <div className="layout-tech-stack">
              <span>LLM-powered build planning</span>
              <span>RAG retrieval and compatibility validation</span>
            </div>
          </div>
        </header>
        <main className="layout-main">{children}</main>
      </div>
    </>
  )
}
