import { createFileRoute } from "@tanstack/react-router";
import { useRef, useState, useEffect } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { FileUp, Loader2, Search, Trash2, FileText, CheckCircle2, AlertCircle } from "lucide-react";
import { toast } from "sonner";
import { api, type RagDocument } from "@/lib/api";

export const Route = createFileRoute("/documents")({
  head: () => ({
    meta: [
      { title: "RAG" },
    ],
  }),
  component: DocumentsPage,
});

interface QueryResult {
  answer?: string;
  response?: string;
  sources?: Array<{ filename?: string; page?: number; text?: string }>;
  [k: string]: unknown;
}

function DocumentsPage() {
  const qc = useQueryClient();
  const fileRef = useRef<HTMLInputElement>(null);
  const [selectedDoc, setSelectedDoc] = useState<string | "">("");
  const [query, setQuery] = useState("");
  const [result, setResult] = useState<QueryResult | null>(null);

  const docsQ = useQuery({
    queryKey: ["docs"],
    queryFn: () => api.get<RagDocument[]>("/api/rag/documents"),
  });

  const upload = useMutation({
    mutationFn: (file: File) => api.upload<{ document_id: string; status: string; chunks: number }>("/api/rag/upload", file),
    onSuccess: (d) => {
      toast.success(`Indexed ${d.chunks} chunks`);
      qc.invalidateQueries({ queryKey: ["docs"] });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const removeDoc = useMutation({
    mutationFn: (id: string) => api.del(`/api/rag/documents/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["docs"] }),
  });

  const runQuery = useMutation({
    mutationFn: (q: string) =>
      api.post<QueryResult>("/api/rag/query", {
        query: q,
        document_id: selectedDoc || null,
      }),
    onSuccess: (r) => setResult(r),
    onError: (e: Error) => toast.error(e.message),
  });

  // Auto-select the first document when documents load
  useEffect(() => {
    if (docsQ.data && docsQ.data.length > 0 && !selectedDoc) {
      setSelectedDoc(docsQ.data[0]._id);
    }
  }, [docsQ.data, selectedDoc]);

  const handleFiles = (files: FileList | null) => {
    if (!files || files.length === 0) return;
    Array.from(files).forEach((f) => upload.mutate(f));
  };

  return (
    <div className="mx-auto w-full max-w-7xl flex-1 px-4 py-8 space-y-6">
      <div>
        <h1 className="font-display text-3xl md:text-4xl font-bold tracking-tight">Documents</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Upload PDFs, Word, PPT, Excel or images. Query them with retrieval-augmented generation.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[1fr_1.3fr]">
        {/* Left: Upload + List */}
        <div className="space-y-6">
          <div
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => {
              e.preventDefault();
              handleFiles(e.dataTransfer.files);
            }}
            onClick={() => fileRef.current?.click()}
            className="rounded-xl border-2 border-dashed border-border bg-card p-8 text-center cursor-pointer hover:border-primary hover:bg-accent/40 transition"
          >
            <input
              ref={fileRef}
              type="file"
              hidden
              multiple
              onChange={(e) => handleFiles(e.target.files)}
            />
            <div className="grid size-12 place-items-center rounded-xl bg-primary/15 text-primary mx-auto">
              {upload.isPending ? <Loader2 className="size-6 animate-spin" /> : <FileUp className="size-6" />}
            </div>
            <div className="mt-3 text-sm font-semibold">
              {upload.isPending ? "Uploading & indexing…" : "Drop files or click to upload"}
            </div>
            <div className="mt-1 text-xs text-muted-foreground">
              PDF · DOCX · PPTX · XLSX · CSV · Images
            </div>
          </div>

          <div className="rounded-xl border border-border bg-card overflow-hidden">
            <div className="flex items-center justify-between px-4 py-3 border-b border-border">
              <h2 className="text-sm font-semibold">Library</h2>
              <span className="text-xs text-muted-foreground">{docsQ.data?.length ?? 0} docs</span>
            </div>
            <div className="max-h-[420px] overflow-y-auto divide-y divide-border">
              {docsQ.isLoading && <div className="p-4 text-sm text-muted-foreground">Loading…</div>}
              {docsQ.data?.length === 0 && (
                <div className="p-6 text-sm text-muted-foreground text-center">No documents yet.</div>
              )}
              {docsQ.data?.map((d) => {
                const active = selectedDoc === d._id;
                const processed = d.status === "processed";
                return (
                  <div
                    key={d._id}
                    onClick={() => setSelectedDoc(active ? "" : d._id)}
                    className={`group flex items-center gap-3 p-3 cursor-pointer hover:bg-muted/60 transition ${
                      active ? "bg-accent" : ""
                    }`}
                  >
                    <div className="grid size-9 place-items-center rounded-md bg-primary/15 text-primary shrink-0">
                      <FileText className="size-4" />
                    </div>
                    <div className="min-w-0 flex-1">
                      <div className="text-sm font-medium truncate">{d.filename}</div>
                      <div className="mt-0.5 flex items-center gap-1.5 text-[11px] text-muted-foreground">
                        {processed ? (
                          <CheckCircle2 className="size-3 text-primary" />
                        ) : (
                          <AlertCircle className="size-3" />
                        )}
                        {d.status ?? "unknown"}
                      </div>
                    </div>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        removeDoc.mutate(d._id);
                      }}
                      className="opacity-0 group-hover:opacity-100 text-muted-foreground hover:text-destructive transition"
                      aria-label="Delete"
                    >
                      <Trash2 className="size-4" />
                    </button>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Right: Query */}
        <div className="rounded-xl border border-border bg-card flex flex-col">
          <div className="px-5 py-4 border-b border-border">
            <h2 className="text-sm font-semibold">Ask your documents</h2>
            <p className="mt-0.5 text-xs text-muted-foreground">
              {selectedDoc
                ? "Scoped to selected document"
                : "Searching across your entire library"}
            </p>
          </div>

          <div className="p-5 space-y-3">
            <div className="flex gap-2">
              <div className="flex items-center gap-2 flex-1 rounded-lg border border-input bg-background px-3 focus-within:ring-2 focus-within:ring-ring">
                <Search className="size-4 text-muted-foreground" />
                <input
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && query.trim()) runQuery.mutate(query.trim());
                  }}
                  placeholder="What does the document say about…"
                  className="flex-1 bg-transparent py-2.5 text-sm outline-none placeholder:text-muted-foreground"
                />
              </div>
              <button
                onClick={() => query.trim() && runQuery.mutate(query.trim())}
                disabled={!query.trim() || runQuery.isPending}
                className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 text-sm font-semibold text-primary-foreground hover:opacity-90 disabled:opacity-50 transition"
              >
                {runQuery.isPending ? <Loader2 className="size-4 animate-spin" /> : "Ask"}
              </button>
            </div>

            {result && (
              <div className="rounded-lg border border-border bg-background p-4 space-y-3">
                <div className="text-[10px] uppercase tracking-widest text-muted-foreground">Answer</div>
                <p className="text-sm leading-relaxed whitespace-pre-wrap">
                  {result.answer || result.response || JSON.stringify(result, null, 2)}
                </p>
                {result.sources && result.sources.length > 0 && (
                  <div className="pt-3 border-t border-border">
                    <div className="text-[10px] uppercase tracking-widest text-muted-foreground mb-2">
                      Sources
                    </div>
                    <ul className="space-y-2">
                      {result.sources.map((s, i) => (
                        <li
                          key={i}
                          className="text-xs text-muted-foreground border-l-2 border-primary pl-3"
                        >
                          <span className="font-medium text-foreground">
                            {s.filename ?? "source"}
                            {s.page !== undefined ? ` · p.${s.page}` : ""}
                          </span>
                          {s.text && <div className="mt-1 line-clamp-3">{s.text}</div>}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {!result && !runQuery.isPending && (
              <div className="text-center text-xs text-muted-foreground py-10">
                Results will appear here.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
