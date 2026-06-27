import { Link } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Sidebar() {

    const { logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate("/");
    };
    return (

        <div className="w-64 h-screen bg-slate-900 text-white p-5">

            <h1 className="text-3xl font-bold mb-8 text-cyan-300">
                WalShield
            </h1>

            <ul className="space-y-4">

                <li className="hover:text-cyan-300 hover:text-xl"><Link to="/dashboard">Dashboard</Link></li>

                <li className="hover:text-cyan-300 hover:text-xl"><Link to="/arp">ARP Scanner</Link></li>

                <li className="hover:text-cyan-300 hover:text-xl"><Link to="/portscanner">Port Scanner Detector</Link></li>

                <li className="hover:text-cyan-300 hover:text-xl"><Link to="/dos">DoS Detector</Link></li>

                <li className="hover:text-cyan-300 hover:text-xl"><Link to="/deauth">Deauth Detector</Link></li>

                <li className="hover:text-cyan-300 hover:text-xl"><Link to="/logs">Logs</Link></li>

                <li className="hover:text-cyan-300 hover:text-xl"><Link to="/settings">Settings</Link></li>

                <button className="bg-red-500 p-4 rounded-full hover:bg-red-200 hover:text-black rounded-full transition-all duration-700 hover:rotate-360 hover:cursor-pointer" onClick={handleLogout}>
                    Logout
                </button>

            </ul>

        </div>

    );

}

export default Sidebar;
