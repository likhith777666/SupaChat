export default function QueryHistory({ history, onSelect }) {
  return (
    <div className="sidebar">
      <h3>History</h3>
      {history.map((q, i) => (
        <div key={i} className="history-item" onClick={() => onSelect(q)}>
          {q}
        </div>
      ))}
    </div>
  );
}