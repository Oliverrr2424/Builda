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
      content: 'Hello, I am your PC build consultant. Tell me your budget and use case, and I will recommend a configuration!',
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
          content: 'Hello, I am your PC build consultant. Tell me your budget and use case, and I will recommend a configuration!',
        },
      ],
    }),
}))
