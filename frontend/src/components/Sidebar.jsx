import { Link } from "react-router-dom";

function Sidebar() {

    return (

        <div className="w-64 h-screen bg-slate-900 text-white p-5">

            <h1 className="text-3xl font-bold mb-8">
                WalShield
            </h1>

            <ul className="space-y-4">

                <li><Link to="/dashboard">Dashboard</Link></li>

                <li><Link to="/arp">ARP Scanner</Link></li>

                <li><Link to="/portscanner">Port Scanner</Link></li>

                <li><Link to="/dos">DoS Detector</Link></li>

                <li><Link to="/portdetector">Port Detector</Link></li>

                <li><Link to="/logs">Logs</Link></li>

                <li><Link to="/settings">Settings</Link></li>

            </ul>

        </div>

    );

}

export default Sidebar;
