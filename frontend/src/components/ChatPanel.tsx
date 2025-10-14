import { FormEvent, useState } from 'react'
import { useApiMutation } from '../hooks/useApi'
import { useChatStore } from '../store/chatStore'
import type { ChatPlanResponse } from '../types/chat'

interface ChatPanelProps {
  onPlanReceived: (plan: ChatPlanResponse) => void
}

export function ChatPanel({ onPlanReceived }: ChatPanelProps) {
  const { messages, addMessage } = useChatStore()
  const [input, setInput] = useState('')

  const mutation = useApiMutation<ChatPlanResponse, {
    messages: { role: string; content: string }[]
    budget?: number
    currency?: string
  }>('/chat/plan')

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!input.trim()) return

    const newMessage = { role: 'user' as const, content: input.trim() }
    addMessage(newMessage)
    setInput('')

    const payload = {
      messages: [...messages, newMessage].map((message) => ({
        role: message.role,
        content: message.content,
      })),
      currency: 'CNY',
    }

    try {
      const plan = await mutation.mutateAsync(payload)
      onPlanReceived(plan)
      addMessage({
        role: 'assistant',
        content: '这是基于当前需求生成的装机建议，详情见右侧方案卡片。',
      })
    } catch (error) {
      addMessage({
        role: 'assistant',
        content: error instanceof Error ? error.message : '生成方案失败，请稍后重试。',
      })
    }
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>对话</h2>
        <span className="panel-subtitle">描述你的使用场景与预算</span>
      </div>
      <div className="chat-window">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-bubble ${message.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'}`}
          >
            <span className="chat-role">{message.role === 'user' ? '你' : 'Builda'}</span>
            <p>{message.content}</p>
          </div>
        ))}
        {mutation.isPending && (
          <div className="chat-bubble chat-bubble-assistant">
            <span className="chat-role">Builda</span>
            <p>正在根据你的需求生成方案...</p>
          </div>
        )}
      </div>
      <form className="chat-form" onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="例如：预算 1.2 万元，希望畅玩 2K 游戏并兼顾视频剪辑"
          rows={3}
        />
        <button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? '生成中...' : '发送'}
        </button>
      </form>
    </div>
  )
}
