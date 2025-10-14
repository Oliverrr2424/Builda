import { create } from 'zustand'

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

interface ChatState {
  messages: ChatMessage[]
  addMessage: (message: ChatMessage) => void
  reset: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [
    {
      role: 'assistant',
      content: '你好，我是你的装机顾问。告诉我预算和用途，我来推荐配置！',
    },
  ],
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, message],
    })),
  reset: () =>
    set({
      messages: [
        {
          role: 'assistant',
          content: '你好，我是你的装机顾问。告诉我预算和用途，我来推荐配置！',
        },
      ],
    }),
}))
