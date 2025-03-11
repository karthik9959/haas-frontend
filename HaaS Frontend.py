// HaaS Frontend - Real-Time Attack Log Dashboard

import { useEffect, useState } from "react";
import io from "socket.io-client";

const socket = io("http://localhost:5000"); // Connect to the backend

export default function Dashboard() {
  const [attacks, setAttacks] = useState([]);

  useEffect(() => {
    // Fetch initial attacks
    fetch("http://localhost:5000/attacks")
      .then((res) => res.json())
      .then((data) => setAttacks(data));

    // Listen for real-time attack updates
    socket.on("new_attack", (newAttack) => {
      setAttacks((prevAttacks) => [newAttack, ...prevAttacks]);
    });

    return () => socket.off("new_attack"); // Cleanup listener
  }, []);

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-4">Honeypot Attack Logs</h1>
      <div className="bg-white p-4 rounded-lg shadow-md">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-200">
              <th className="border p-2">IP Address</th>
              <th className="border p-2">Port</th>
              <th className="border p-2">Protocol</th>
              <th className="border p-2">Payload</th>
              <th className="border p-2">Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {attacks.map((attack, index) => (
              <tr key={index} className="border">
                <td className="p-2">{attack.ip}</td>
                <td className="p-2">{attack.port}</td>
                <td className="p-2">{attack.protocol}</td>
                <td className="p-2">{attack.payload}</td>
                <td className="p-2">{new Date(attack.timestamp).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
