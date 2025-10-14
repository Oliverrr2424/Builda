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
    <div className="panel">
      <div className="panel-header">
        <h2>Chat</h2>
        <span className="panel-subtitle">Describe your use case and budget</span>
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
        <button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? 'Generating...' : 'Send'}
        </button>
      </form>
    </div>
  )
}
