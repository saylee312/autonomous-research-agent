import { createFileRoute } from "@tanstack/react-router";
import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Download, FileText, Loader2, Sparkles, Trash2, Clock } from "lucide-react";
import { toast } from "sonner";
import { api, API_BASE, type ResearchReport } from "@/lib/api";

export const Route = createFileRoute("/research")({
  head: () => ({
    meta: [
      { title: "Research" },
    ],
  }),
  component: ResearchPage,
});

function ResearchPage() {
  const qc = useQueryClient();
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<ResearchReport | null>(null);

  const reportsQ = useQuery({
    queryKey: ["reports"],
    queryFn: () => api.get<ResearchReport[]>("/api/reports/"),
  });

  const generate = useMutation({
    mutationFn: (q: string) =>
      api.post<{ report_id: string; report: string; generation_time_seconds: number }>(
        "/api/reports/generate-report",
        { query: q }
      ),
    onSuccess: (data) => {
      toast.success(`Report generated in ${data.generation_time_seconds.toFixed(1)}s`);
      qc.invalidateQueries({ queryKey: ["reports"] });
      setSelected({ _id: data.report_id, title: query, content: data.report });
    },
    onError: (e: Error) => toast.error(e.message),
  });

  const removeReport = useMutation({
    mutationFn: (id: string) => api.del(`/api/reports/${id}`),
    onSuccess: (_d, id) => {
      qc.invalidateQueries({ queryKey: ["reports"] });
      if (selected?._id === id) setSelected(null);
    },
  });

  return (
    <div className="mx-auto w-full max-w-7xl flex-1 px-4 py-8">
      {/* Hero / generator */}
      <div className="rounded-2xl border border-border bg-card p-6 md:p-8 shadow-sm">
        <div className="flex items-center gap-2 text-xs uppercase tracking-widest text-muted-foreground">
          <Sparkles className="size-3.5 text-primary" /> Autonomous Research
        </div>
        <h1 className="mt-2 text-3xl md:text-4xl font-bold tracking-tight">
          Generate a deep-research report
        </h1>
        <p className="mt-2 text-sm text-muted-foreground max-w-2xl">
          Describe a topic or question. The agent will plan, research the web, synthesize findings,
          and write a structured report.
        </p>

        <div className="mt-6 flex flex-col md:flex-row gap-2">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g. State of small open-source language models in 2026"
            className="flex-1 rounded-lg border border-input bg-background px-4 py-3 text-sm outline-none focus:ring-2 focus:ring-ring"
            onKeyDown={(e) => {
              if (e.key === "Enter" && query.trim() && !generate.isPending) generate.mutate(query.trim());
            }}
          />
          <button
            onClick={() => query.trim() && generate.mutate(query.trim())}
            disabled={!query.trim() || generate.isPending}
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground hover:opacity-90 disabled:opacity-50 transition"
          >
            {generate.isPending ? (
              <>
                <Loader2 className="size-4 animate-spin" /> Researching…
              </>
            ) : (
              <>
                <Sparkles className="size-4" /> Generate
              </>
            )}
          </button>
        </div>
        {generate.isPending && (
          <p className="mt-3 text-xs text-muted-foreground">
            This can take 30s–2min as the agent plans, searches, and synthesizes.
          </p>
        )}
      </div>

      {/* Reports grid + viewer */}
      <div className="mt-8 grid gap-6 md:grid-cols-[1fr_1.4fr]">
        <div className="rounded-xl border border-border bg-card overflow-hidden">
          <div className="flex items-center justify-between px-4 py-3 border-b border-border">
            <h2 className="text-sm font-semibold">Library</h2>
            <span className="text-xs text-muted-foreground">
              {reportsQ.data?.length ?? 0} reports
            </span>
          </div>
          <div className="max-h-[560px] overflow-y-auto divide-y divide-border">
            {reportsQ.isLoading && (
              <div className="p-4 text-sm text-muted-foreground">Loading…</div>
            )}
            {reportsQ.data?.length === 0 && (
              <div className="p-6 text-sm text-muted-foreground text-center">
                No reports yet — generate your first above.
              </div>
            )}
            {reportsQ.data?.map((r) => (
              <button
                key={r._id}
                onClick={() => setSelected(r)}
                className={`w-full text-left p-4 hover:bg-muted/60 transition flex gap-3 ${
                  selected?._id === r._id ? "bg-accent" : ""
                }`}
              >
                <div className="grid size-9 place-items-center rounded-md bg-primary/15 text-primary shrink-0">
                  <FileText className="size-4" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="text-sm font-medium truncate">{r.title}</div>
                  <div className="mt-0.5 flex items-center gap-2 text-[11px] text-muted-foreground">
                    <Clock className="size-3" />
                    {r.created_at ? new Date(r.created_at).toLocaleString() : "—"}
                  </div>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    removeReport.mutate(r._id);
                  }}
                  className="text-muted-foreground hover:text-destructive transition"
                  aria-label="Delete"
                >
                  <Trash2 className="size-4" />
                </button>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-border bg-card flex flex-col min-h-[400px]">
          {!selected ? (
            <div className="flex-1 grid place-items-center text-center p-10">
              <div>
                <div className="grid size-14 place-items-center rounded-2xl bg-primary/15 text-primary mx-auto">
                  <FileText className="size-7" />
                </div>
                <h3 className="mt-4 text-lg font-semibold">No report selected</h3>
                <p className="mt-1 text-sm text-muted-foreground max-w-sm">
                  Pick a report from the library, or generate a new one.
                </p>
              </div>
            </div>
          ) : (
            <>
              <div className="flex items-center justify-between gap-4 px-5 py-4 border-b border-border">
                <div className="min-w-0">
                  <h3 className="font-display text-lg font-semibold truncate">{selected.title}</h3>
                  <p className="text-xs text-muted-foreground font-mono">{selected._id}</p>
                </div>
                <a
                  href={`${API_BASE}/api/reports/${selected._id}/download`}
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center gap-2 rounded-lg border border-border bg-background px-3 py-2 text-xs font-medium hover:bg-accent transition"
                >
                  <Download className="size-3.5" /> Download
                </a>
              </div>
              <div className="flex-1 overflow-y-auto px-6 py-5 prose-content">
                {selected.content ? (
                  <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-foreground">
                    {selected.content}
                  </pre>
                ) : (
                  <p className="text-sm text-muted-foreground">
                    Content preview unavailable. Use the download button to open the full report.
                  </p>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
