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

  const readiness = data?.readiness_percentage ?? 0;

  return (
    <div className="chart-container">
       <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 50 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#eee" />
            <XAxis 
              dataKey="skill" 
              interval={0} 
              angle={-25} 
              textAnchor="end" 
              height={80} 
              stroke="#666" 
              fontSize={12} 
            />
            <YAxis 
              domain={[0, 3]} 
              ticks={[0, 1, 2, 3]} 
              stroke="#666" 
              fontSize={12} 
            />
            <Tooltip 
              cursor={{ fill: '#f9f9f9' }}
              contentStyle={{ borderRadius: '12px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}
            />
            <Legend verticalAlign="top" height={36}/>
            <Bar dataKey="current" fill="#f4b400" name="Your Level" radius={[4, 4, 0, 0]} barSize={40} />
            <Bar dataKey="required" fill="#111111" name="Required Level" radius={[4, 4, 0, 0]} barSize={40} />
          </BarChart>
        </ResponsiveContainer>
    </div>
  );
}
