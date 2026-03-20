import { Bar, BarChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const rank = {
  none: 0,
  beginner: 1,
  intermediate: 2,
  advanced: 3,
};

export default function SkillGapChart({ data }) {
  const chartData = (data?.gaps || []).map((gap) => ({
    skill: gap.skill,
    current: rank[gap.current_level] ?? 0,
    required: rank[gap.required_level] ?? 0,
  }));

  return (
    <section className="panel">
      <h2>Skill Gap Analysis</h2>
      <p>Readiness: {data?.readiness_percentage ?? 0}%</p>
      <div className="chart-wrap">
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="skill" interval={0} angle={-25} textAnchor="end" height={80} />
            <YAxis domain={[0, 3]} ticks={[0, 1, 2, 3]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="current" fill="#0b7285" name="Current Level" />
            <Bar dataKey="required" fill="#f08c00" name="Required Level" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </section>
  );
}
