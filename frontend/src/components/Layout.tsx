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
          <div className="layout-header-overlay" />
          <div className="layout-header-content">
            <div className="layout-brand-group">
              <span className="layout-brand">Builda Studio</span>
              <p className="layout-subtitle">Gemini-orchestrated PC architecture lab</p>
            </div>
            <nav className="layout-nav">
              <a href="#workflow">Workflow</a>
              <a href="#features">Features</a>
              <a href="https://ai.google.dev/gemini-api" target="_blank" rel="noreferrer">
                Gemini API
              </a>
            </nav>
          </div>
        </header>
        <main className="layout-main">{children}</main>
      </div>
    </>
  )
}
