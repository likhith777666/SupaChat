import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
} from "recharts";

export default function Charts({ data }) {
  if (!data || data.length === 0) return null;

  const keys = Object.keys(data[0]);

  if (keys.length < 2) return null;

  return (
    <div>
      <h3>Graph</h3>
      <LineChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey={keys[0]} />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey={keys[1]} />
      </LineChart>
    </div>
  );
}