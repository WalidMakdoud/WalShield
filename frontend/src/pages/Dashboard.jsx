import Sidebar from "../components/Sidebar";
import { Link } from "react-router-dom";

function Dashboard() {

    return (

        <div className="flex">

            <Sidebar />

            <div className="flex-1 p-8">

                <h1 className="text-4xl font-bold mb-8">
                    Dashboard
                </h1>

                <div className="grid grid-cols-2 gap-6">

                    <Link to="/arp">

                        <div className="bg-blue-600 text-white rounded-xl p-8 hover:bg-blue-700">

                            <h2 className="text-2xl font-bold">
                                ARP Scanner
                            </h2>

                        </div>

                    </Link>

                    <Link to="/portscanner">

                        <div className="bg-green-600 text-white rounded-xl p-8">

                            <h2 className="text-2xl font-bold">
                                Port Scanner
                            </h2>

                        </div>

                    </Link>

                    <Link to="/dos">

                        <div className="bg-red-600 text-white rounded-xl p-8">

                            <h2 className="text-2xl font-bold">
                                DoS Detector
                            </h2>

                        </div>

                    </Link>

                    <Link to="/logs">

                        <div className="bg-purple-600 text-white rounded-xl p-8">

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
