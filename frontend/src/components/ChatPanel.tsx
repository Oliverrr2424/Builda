import { FormEvent, useCallback, useEffect, useRef, useState } from 'react'
import { useApiMutation } from '../hooks/useApi'
import { useChatStore } from '../store/chatStore'
import type { ChatPlanResponse } from '../types/chat'

interface ChatPanelProps {
  onPlanReceived: (plan: ChatPlanResponse) => void
}

type StepStatus = 'idle' | 'active' | 'complete' | 'error'

const PROGRESS_STEPS = [
  'Confirming requirements',
  'Querying product database',
  'Checking compatibility',
  'Finalizing configuration',
]

export function ChatPanel({ onPlanReceived }: ChatPanelProps) {
  const { messages, addMessage } = useChatStore()
  const [input, setInput] = useState('')
  const [stepStatuses, setStepStatuses] = useState<StepStatus[]>(() => PROGRESS_STEPS.map(() => 'idle'))
  const timersRef = useRef<number[]>([])

  const quickPrompts = [
    {
      label: 'Creator workstation · $2200',
      content: 'Budget 2200 USD, need buttery-smooth 4K video editing with a quiet case and two 27-inch monitors.',
    },
    {
      label: 'Flagship gaming · $2500',
      content: 'Budget 2500 USD, want smooth 4K AAA gaming with ray tracing and Wi-Fi 7.',
    },
    {
      label: 'Compact AI rig · $1400',
      content: 'Budget 1400 USD, prefer a mini-ITX build that balances AI image generation and everyday productivity.',
    },
  ]

  const clearTimers = useCallback(() => {
    timersRef.current.forEach((timer) => window.clearTimeout(timer))
    timersRef.current = []
  }, [])

  const startProgress = useCallback(() => {
    clearTimers()
    setStepStatuses(PROGRESS_STEPS.map((_, index) => (index === 0 ? 'active' : 'idle')))
    PROGRESS_STEPS.slice(1).forEach((_, index) => {
      const timer = window.setTimeout(() => {
        setStepStatuses((current) =>
          current.map((status, statusIndex) => {
            if (statusIndex < index + 1) {
              return 'complete'
            }
            if (statusIndex === index + 1) {
              return 'active'
            }
            return status
          }),
        )
      }, (index + 1) * 1200)
      timersRef.current.push(timer)
    })
  }, [clearTimers])

  const completeProgress = useCallback(() => {
    clearTimers()
    setStepStatuses(PROGRESS_STEPS.map(() => 'complete'))
  }, [clearTimers])

  const failProgress = useCallback(() => {
    clearTimers()
    setStepStatuses(PROGRESS_STEPS.map((_, index) => (index < PROGRESS_STEPS.length - 1 ? 'complete' : 'error')))
  }, [clearTimers])

  useEffect(() => () => clearTimers(), [clearTimers])

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
    startProgress()

    const payload = {
      messages: [...messages, newMessage].map((message) => ({
        role: message.role,
        content: message.content,
      })),
      currency: 'USD',
    }

    try {
      const plan = await mutation.mutateAsync(payload)
      onPlanReceived(plan)
      addMessage({
        role: 'assistant',
        content: 'Here is a build suggestion based on your needs. See the plan card on the right for details.',
      })
      completeProgress()
    } catch (error) {
      failProgress()
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
      <div className="progress-steps">
        {PROGRESS_STEPS.map((step, index) => (
          <div key={step} className="progress-step" data-status={stepStatuses[index]}>
            <span className="progress-step-indicator" aria-hidden="true" />
            <span>{step}</span>
          </div>
        ))}
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
