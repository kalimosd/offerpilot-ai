"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ChatMessage } from "@/components/chat-message";
import { fetchSSE, uploadFile } from "@/lib/api";
import { useChatMessages, Message } from "@/lib/chat-context";

export default function ChatPage() {
  const { messages, setMessages } = useChatMessages();
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo(0, scrollRef.current.scrollHeight);
  }, [messages]);

  async function handleSend() {
    const text = input.trim();
    if (!text || loading) return;
    setInput("");
    setLoading(true);

    const userMsg: Message = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);

    const history = messages
      .filter((m) => m.role !== "tool")
      .map((m) => ({ role: m.role, content: m.content }));

    let assistantContent = "";
    setMessages((prev) => [...prev, { role: "assistant", content: "..." }]);

    await fetchSSE(text, history, (event, data: unknown) => {
      const d = data as Record<string, string>;
      if (event === "token") {
        assistantContent += d.content || "";
        setMessages((prev) => {
          const next = [...prev];
          next[next.length - 1] = { role: "assistant", content: assistantContent };
          return next;
        });
      } else if (event === "tool_call") {
        setMessages((prev) => [
          ...prev,
          { role: "tool", content: `${d.name}(${JSON.stringify(d.args)})`, toolName: d.name },
        ]);
      } else if (event === "tool_result") {
        setMessages((prev) => [
          ...prev,
          { role: "tool", content: d.result || "", toolName: d.name },
        ]);
      }
    });

    setLoading(false);
  }

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const target = file.name.toLowerCase().includes("jd") ? "jds" : "root";
    const res = await uploadFile(file, target);
    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: `📎 已上传: ${res.path} (${(res.size / 1024).toFixed(1)} KB)` },
    ]);
    if (fileRef.current) fileRef.current.value = "";
  }

  return (
    <div className="flex flex-col h-full">
      <div className="border-b border-zinc-200 px-6 py-3">
        <h1 className="text-sm font-semibold">OfferPilot Chat</h1>
      </div>

      <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-4">
        {messages.length === 0 && (
          <div className="text-center text-zinc-400 mt-20">
            <p className="text-2xl mb-2">💼</p>
            <p className="text-sm">输入任务开始，或上传简历/JD 文件</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <ChatMessage key={i} msg={msg} />
        ))}
      </div>

      <div className="border-t border-zinc-200 px-6 py-3">
        <div className="flex gap-2 items-end">
          <input ref={fileRef} type="file" className="hidden" onChange={handleUpload} accept=".md,.pdf,.docx,.txt,.yaml,.yml" />
          <Button variant="outline" size="sm" onClick={() => fileRef.current?.click()} className="shrink-0">
            📎
          </Button>
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); } }}
            placeholder="输入任务... (Enter 发送, Shift+Enter 换行)"
            className="min-h-[40px] max-h-[120px] resize-none text-sm"
            rows={1}
          />
          <Button onClick={handleSend} disabled={loading || !input.trim()} size="sm" className="shrink-0">
            {loading ? "⏳" : "发送"}
          </Button>
        </div>
      </div>
    </div>
  );
}
