import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";

export default function PathwayVisualizer({ pathway }) {
  const nodes = [];
  const edges = [];

  let y = 0;
  for (const week of pathway?.pathway || []) {
    const weekNodeId = `week-${week.week}`;
    nodes.push({
      id: weekNodeId,
      position: { x: 60, y },
      data: { label: `Week ${week.week} (${week.estimated_hours}h)` },
      style: { background: "#0b7285", color: "#fff", padding: 10, borderRadius: 8, fontWeight: 700 },
    });

    let x = 320;
    for (const course of week.courses) {
      const courseId = `course-${course.id}`;
      nodes.push({
        id: courseId,
        position: { x, y },
        data: { label: `${course.title} (${course.duration_hours}h)` },
        style: { width: 240, padding: 10, borderRadius: 8, border: "2px solid #0b7285", background: "#f1f3f5" },
      });
      edges.push({ id: `${weekNodeId}-${courseId}`, source: weekNodeId, target: courseId, animated: true });
      for (const prereq of course.prerequisites || []) {
        edges.push({ id: `${prereq}-${course.id}`, source: `course-${prereq}`, target: courseId, type: "smoothstep" });
      }
      x += 290;
    }
    y += 160;
  }

  return (
    <section className="panel">
      <h2>Learning Pathway</h2>
      <div className="flow-wrap">
        <ReactFlow nodes={nodes} edges={edges} fitView>
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </section>
  );
}
