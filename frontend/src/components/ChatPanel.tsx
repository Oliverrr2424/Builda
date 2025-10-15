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

  const quickPrompts = [
    {
      label: '创作工作站 · ¥15000',
      content: '预算15000人民币，需要4K剪辑和三屏设计，机箱要静音。',
    },
    {
      label: '电竞旗舰 · $2500',
      content: 'Budget 2500 USD, want smooth 4K AAA gaming with ray tracing and Wi-Fi 7.',
    },
    {
      label: '紧凑主机 · ¥8000',
      content: '预算8000人民币，mini-ITX机箱，要兼顾AI绘图和日常办公。',
    },
  ]

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
        content: 'Here is a build suggestion based on your needs. See the plan card on the right for details.',
      })
    } catch (error) {
      addMessage({
        role: 'assistant',
        content: error instanceof Error ? error.message : 'Failed to generate the plan, please try again later.',
      })
    }
  }

  return (
    <div className="panel panel-glass">
      <div className="panel-header">
        <h2>Plan with Builda</h2>
        <span className="panel-subtitle">Describe your workflow. Gemini shapes the configuration.</span>
      </div>
      <div className="prompt-chips">
        {quickPrompts.map((prompt) => (
          <button
            key={prompt.label}
            type="button"
            onClick={() => setInput(prompt.content)}
            disabled={mutation.isPending}
          >
            {prompt.label}
          </button>
        ))}
      </div>
      <div className="chat-window">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-bubble ${message.role === 'user' ? 'chat-bubble-user' : 'chat-bubble-assistant'}`}
          >
            <span className="chat-role">{message.role === 'user' ? 'You' : 'Builda'}</span>
            <p>{message.content}</p>
          </div>
        ))}
        {mutation.isPending && (
          <div className="chat-bubble chat-bubble-assistant">
            <span className="chat-role">Builda</span>
            <p>Generating a plan based on your needs...</p>
          </div>
        )}
      </div>
      <form className="chat-form" onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Example: Budget 1200 USD, want smooth 2K gaming and video editing"
          rows={3}
        />
        <div className="chat-form-footer">
          <span className="chat-form-hint">Enter to send • Shift + Enter for new line</span>
          <button type="submit" disabled={mutation.isPending}>
            {mutation.isPending ? 'Generating…' : 'Send to Gemini'}
          </button>
        </div>
      </form>
    </div>
  )
}
