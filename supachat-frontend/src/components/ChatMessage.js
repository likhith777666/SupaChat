import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar
} from "recharts";

export default function ChatMessage({ role, text, data }) {
const keys = data && data.length > 0 ? Object.keys(data[0]) : [];

let xKey = null;
let yKey = null;

if (data && data.length > 0) {
  // X-axis: prefer date or string
  xKey =
    keys.find(k => k.includes("date") || k.includes("time")) ||
    keys.find(k => typeof data[0][k] === "string") ||
    keys[0];

  // Y-axis: must be number
  yKey =
    keys.find(k => k === "views") ||
    keys.find(k => k === "likes") ||
    keys.find(k => typeof data[0][k] === "number");
}

  const showChart = data && keys.length >= 2;
  
  const formattedData = data
  ? data.map(row => ({
      ...row,
      views: Number(row.views),
      likes: Number(row.likes)
    }))
  : [];

  return (
    <div className={`message ${role}`}>
      <div className="bubble">
        <p>{text}</p>

        {/* TABLE */}
        {data && data.length > 0 && (
          <table>
            <thead>
              <tr>
                {keys.map((k) => (
                  <th key={k}>{k}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, i) => (
                <tr key={i}>
                  {Object.values(row).map((v, j) => (
                    <td key={j}>{v}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* CHART */}
        {showChart && (
          <div style={{ marginTop: "20px" }}>
            <LineChart width={400} height={250} data={formattedData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={xKey} />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey={yKey} />
            </LineChart>
          </div>
        )}
      </div>
    </div>
  );
}