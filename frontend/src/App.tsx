import { useEffect, useState } from "react";
import type { FormEvent } from "react";
import { loginUser, registerUser } from "./api/auth";
import { clearToken, getToken } from "./api/client";
import { explainAlert, getAegisKnowledge, getAegisStatus, getAegisWelcome, sendAegisMessage } from "./api/aegis";
import {
  analyzeNetworkRequest,
  getAlerts,
  getBackendStatus,
  getDatabaseStatus,
  getDashboardSummary,
  getDetections,
  getSecurityEvents,
} from "./api/security";
import type { Alert, DashboardSummary, Detection, SecurityEvent, User } from "./types";

type View = "overview" | "detection" | "alerts" | "events" | "aegis" | "system";
type Notice = { kind: "success" | "error"; text: string } | null;

function StatusDot({ ok }: { ok: boolean }) {
  return <span className={`inline-block h-2.5 w-2.5 rounded-full ${ok ? "bg-emerald-400" : "bg-rose-400"}`} />;
}

function Card({ title, value, detail, ok }: { title: string; value: string; detail: string; ok?: boolean }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5 shadow-lg shadow-black/10">
      <div className="flex items-center justify-between text-sm text-slate-400">
        <span>{title}</span>{ok !== undefined && <StatusDot ok={ok} />}
      </div>
      <div className="mt-3 text-2xl font-semibold text-white">{value}</div>
      <div className="mt-1 text-xs text-slate-500">{detail}</div>
    </div>
  );
}

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [view, setView] = useState<View>("overview");
  const [authMode, setAuthMode] = useState<"login" | "register">("login");
  const [notice, setNotice] = useState<Notice>(null);
  const [booting, setBooting] = useState(true);

  useEffect(() => {
    if (!getToken()) {
      setBooting(false);
      return;
    }
    getBackendStatus()
      .then(() => setUser({ id: 0, username: "Authenticated user", email: "", is_active: true }))
      .catch(() => clearToken())
      .finally(() => setBooting(false));
  }, []);

  if (booting) return <FullScreenMessage text="Restoring secure session…" />;
  if (!user) {
    return (
      <AuthScreen
        mode={authMode}
        onModeChange={setAuthMode}
        onAuthenticated={(nextUser) => setUser(nextUser)}
        onNotice={setNotice}
      />
    );
  }

  return (
    <div className="min-h-screen bg-[#07111f] text-slate-200">
      <header className="sticky top-0 z-20 border-b border-slate-800 bg-[#07111f]/95 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-4 lg:px-8">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.25em] text-cyan-400">EAG</p>
            <h1 className="text-lg font-semibold text-white">Extension AI Guard</h1>
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-slate-400 sm:block">{user.username}</span>
            <button onClick={() => { clearToken(); setUser(null); }} className="rounded-lg border border-slate-700 px-3 py-2 text-sm text-slate-300 hover:bg-slate-800">
              Logout
            </button>
          </div>
        </div>
      </header>

      <div className="mx-auto flex max-w-7xl gap-6 px-4 py-6 lg:px-8">
        <aside className="hidden w-52 shrink-0 lg:block">
          <nav className="sticky top-24 space-y-1">
            {(["overview", "detection", "alerts", "events", "aegis", "system"] as View[]).map((item) => (
              <button key={item} onClick={() => setView(item)} className={`w-full rounded-xl px-4 py-3 text-left text-sm capitalize ${view === item ? "bg-cyan-500/15 text-cyan-300" : "text-slate-400 hover:bg-slate-900 hover:text-white"}`}>
                {item === "events" ? "Security Events" : item}
              </button>
            ))}
          </nav>
        </aside>

        <main className="min-w-0 flex-1">
          <div className="mb-6 lg:hidden">
            <select value={view} onChange={(e) => setView(e.target.value as View)} className="w-full rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm text-white">
              <option value="overview">Overview</option>
              <option value="detection">Detection</option>
              <option value="alerts">Alerts</option>
              <option value="events">Security Events</option>
              <option value="aegis">Aegis</option>
              <option value="system">System Status</option>
            </select>
          </div>
          {notice && <div className={`mb-5 rounded-xl border px-4 py-3 text-sm ${notice.kind === "success" ? "border-emerald-800 bg-emerald-950/40 text-emerald-300" : "border-rose-800 bg-rose-950/40 text-rose-300"}`}>{notice.text}</div>}
          {view === "overview" && <Overview />}
          {view === "detection" && <DetectionPage onNotice={setNotice} />}
          {view === "alerts" && <AlertsPage />}
          {view === "events" && <EventsPage />}
          {view === "aegis" && <AegisPage onNotice={setNotice} />}
          {view === "system" && <SystemPage />}
        </main>
      </div>
    </div>
  );
}

function FullScreenMessage({ text }: { text: string }) {
  return <div className="grid min-h-screen place-items-center bg-[#07111f] text-slate-300">{text}</div>;
}

function AuthScreen({ mode, onModeChange, onAuthenticated, onNotice }: { mode: "login" | "register"; onModeChange: (m: "login" | "register") => void; onAuthenticated: (u: User) => void; onNotice: (n: Notice) => void }) {
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent) {
    event.preventDefault();
    setBusy(true); onNotice(null);
    try {
      if (mode === "register") {
        if (username.trim().length < 2) throw new Error("Username must contain at least 2 characters.");
        await registerUser({ username: username.trim(), email: email.trim(), password });
        onModeChange("login");
        onNotice({ kind: "success", text: "Registration complete. Sign in to continue." });
      } else {
        const nextUser = await loginUser({ email: email.trim(), password });
        onAuthenticated(nextUser);
      }
    } catch (error) {
      onNotice({ kind: "error", text: error instanceof Error ? error.message : "Authentication failed." });
    } finally { setBusy(false); }
  }

  return (
    <div className="grid min-h-screen place-items-center bg-[#07111f] px-4">
      <div className="w-full max-w-md rounded-3xl border border-slate-800 bg-slate-900/90 p-7 shadow-2xl">
        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-cyan-400">Security Console</p>
        <h1 className="mt-3 text-3xl font-bold text-white">Extension AI Guard</h1>
        <p className="mt-2 text-sm text-slate-400">Authenticated access to the EAG security dashboard.</p>
        <form onSubmit={submit} className="mt-7 space-y-4">
          {mode === "register" && <Field label="Username" value={username} onChange={setUsername} />}
          <Field label="Email" type="email" value={email} onChange={setEmail} />
          <Field label="Password" type="password" value={password} onChange={setPassword} />
          <button disabled={busy} className="w-full rounded-xl bg-cyan-500 px-4 py-3 font-semibold text-slate-950 disabled:opacity-50">{busy ? "Processing…" : mode === "login" ? "Sign in" : "Create account"}</button>
        </form>
        <button onClick={() => onModeChange(mode === "login" ? "register" : "login")} className="mt-5 w-full text-sm text-slate-400 hover:text-cyan-300">
          {mode === "login" ? "Need an account? Register" : "Already registered? Sign in"}
        </button>
      </div>
    </div>
  );
}

function Field({ label, type = "text", value, onChange }: { label: string; type?: string; value: string; onChange: (v: string) => void }) {
  return <label className="block text-sm text-slate-300"><span className="mb-2 block">{label}</span><input required type={type} value={value} onChange={(e) => onChange(e.target.value)} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white outline-none focus:border-cyan-500" /></label>;
}

function Overview() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [backend, setBackend] = useState("Checking…");
  const [db, setDb] = useState("Checking…");
  const [aegis, setAegis] = useState("Checking…");
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getDashboardSummary(), getBackendStatus(), getDatabaseStatus(), getAegisStatus()])
      .then(([s, b, d, a]) => {
        setSummary(s); setBackend(b.status); setDb(d.status); setAegis(a.completed ? "Completed" : a.started ? "In progress" : "Not started");
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Unable to load overview."));
  }, []);

  if (error) return <ErrorState message={error} />;
  if (!summary) return <LoadingState />;

  return <>
    <PageTitle title="Security Overview" subtitle="Current verified operational state. Historical values come only from persisted backend records." />
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      <Card title="Backend" value={backend} detail="Phase 19 API" ok={backend === "online"} />
      <Card title="Database" value={db} detail="Persistence layer" ok={db === "configured"} />
      <Card title="Detections" value={String(summary.detection_count)} detail="Persisted analyses" />
      <Card title="Alerts" value={String(summary.alert_count)} detail="Persisted security alerts" />
    </div>
    <div className="mt-4 grid gap-4 sm:grid-cols-2">
      <Card title="Malicious" value={String(summary.malicious_count)} detail="Persisted malicious classifications" />
      <Card title="Aegis" value={aegis} detail="Authenticated onboarding state" />
    </div>
    <section className="mt-6 rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
      <h2 className="text-lg font-semibold text-white">Latest detection</h2>
      {summary.latest_detection ? <div className="mt-4 grid gap-3 sm:grid-cols-2">
        <Info label="Request" value={summary.latest_detection.request_id} />
        <Info label="Classification" value={summary.latest_detection.is_malicious ? "MALICIOUS" : "BENIGN"} />
        <Info label="Confidence" value={`${(summary.latest_detection.confidence * 100).toFixed(1)}%`} />
        <Info label="Threat type" value={summary.latest_detection.threat_type} />
        <div className="sm:col-span-2"><Info label="Explanation" value={summary.latest_detection.explanation} /></div>
      </div> : <EmptyState text="No network-request analyses have been persisted yet." />}
    </section>
  </>;
}

function DetectionPage({ onNotice }: { onNotice: (n: Notice) => void }) {
  const [form, setForm] = useState({ request_id: `req-${Date.now()}`, url: "http://example.test/", method: "GET", domain: "example.test", timestamp: new Date().toISOString() });
  const [result, setResult] = useState<Detection | null>(null);\n  const [analysisDetails, setAnalysisDetails] = useState<{ alert: Alert | null; security_event: SecurityEvent } | null>(null);
  const [busy, setBusy] = useState(false);
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true); onNotice(null);
    try { const response = await analyzeNetworkRequest(form); setResult(response.detection); setAnalysisDetails({ alert: response.alert, security_event: response.security_event }); onNotice({ kind: "success", text: "Network request analyzed and persisted." }); }
    catch (error) { onNotice({ kind: "error", text: error instanceof Error ? error.message : "Analysis failed." }); }
    finally { setBusy(false); }
  }
  return <>
    <PageTitle title="Detection" subtitle="Submit a controlled request to the authoritative Phase 19 analysis endpoint." />
    <form onSubmit={submit} className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6">
      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Request ID" value={form.request_id} onChange={(v) => setForm({ ...form, request_id: v })} />
        <Field label="Domain" value={form.domain} onChange={(v) => setForm({ ...form, domain: v })} />
        <div className="sm:col-span-2"><Field label="URL" value={form.url} onChange={(v) => setForm({ ...form, url: v })} /></div>
        <label className="block text-sm text-slate-300"><span className="mb-2 block">HTTP method</span><select value={form.method} onChange={(e) => setForm({ ...form, method: e.target.value })} className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-white"><option>GET</option><option>POST</option><option>PUT</option><option>PATCH</option><option>DELETE</option></select></label>
        <Field label="Timestamp" value={form.timestamp} onChange={(v) => setForm({ ...form, timestamp: v })} />
      </div>
      <button disabled={busy} className="mt-5 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950 disabled:opacity-50">{busy ? "Analyzing…" : "Analyze request"}</button>
    </form>
    {result && <section className="mt-5 rounded-2xl border border-slate-800 bg-slate-900/80 p-6"><h2 className="text-lg font-semibold text-white">Detection result</h2><div className="mt-4 grid gap-3 sm:grid-cols-2"><Info label="Classification" value={result.is_malicious ? "MALICIOUS" : "BENIGN"} /><Info label="Confidence" value={`${(result.confidence * 100).toFixed(1)}%`} /><Info label="Threat type" value={result.threat_type} /><Info label="Request ID" value={result.request_id} /><div className="sm:col-span-2"><Info label="Explanation" value={result.explanation} /></div>{analysisDetails && <><Info label="Alert" value={analysisDetails.alert ? `${analysisDetails.alert.severity.toUpperCase()}: ${analysisDetails.alert.title}` : "No alert generated"} /><Info label="Security event" value={`${analysisDetails.security_event.event_type} / ${analysisDetails.security_event.severity}`} /></>}</div></section>}
  </>;
}

function AlertsPage() {
  const [items, setItems] = useState<Alert[] | null>(null);
  const [error, setError] = useState("");
  useEffect(() => { getAlerts().then(setItems).catch(e => setError(e.message)); }, []);
  if (error) return <ErrorState message={error} />; if (!items) return <LoadingState />;
  return <><PageTitle title="Alerts" subtitle="Persisted alerts generated by backend security analysis." />{items.length ? <div className="space-y-3">{items.map(a => <div key={a.alert_id} className="rounded-2xl border border-rose-900/60 bg-rose-950/20 p-5"><div className="flex flex-wrap justify-between gap-3"><span className="rounded-full bg-rose-500/15 px-3 py-1 text-xs font-semibold uppercase text-rose-300">{a.severity}</span><span className="text-xs text-slate-500">{new Date(a.created_at).toLocaleString()}</span></div><h2 className="mt-3 font-semibold text-white">{a.title}</h2><p className="mt-1 text-sm text-slate-400">{a.message}</p></div>)}</div> : <EmptyState text="No persisted alerts are available." />}</>;
}

function EventsPage() {
  const [items, setItems] = useState<SecurityEvent[] | null>(null); const [error, setError] = useState("");
  useEffect(() => { getSecurityEvents().then(setItems).catch(e => setError(e.message)); }, []);
  if (error) return <ErrorState message={error} />; if (!items) return <LoadingState />;
  return <><PageTitle title="Security Events" subtitle="Persisted events emitted by backend security operations." />{items.length ? <div className="space-y-3">{items.map(e => <div key={e.event_id} className="rounded-2xl border border-slate-800 bg-slate-900/80 p-5"><div className="flex justify-between gap-3"><span className="text-sm font-semibold text-white">{e.event_type}</span><span className="text-xs text-slate-500">{new Date(e.timestamp).toLocaleString()}</span></div><p className="mt-2 text-sm text-slate-400">{e.description}</p></div>)}</div> : <EmptyState text="No persisted security events are available." />}</>;
}

function AegisPage({ onNotice }: { onNotice: (n: Notice) => void }) {
  const [status, setStatus] = useState<Record<string, unknown> | null>(null);
  const [welcome, setWelcome] = useState<Record<string, unknown> | null>(null);
  const [knowledge, setKnowledge] = useState<Record<string, unknown> | null>(null);
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState<Record<string, unknown> | null>(null);
  const [alertForm, setAlertForm] = useState({ severity: "high", title: "Malicious Network Request Detected", message: "" });
  const [explanation, setExplanation] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    Promise.all([getAegisWelcome(), getAegisStatus(), getAegisKnowledge()])
      .then(([w, s, k]) => { setWelcome(w); setStatus(s); setKnowledge(k); })
      .catch(e => onNotice({ kind: "error", text: e.message }));
  }, [onNotice]);

  async function send(e: FormEvent) {
    e.preventDefault();
    try { setResponse(await sendAegisMessage(message)); setMessage(""); }
    catch (error) { onNotice({ kind: "error", text: error instanceof Error ? error.message : "Aegis request failed." }); }
  }

  async function explain(e: FormEvent) {
    e.preventDefault();
    try { setExplanation(await explainAlert(alertForm.severity, alertForm.title, alertForm.message)); }
    catch (error) { onNotice({ kind: "error", text: error instanceof Error ? error.message : "Alert explanation failed." }); }
  }

  return <>
    <PageTitle title="Aegis" subtitle="Authenticated security assistant integration." />
    <div className="grid gap-5 lg:grid-cols-2">
      <section className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6"><h2 className="font-semibold text-white">Welcome</h2><pre className="mt-4 max-h-56 overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-400">{JSON.stringify(welcome, null, 2)}</pre></section>
      <section className="rounded-2xl border border-slate-800 bg-slate-900/80 p-6"><h2 className="font-semibold text-white">Onboarding status</h2><pre className="mt-4 max-h-56 overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-400">{JSON.stringify(status, null, 2)}</pre></section>
    </div>
    <section className="mt-5 rounded-2xl border border-slate-800 bg-slate-900/80 p-6"><h2 className="font-semibold text-white">Knowledge</h2><pre className="mt-4 max-h-64 overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-400">{JSON.stringify(knowledge, null, 2)}</pre></section>
    <form onSubmit={send} className="mt-5 rounded-2xl border border-slate-800 bg-slate-900/80 p-6"><label className="block text-sm text-slate-300">Message<textarea required value={message} onChange={e => setMessage(e.target.value)} rows={4} className="mt-2 w-full rounded-xl border border-slate-700 bg-slate-950 p-4 text-white outline-none focus:border-cyan-500" /></label><button className="mt-4 rounded-xl bg-cyan-500 px-5 py-3 font-semibold text-slate-950">Ask Aegis</button>{response && <pre className="mt-4 overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-400">{JSON.stringify(response, null, 2)}</pre>}</form>
    <form onSubmit={explain} className="mt-5 rounded-2xl border border-slate-800 bg-slate-900/80 p-6"><h2 className="font-semibold text-white">Explain an alert</h2><div className="mt-4 grid gap-4 sm:grid-cols-2"><Field label="Severity" value={alertForm.severity} onChange={v => setAlertForm({ ...alertForm, severity: v })} /><Field label="Title" value={alertForm.title} onChange={v => setAlertForm({ ...alertForm, title: v })} /><div className="sm:col-span-2"><Field label="Alert message" value={alertForm.message} onChange={v => setAlertForm({ ...alertForm, message: v })} /></div></div><button className="mt-4 rounded-xl border border-cyan-700 px-5 py-3 font-semibold text-cyan-300">Explain alert</button>{explanation && <pre className="mt-4 overflow-auto rounded-xl bg-slate-950 p-4 text-xs text-slate-400">{JSON.stringify(explanation, null, 2)}</pre>}</form>
  </>;
}

function SystemPage() {
  const [data, setData] = useState<Record<string, string> | null>(null); const [error, setError] = useState("");
  useEffect(() => { Promise.all([getBackendStatus(), getDatabaseStatus()]).then(([b,d]) => setData({ backend: b.status, database: d.status, frontend: "online" })).catch(e => setError(e.message)); }, []);
  if (error) return <ErrorState message={error} />; if (!data) return <LoadingState />;
  return <><PageTitle title="System Status" subtitle="Connectivity and service state from verified backend responses." /><div className="grid gap-4 sm:grid-cols-3">{Object.entries(data).map(([k,v]) => <Card key={k} title={k} value={v} detail="Current status" ok={v === "online" || v === "configured"} />)}</div></>;
}

function PageTitle({ title, subtitle }: { title: string; subtitle: string }) { return <div className="mb-6"><h2 className="text-2xl font-bold text-white">{title}</h2><p className="mt-1 max-w-3xl text-sm text-slate-400">{subtitle}</p></div>; }
function Info({ label, value }: { label: string; value: string }) { return <div className="rounded-xl bg-slate-950/70 p-4"><div className="text-xs uppercase tracking-wider text-slate-500">{label}</div><div className="mt-1 break-words text-sm text-slate-200">{value}</div></div>; }
function LoadingState() { return <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-8 text-center text-sm text-slate-400">Loading verified backend data…</div>; }
function EmptyState({ text }: { text: string }) { return <div className="rounded-xl border border-dashed border-slate-700 p-8 text-center text-sm text-slate-500">{text}</div>; }
function ErrorState({ message }: { message: string }) { return <div className="rounded-2xl border border-rose-900/60 bg-rose-950/20 p-6 text-sm text-rose-300">Service error: {message}</div>; }

export default App;
