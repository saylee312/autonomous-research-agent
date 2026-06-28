import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useRef, useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Plus, Send, Trash2, MessageSquare, Loader2, Bot, User } from "lucide-react";
import { toast } from "sonner";
import { api, type ChatMessage, type ChatSession } from "@/lib/api";
import { cn } from "@/lib/utils";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "Chat" },
    ],
  }),
  component: ChatPage,
});

function ChatPage() {
  const qc = useQueryClient();
  const [activeId, setActiveId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);

  const sessionsQ = useQuery({
    queryKey: ["sessions"],
    queryFn: () => api.get<ChatSession[]>("/api/sessions/"),
  });

  const messagesQ = useQuery({
    queryKey: ["session", activeId],
    queryFn: () => api.get<ChatMessage[]>(`/api/sessions/${activeId}`),
    enabled: !!activeId,
  });

  const createSession = useMutation({
    mutationFn: () => api.post<ChatSession>("/api/sessions/"),
    onSuccess: (s) => {
      qc.invalidateQueries({ queryKey: ["sessions"] });
      setActiveId(s._id);
    },
  });

  const deleteSession = useMutation({
    mutationFn: (id: string) => api.del(`/api/sessions/${id}`),
    onSuccess: (_d, id) => {
      qc.invalidateQueries({ queryKey: ["sessions"] });
      if (activeId === id) setActiveId(null);
    },
  });

  const sendMessage = useMutation({
    mutationFn: async (msg: string) => {
      if (!activeId) throw new Error("No active session");
      return api.post<{ response: string }>("/api/chat", { session_id: activeId, message: msg });
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["session", activeId] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  useEffect(() => {
    if (sessionsQ.data && sessionsQ.data.length && !activeId) {
      setActiveId(sessionsQ.data[0]._id);
    }
  }, [sessionsQ.data, activeId]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messagesQ.data, sendMessage.isPending]);

  const handleSend = () => {
    const text = input.trim();
    if (!text) return;
    if (!activeId) {
      createSession.mutate(undefined, {
        onSuccess: () => {
          // submit after creation
          setTimeout(() => {
            sendMessage.mutate(text);
            setInput("");
          }, 50);
        },
      });
      return;
    }
    sendMessage.mutate(text);
    setInput("");
  };

  return (
    <div className="mx-auto w-full max-w-7xl flex-1 px-4 py-6 grid gap-6 md:grid-cols-[280px_1fr] min-h-0">
      {/* Sidebar */}
      <aside className="rounded-xl border border-border bg-card p-3 flex flex-col gap-2 h-[calc(100vh-7rem)]">
        <button
          onClick={() => createSession.mutate()}
          className="flex items-center justify-center gap-2 rounded-lg bg-primary px-3 py-2.5 text-sm font-semibold text-primary-foreground hover:opacity-90 transition"
        >
          <Plus className="size-4" /> New chat
        </button>
        <div className="text-[10px] uppercase tracking-widest text-muted-foreground px-2 pt-2">Sessions</div>
        <div className="flex-1 overflow-y-auto -mr-1 pr-1 space-y-1">
          {sessionsQ.isLoading && <div className="text-xs text-muted-foreground p-2">Loading…</div>}
          {sessionsQ.data?.length === 0 && (
            <div className="text-xs text-muted-foreground p-2">No sessions yet.</div>
          )}
          {sessionsQ.data?.map((s) => (
            <div
              key={s._id}
              className={cn(
                "group flex items-center gap-2 rounded-lg px-2.5 py-2 text-sm cursor-pointer transition",
                activeId === s._id
                  ? "bg-accent text-accent-foreground"
                  : "hover:bg-muted text-muted-foreground"
              )}
              onClick={() => setActiveId(s._id)}
            >
              <MessageSquare className="size-3.5 shrink-0" />
              <span className="truncate font-mono text-[11px]">{s._id.slice(-8)}</span>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  deleteSession.mutate(s._id);
                }}
                className="ml-auto opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive transition"
                aria-label="Delete"
              >
                <Trash2 className="size-3.5" />
              </button>
            </div>
          ))}
        </div>
      </aside>

      {/* Chat area */}
      <section className="rounded-xl border border-border bg-card flex flex-col h-[calc(100vh-7rem)] overflow-hidden">
        <div ref={scrollRef} className="flex-1 overflow-y-auto px-6 py-8 space-y-6">
          {!activeId && (
            <EmptyState
              title="Start a conversation"
              subtitle="Create a new session and ask your research agent anything."
            />
          )}
          {activeId && messagesQ.data?.length === 0 && (
            <EmptyState
              title="Ready when you are"
              subtitle="Send your first message to kick off this session."
            />
          )}
          {messagesQ.data?.map((m, i) => (
            <MessageBubble key={m._id ?? i} role={m.role} content={m.content} />
          ))}
          {sendMessage.isPending && (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="size-4 animate-spin" /> Thinking…
            </div>
          )}
        </div>

        <div className="border-t border-border bg-background/40 p-4">
          <div className="flex items-end gap-2 rounded-xl border border-border bg-background p-2 focus-within:ring-2 focus-within:ring-ring transition">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              rows={1}
              placeholder="Ask anything…"
              className="flex-1 resize-none bg-transparent px-2 py-2 text-sm outline-none placeholder:text-muted-foreground max-h-40"
            />
            <button
              onClick={handleSend}
              disabled={sendMessage.isPending || !input.trim()}
              className="grid size-9 place-items-center rounded-lg bg-primary text-primary-foreground hover:opacity-90 disabled:opacity-40 transition"
            >
              {sendMessage.isPending ? <Loader2 className="size-4 animate-spin" /> : <Send className="size-4" />}
            </button>
          </div>
          <div className="mt-1.5 text-[10px] text-muted-foreground px-1">Enter to send · Shift+Enter for newline</div>
        </div>
      </section>
    </div>
  );
}

function MessageBubble({ role, content }: { role: string; content: string }) {
  const isUser = role === "user";
  return (
    <div className={cn("flex gap-3", isUser && "flex-row-reverse")}>
      <div
        className={cn(
          "grid size-8 place-items-center rounded-lg shrink-0",
          isUser ? "bg-foreground text-background" : "bg-primary text-primary-foreground"
        )}
      >
        {isUser ? <User className="size-4" /> : <Bot className="size-4" />}
      </div>
      <div
        className={cn(
          "max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap",
          isUser
            ? "bg-foreground text-background rounded-tr-sm"
            : "bg-muted text-foreground rounded-tl-sm"
        )}
      >
        {content}
      </div>
    </div>
  );
}

function EmptyState({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="h-full flex flex-col items-center justify-center text-center py-20">
      <div className="grid size-14 place-items-center rounded-2xl bg-primary text-primary-foreground mb-4">
        <Bot className="size-7" />
      </div>
      <h2 className="text-xl font-semibold">{title}</h2>
      <p className="mt-1 text-sm text-muted-foreground max-w-sm">{subtitle}</p>
    </div>
  );
}
