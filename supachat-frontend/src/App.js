import './App.css';

import { useState } from "react";
import axios from "axios";
import ChatMessage from "./components/ChatMessage";
import ChatBox from "./components/ChatBox";
import QueryHistory from "./components/QueryHistory";
import ResultsTable from "./components/ResultsTabel";
import Charts from "./components/Charts";
import Loader from "./components/Loader";
import Error from "./components/Errors";

function App() {
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sendQuery = async (query) => {
    setMessages((prev) => [...prev, { role: "user", text: query }]);

    try {
      setLoading(true);
      setError("");
      // console.log("Sending query:", `${process.env.REACT_APP_API_URL}/query`);
      const res = await axios.post("/api/query", { query });

      if (res.data.error) throw new Error(res.data.error);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: res.data.summary || "Here are your results",
          data: res.data.data,
        },
      ]);

      setHistory((prev) => [query, ...prev]);

    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <QueryHistory history={history} onSelect={sendQuery} />

      <div className="chat-container">
        <div className="messages">
          {messages.map((msg, i) => (
            <ChatMessage key={i} {...msg} />
          ))}

          {loading && <Loader />}
          {error && <Error message={error} />}
        </div>

        <ChatBox onSend={sendQuery} loading={loading} />
      </div>
    </div>
  );
}

export default App;
