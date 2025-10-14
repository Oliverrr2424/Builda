import { useState, useEffect } from 'react'
import Head from 'next/head'

export default function Home() {
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  const fetchData = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/hello')
      const data = await response.json()
      setMessage(data.message)
    } catch (error) {
      setMessage('连接后端失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  return (
    <div>
      <Head>
        <title>Builda - React + FastAPI</title>
        <meta name="description" content="React Next.js 前端 + Python FastAPI 后端" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container">
        <h1 className="title">
          欢迎使用 <span className="highlight">Builda</span>
        </h1>
        
        <p className="description">
          React + Next.js 前端 + Python FastAPI 后端
        </p>

        <div className="api-section">
          <h2>API 测试</h2>
          <button 
            className="button" 
            onClick={fetchData}
            disabled={loading}
          >
            {loading ? '加载中...' : '测试后端连接'}
          </button>
          
          {message && (
            <div className="message">
              <strong>后端响应:</strong> {message}
            </div>
          )}
        </div>

        <div className="grid">
          <div className="card">
            <h3>前端技术栈</h3>
            <ul>
              <li>React 18</li>
              <li>Next.js 14</li>
              <li>TypeScript</li>
              <li>CSS Modules</li>
            </ul>
          </div>

          <div className="card">
            <h3>后端技术栈</h3>
            <ul>
              <li>Python 3.11+</li>
              <li>FastAPI</li>
              <li>Uvicorn</li>
              <li>Pydantic</li>
            </ul>
          </div>
        </div>
      </main>
    </div>
  )
}
