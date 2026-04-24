"use client";

import { createContext, useContext, useState, ReactNode } from "react";

export interface Message {
  role: "user" | "assistant" | "tool";
  content: string;
  toolName?: string;
}

interface ChatContextType {
  messages: Message[];
  setMessages: React.Dispatch<React.SetStateAction<Message[]>>;
}

const ChatContext = createContext<ChatContextType>({ messages: [], setMessages: () => {} });

export function ChatProvider({ children }: { children: ReactNode }) {
  const [messages, setMessages] = useState<Message[]>([]);
  return <ChatContext.Provider value={{ messages, setMessages }}>{children}</ChatContext.Provider>;
}

export function useChatMessages() {
  return useContext(ChatContext);
}
