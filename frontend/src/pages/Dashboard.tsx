import { useEffect, useState } from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { api } from "../api/client";
import Navbar from "../components/Navbar";
import { DashboardSummary } from "../types";

export default function Dashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);

  useEffect(() => {
    api.get("/api/dashboard/summary").then((res) => setSummary(res.data));
  }, []);

  const cards = summary
    ? [
        { label: "Revenue", value: `₹${(summary.revenue / 100000).toFixed(1)}L` },
        { label: "Qualified Leads", value: summary.qualified_leads },
        { label: "Conversion", value: `${summary.conversion_rate}%` },
        { label: "Avg AI Lead Score", value: summary.avg_ai_score ? `${summary.avg_ai_score}%` : "—" },
        { label: "Pipeline", value: `₹${(summary.pipeline / 100000).toFixed(1)}L` },
      ]
    : [];

  const chartData = summary
    ? [
        { name: "Total Leads", value: summary.total_leads },
        { name: "Qualified", value: summary.qualified_leads },
      ]
    : [];

  return (
    <div className="min-h-screen bg-app">
      <Navbar />
      <div className="p-6 max-w-6xl mx-auto">
        <h1 className="text-xl font-bold text-white mb-6">Dashboard</h1>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
          {cards.map((c, i) => (
            <div
              key={c.label}
              className="animate-fadeInUp bg-panel border border-panelBorder rounded-xl p-4 hover:border-accent/50 transition-colors"
              style={{ animationDelay: `${i * 60}ms`, animationFillMode: "backwards" }}
            >
              <p className="text-gray-500 text-xs">{c.label}</p>
              <p className="text-2xl font-bold text-accent mt-1">{c.value}</p>
            </div>
          ))}
        </div>

        <div className="bg-panel border border-panelBorder rounded-xl p-4 h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#242424" />
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{ backgroundColor: "#141414", border: "1px solid #242424", borderRadius: "8px", color: "#e5e5e5" }}
              />
              <Bar dataKey="value" fill="#22c55e" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
