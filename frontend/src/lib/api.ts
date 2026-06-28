const RAW = (import.meta.env.VITE_API_URL as string | undefined) ?? "http://localhost:8000";
export const API_BASE = RAW.replace(/\/$/, "");

async function handle<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let detail = res.statusText;
    try {
      const j = await res.json();
      detail = j.detail || j.message || detail;
    } catch {
      /* noop */
    }
    throw new Error(detail || `Request failed (${res.status})`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  get: <T>(path: string) => fetch(`${API_BASE}${path}`).then(handle<T>),
  post: <T>(path: string, body?: unknown) =>
    fetch(`${API_BASE}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body ? JSON.stringify(body) : undefined,
    }).then(handle<T>),
  del: <T>(path: string) =>
    fetch(`${API_BASE}${path}`, { method: "DELETE" }).then(handle<T>),
  upload: <T>(path: string, file: File) => {
    const fd = new FormData();
    fd.append("file", file);
    return fetch(`${API_BASE}${path}`, { method: "POST", body: fd }).then(handle<T>);
  },
};

// ---- Types ----
export interface ChatSession {
  _id: string;
  created_at?: string;
}
export interface ChatMessage {
  _id?: string;
  session_id?: string;
  role: "user" | "assistant" | string;
  content: string;
  created_at?: string;
}
export interface ResearchReport {
  _id: string;
  title: string;
  content?: string;
  report_type?: string;
  file_path?: string;
  created_at?: string;
}
export interface RagDocument {
  _id: string;
  filename: string;
  status?: string;
  file_path?: string;
  created_at?: string;
}
