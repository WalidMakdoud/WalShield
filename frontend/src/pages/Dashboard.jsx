import Sidebar from "../components/Sidebar";
import { Link } from "react-router-dom";

function Dashboard() {
  return (
    <div className="flex min-h-screen bg-gray-100">
      <Sidebar />

      <div className="flex-1 p-8">
        <h1 className="text-4xl font-bold mb-8 text-gray-800">
          Dashboard
        </h1>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link to="/arp">
            <div className="bg-blue-600 text-white rounded-xl p-8 shadow-lg hover:bg-blue-500 transition duration-300 cursor-pointer">
              <h2 className="text-2xl font-bold">
                ARP Scanner
              </h2>
            </div>
          </Link>

          <Link to="/portscanner">
            <div className="bg-green-600 text-white rounded-xl p-8 shadow-lg hover:bg-green-500 transition duration-300 cursor-pointer">
              <h2 className="text-2xl font-bold">
                Port Scanner Detector
              </h2>
            </div>
          </Link>

          <Link to="/dos">
            <div className="bg-red-600 text-white rounded-xl p-8 shadow-lg hover:bg-red-500 transition duration-300 cursor-pointer">
              <h2 className="text-2xl font-bold">
                DoS Detector
              </h2>
            </div>
          </Link>

          <Link to="/deauth">
            <div className="bg-yellow-500 text-white rounded-xl p-8 shadow-lg hover:bg-yellow-400 transition duration-300 cursor-pointer">
              <h2 className="text-2xl font-bold">
                Deauth Detector
              </h2>
            </div>
          </Link>

          <Link to="/logs">
            <div className="bg-purple-600 text-white rounded-xl p-8 shadow-lg hover:bg-purple-500 transition duration-300 cursor-pointer">
              <h2 className="text-2xl font-bold">
                Logs
              </h2>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;