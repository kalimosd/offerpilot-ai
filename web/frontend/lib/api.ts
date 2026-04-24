const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function fetchSSE(
  message: string,
  history: { role: string; content: string }[],
  onEvent: (event: string, data: unknown) => void,
) {
  const res = await fetch(`${API}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  const reader = res.body?.getReader();
  if (!reader) return;
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() || "";
    let currentEvent = "token";
    for (const line of lines) {
      if (line.startsWith("event:")) {
        currentEvent = line.slice(6).trim();
      } else if (line.startsWith("data:")) {
        try {
          const data = JSON.parse(line.slice(5).trim());
          onEvent(currentEvent, data);
        } catch { /* skip */ }
      }
    }
  }
}

export async function getTracker(status = "", company = "") {
  const params = new URLSearchParams();
  if (status) params.set("status", status);
  if (company) params.set("company", company);
  const res = await fetch(`${API}/api/tracker?${params}`);
  return res.json();
}

export async function addTracker(data: { url: string; company: string; title: string; status?: string; notes?: string }) {
  const res = await fetch(`${API}/api/tracker`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
  return res.json();
}

export async function updateTracker(data: { url: string; status: string; notes?: string }) {
  const res = await fetch(`${API}/api/tracker`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
  return res.json();
}

export async function getFollowups() {
  const res = await fetch(`${API}/api/tracker/followups`);
  return res.json();
}

export async function getOutputs(dir = "") {
  const res = await fetch(`${API}/api/files/outputs?dir=${dir}`);
  return res.json();
}

export async function uploadFile(file: File, target = "root") {
  const form = new FormData();
  form.append("file", file);
  form.append("target", target);
  const res = await fetch(`${API}/api/files/upload`, { method: "POST", body: form });
  return res.json();
}

export async function deleteFile(subdir: string, filename: string) {
  const res = await fetch(`${API}/api/files/outputs/${subdir}/${filename}`, { method: "DELETE" });
  return res.json();
}

export function getFileUrl(subdir: string, filename: string) {
  return `${API}/api/files/outputs/${subdir}/${filename}`;
}
