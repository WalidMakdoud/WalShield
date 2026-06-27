import { useEffect, useState } from "react";
import Sidebar from "../components/Sidebar";

function DosScanne() {
  const [devices, setDevices] = useState([]);

  useEffect(() => {
    async function loadArpData() {
      try {
        const response = await fetch("http://127.0.0.1:8000/dos");
        const data = await response.json();
        setDevices(data);
      } catch (error) {
        console.error(error);
      }
    }

    loadArpData();
  }, []);

  return (
  <div className="flex">
    <Sidebar />

    <div className="flex-1 p-10">
      <h1 className="text-3xl font-bold mb-6">
        Dos Scanner
      </h1>

      <table className="w-full border">
        <thead className="bg-gray-200">
          <tr>
            <th className="border p-2">IP Address</th>
          </tr>
        </thead>

        <tbody>
          {devices.map((device, index) => (
            <tr key={index}>
              <td className="border p-2">{device.ip}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);
}

export default DosScanne; 