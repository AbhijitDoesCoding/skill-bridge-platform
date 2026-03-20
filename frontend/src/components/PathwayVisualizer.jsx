import ReactFlow, { Background, Controls } from "reactflow";
import "reactflow/dist/style.css";

export default function PathwayVisualizer({ pathway }) {
  const nodes = [];
  const edges = [];

  const weekStyle = {
    background: '#f4b400',
    color: '#111',
    padding: '10px',
    borderRadius: '10px',
    fontWeight: 800,
    border: 'none',
    width: 140,
    textAlign: 'center',
  };

  const courseStyle = {
    background: '#ffffff',
    color: '#111',
    padding: '12px',
    borderRadius: '12px',
    border: '1px solid #eee',
    boxShadow: '0 4px 10px rgba(0,0,0,0.05)',
    width: 250,
    fontSize: '13px',
  };

  let y = 0;
  for (const week of pathway?.pathway || []) {
    const weekNodeId = `week-${week.week}`;
    nodes.push({
      id: weekNodeId,
      position: { x: 50, y },
      data: { label: `WEEK ${week.week}` },
      style: weekStyle,
    });

    let x = 250;
    for (const course of week.courses) {
      const courseId = `course-${course.id}`;
      nodes.push({
        id: courseId,
        position: { x, y },
        data: { label: `${course.title} (${course.duration_hours}h)` },
        style: courseStyle,
      });
      edges.push({ 
        id: `${weekNodeId}-${courseId}`, 
        source: weekNodeId, 
        target: courseId, 
        animated: true,
        style: { stroke: '#f4b400', strokeWidth: 2 }
      });
      for (const prereq of course.prerequisites || []) {
        edges.push({ 
          id: `${prereq}-${course.id}`, 
          source: `course-${prereq}`, 
          target: courseId, 
          type: "smoothstep",
          style: { stroke: '#ccc' }
        });
      }
      x += 280;
    }
    y += 150;
  }

  return (
    <div className="flow-container">
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background color="#f0f0f0" gap={20} size={1} />
        <Controls />
      </ReactFlow>
    </div>
  );
}
