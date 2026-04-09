import { useState } from "react";

export default function ChatBox({ onSend, loading }) {
  const [query, setQuery] = useState("");

  const handleSend = () => {
    if (!query.trim()) return;
    onSend(query);
    setQuery("");
  };

  return (
    <div className="chat-input">
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask about your data..."
      />
      <button onClick={handleSend} disabled={loading}>
        ➤
      </button>
    </div>
  );
}