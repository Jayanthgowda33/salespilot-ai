import { useEffect, useState } from "react";
import { api } from "../api/client";
import Navbar from "../components/Navbar";
import { Lead } from "../types";

export default function Leads() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [scoringId, setScoringId] = useState<string | null>(null);

  async function loadLeads() {
    const res = await api.get("/api/leads");
    setLeads(res.data);
  }

  useEffect(() => {
    loadLeads();
  }, []);

  async function handleAddLead(e: React.FormEvent) {
    e.preventDefault();
    await api.post("/api/leads", { name, email, company_name: companyName });
    setName(""); setEmail(""); setCompanyName("");
    setShowForm(false);
    loadLeads();
  }

  async function handleScore(leadId: string) {
    setScoringId(leadId);
    try {
      await api.post(`/api/ai/score-lead/${leadId}`);
      await loadLeads();
    } finally {
      setScoringId(null);
    }
  }

  function scoreColor(score: number | null) {
    if (score === null) return "bg-panelBorder text-gray-400";
    if (score >= 70) return "bg-accentDim text-accentSoft";
    if (score >= 40) return "bg-yellow-950 text-yellow-400";
    return "bg-red-950 text-red-400";
  }

  const inputClass =
    "bg-app border border-panelBorder text-white placeholder-gray-500 rounded-lg px-3 py-2 flex-1 min-w-[150px] focus:outline-none focus:border-accent transition-colors";

  return (
    <div className="min-h-screen bg-app">
      <Navbar />
      <div className="p-6 max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-xl font-bold text-white">Leads</h1>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-accent text-black rounded-lg px-4 py-2 text-sm font-semibold hover:bg-accentSoft transition-colors"
          >
            + New Lead
          </button>
        </div>

        {showForm && (
          <form onSubmit={handleAddLead} className="animate-fadeInUp bg-panel border border-panelBorder rounded-xl p-4 mb-6 flex gap-3 flex-wrap">
            <input placeholder="Lead name" value={name} onChange={(e) => setName(e.target.value)} required className={inputClass} />
            <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} className={inputClass} />
            <input placeholder="Company" value={companyName} onChange={(e) => setCompanyName(e.target.value)} className={inputClass} />
            <button type="submit" className="bg-accent text-black rounded-lg px-4 py-2 text-sm font-semibold hover:bg-accentSoft transition-colors">
              Save
            </button>
          </form>
        )}

        <div className="bg-panel border border-panelBorder rounded-xl overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-app text-gray-500 text-left">
              <tr>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Company</th>
                <th className="px-4 py-3">Status</th>
                <th className="px-4 py-3">AI Score</th>
                <th className="px-4 py-3">Next Best Action</th>
                <th className="px-4 py-3"></th>
              </tr>
            </thead>
            <tbody>
              {leads.map((lead) => (
                <tr key={lead.id} className="border-t border-panelBorder hover:bg-app/50 transition-colors">
                  <td className="px-4 py-3 font-medium text-white">{lead.name}</td>
                  <td className="px-4 py-3 text-gray-400">{lead.company_name || "—"}</td>
                  <td className="px-4 py-3 text-gray-400 capitalize">{lead.status}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${scoreColor(lead.ai_score)}`}>
                      {lead.ai_score !== null ? `${lead.ai_score}` : "Not scored"}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-400 max-w-xs truncate">{lead.next_best_action || "—"}</td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => handleScore(lead.id)}
                      disabled={scoringId === lead.id}
                      className="text-accentSoft hover:text-accent hover:underline text-xs font-medium disabled:opacity-50"
                    >
                      {scoringId === lead.id ? "Scoring..." : "Run AI Score"}
                    </button>
                  </td>
                </tr>
              ))}
              {leads.length === 0 && (
                <tr>
                  <td colSpan={6} className="px-4 py-8 text-center text-gray-600">No leads yet. Add your first one above.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
