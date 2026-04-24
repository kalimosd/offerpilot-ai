"use client";

import { useState, useEffect, useCallback } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { getTracker, addTracker, updateTracker, getFollowups } from "@/lib/api";

const STATUS_COLORS: Record<string, string> = {
  discovered: "bg-zinc-200 text-zinc-700",
  applied: "bg-blue-100 text-blue-700",
  interviewing: "bg-yellow-100 text-yellow-700",
  offer: "bg-green-100 text-green-700",
  rejected: "bg-red-100 text-red-700",
  ghosted: "bg-zinc-100 text-zinc-400",
};
const STATUSES = ["discovered", "applied", "interviewing", "offer", "rejected", "ghosted"];

interface TrackerRow {
  url: string; company: string; title: string; status: string;
  applied_date: string; last_update: string; notes: string;
}

function parseTrackerResult(result: string): TrackerRow[] {
  const lines = result.split("\n").filter((l) => l.startsWith("- ["));
  return lines.map((l) => {
    const match = l.match(/\[(\w+)\]\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+)/);
    if (!match) return null;
    return { status: match[1], company: match[2], title: match[3], last_update: match[4], url: match[5], applied_date: "", notes: "" };
  }).filter(Boolean) as TrackerRow[];
}

export default function TrackerPage() {
  const [rows, setRows] = useState<TrackerRow[]>([]);
  const [followups, setFollowups] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");
  const [filterCompany, setFilterCompany] = useState("");
  const [addOpen, setAddOpen] = useState(false);
  const [form, setForm] = useState({ url: "", company: "", title: "", status: "discovered", notes: "" });

  const load = useCallback(async () => {
    const status = filterStatus === "all" ? "" : filterStatus;
    const res = await getTracker(status, filterCompany);
    setRows(parseTrackerResult(res.result));
    const f = await getFollowups();
    setFollowups(f.result);
  }, [filterStatus, filterCompany]);

  useEffect(() => { load(); }, [load]);

  async function handleAdd() {
    await addTracker(form);
    setForm({ url: "", company: "", title: "", status: "discovered", notes: "" });
    setAddOpen(false);
    load();
  }

  async function handleStatusChange(url: string, status: string) {
    await updateTracker({ url, status });
    load();
  }

  return (
    <div className="flex flex-col h-full">
      <div className="border-b border-zinc-200 px-6 py-3 flex items-center justify-between">
        <h1 className="text-sm font-semibold">Application Tracker</h1>
        <Dialog open={addOpen} onOpenChange={setAddOpen}>
          <DialogTrigger><Button size="sm">+ 添加</Button></DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>添加申请记录</DialogTitle></DialogHeader>
            <div className="flex flex-col gap-3 mt-2">
              <Input placeholder="岗位链接" value={form.url} onChange={(e) => setForm({ ...form, url: e.target.value })} />
              <Input placeholder="公司" value={form.company} onChange={(e) => setForm({ ...form, company: e.target.value })} />
              <Input placeholder="岗位" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
              <Select value={form.status} onValueChange={(v) => v && setForm({ ...form, status: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>{STATUSES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
              </Select>
              <Input placeholder="备注" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} />
              <Button onClick={handleAdd}>添加</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>

      {followups && !followups.includes("暂无") && (
        <div className="bg-yellow-50 border-b border-yellow-200 px-6 py-2 text-sm text-yellow-800">
          ⏰ {followups}
        </div>
      )}

      <div className="px-6 py-3 flex gap-3 border-b border-zinc-100">
        <Select value={filterStatus} onValueChange={(v) => v && setFilterStatus(v)}>
          <SelectTrigger className="w-40"><SelectValue placeholder="状态筛选" /></SelectTrigger>
          <SelectContent>
            <SelectItem value="all">全部状态</SelectItem>
            {STATUSES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}
          </SelectContent>
        </Select>
        <Input placeholder="搜索公司..." value={filterCompany} onChange={(e) => setFilterCompany(e.target.value)} className="w-48" />
      </div>

      <div className="flex-1 overflow-y-auto px-6 py-2">
        {rows.length === 0 ? (
          <p className="text-center text-zinc-400 mt-20 text-sm">暂无记录</p>
        ) : (
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-zinc-500 border-b">
                <th className="py-2 font-medium">公司</th>
                <th className="py-2 font-medium">岗位</th>
                <th className="py-2 font-medium">状态</th>
                <th className="py-2 font-medium">更新时间</th>
                <th className="py-2 font-medium">链接</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r, i) => (
                <tr key={i} className="border-b border-zinc-50 hover:bg-zinc-50">
                  <td className="py-2">{r.company}</td>
                  <td className="py-2">{r.title}</td>
                  <td className="py-2">
                    <Select value={r.status} onValueChange={(v) => v && handleStatusChange(r.url, v)}>
                      <SelectTrigger className="h-7 w-32 border-0 p-0">
                        <Badge className={STATUS_COLORS[r.status] || ""}>{r.status}</Badge>
                      </SelectTrigger>
                      <SelectContent>{STATUSES.map((s) => <SelectItem key={s} value={s}>{s}</SelectItem>)}</SelectContent>
                    </Select>
                  </td>
                  <td className="py-2 text-zinc-500">{r.last_update}</td>
                  <td className="py-2"><a href={r.url} target="_blank" className="text-blue-600 hover:underline text-xs">查看</a></td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
